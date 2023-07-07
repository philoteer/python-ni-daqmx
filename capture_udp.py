#!/usr/bin/env python3

import nidaqmx
import nidaqmx.stream_readers
import nidaqmx.constants as consts
import numpy as np 
import matplotlib.pyplot as plt
import time
import socket
########################################################################
######### Consts
########################################################################

### DAQ
fs = 1000
num_ch = 2
buf_len = fs #true buffer len = buf_len * num_ch  (* size per sample)
timeout = 2
dev = "Dev1"

channels = []
for i in range (0, num_ch):
	channels.append( {"port" : f"{dev}/ai{i}", "name" : f"Ch{str(i+1)}" , "min_val" : -5.0, "max_val" : 5.0, "units":consts.VoltageUnits.VOLTS})

### UDP Socket
server_ip = "127.0.0.1"
#server_ip = "141.223.84.137"
server_port = 8087

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
dest = (server_ip, server_port)
pkt_max_len = 2048 #warning: larger than the safe udp pkt size

########################################################################
######### Set up the DAQ
########################################################################

task = nidaqmx.Task() 

#add channels
for ch in channels:
	task.ai_channels.add_ai_voltage_chan(ch["port"], name_to_assign_to_channel=ch["name"],terminal_config=consts.TerminalConfiguration.DEFAULT, min_val= ch["min_val"], max_val= ch["max_val"], units= ch["units"], custom_scale_name='')

#configure daq, start
task.timing.cfg_samp_clk_timing(fs, source="", active_edge=consts.Edge.RISING, sample_mode=consts.AcquisitionType.CONTINUOUS)
task.start()

buf = np.zeros((num_ch, buf_len),dtype=np.float64) 
reader = nidaqmx.stream_readers.AnalogMultiChannelReader(task.in_stream)	

#uncomment if you want "number_of_samples_per_channel= nidaqmx.constants.READ_ALL_AVAILABLE"
#reader._verify_array_shape = False 

########################################################################
######### Do collection
########################################################################

# the main loop
print("Starting the collection.")
tx_cnt = 0
while True:
	nout = reader.read_many_sample(buf, number_of_samples_per_channel= buf_len, timeout=timeout)
	#if we got non-zero number of samples:
	if(nout > 0):
		#trim the buffer (only needed if number_of_samples_per_channel= nidaqmx.constants.READ_ALL_AVAILABLE)
		#data_tx = buf[0:nout*num_ch].astype(np.float32)	#2 by n_out		
		#data_tx = data_tx.reshape(num_ch,nout).T.flatten()
		data_tx = buf.astype(np.float32).T.flatten()
		
		#tx
		cnt = 0
		data_tx = data_tx.tobytes()
		data_len = len(data_tx)
		
		while ((cnt * pkt_max_len) < data_len): 
			sock.sendto(data_tx[pkt_max_len *cnt:pkt_max_len *cnt+pkt_max_len],dest)
			tx_cnt += len(data_tx[pkt_max_len *cnt:pkt_max_len *cnt+pkt_max_len])
			cnt += 1
		
	#time.sleep(0.1) #(for testing purpose only)
