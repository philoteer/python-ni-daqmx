#!/usr/bin/env python3
#Ref: 
#	samp rate: https://knowledge.ni.com/KnowledgeArticleDetails?id=kA00Z0000019ZWxSAM&l=ko-KR
#	cont. sampling: https://stackoverflow.com/questions/56366033/continuous-acquistion-with-nidaqmx
#	cont. sampling 2: https://forums.ni.com/t5/Multifunction-DAQ/real-time-read-plot-using-python/td-p/3905203

import nidaqmx
import nidaqmx.stream_readers
import nidaqmx.constants as consts
import numpy as np 
import matplotlib.pyplot as plt
import time

capture_len = 1000
dev = "Dev1"
fs = 1000
num_ai_ch = 32

channels = []
for i in range (0, num_ai_ch):
	channels.append( {"port" : f"{dev}/ai{i}", "name" : f"Ch{str(i+1)}" , "min_val" : -5.0, "max_val" : 5.0, "units":consts.VoltageUnits.VOLTS})

def single_shot(capture_len):
	with nidaqmx.Task() as task:
		for ch in channels:
			task.ai_channels.add_ai_voltage_chan(ch["port"], name_to_assign_to_channel=ch["name"],terminal_config=consts.TerminalConfiguration.DEFAULT, min_val= ch["min_val"], max_val= ch["max_val"], units= ch["units"], custom_scale_name='')
		task.timing.cfg_samp_clk_timing(fs, source="", active_edge=consts.Edge.RISING, sample_mode=consts.AcquisitionType.CONTINUOUS)
		return task.read(capture_len)	

capture = np.array(single_shot(capture_len))
print(capture)
print(np.shape(capture))
plt.plot(capture.T)
plt.show()
