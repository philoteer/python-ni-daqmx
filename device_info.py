#!/usr/bin/env python3

import nidaqmx

dev_list = nidaqmx.system._collections.device_collection.DeviceCollection().device_names
print(f"List of devices: {dev_list}")

for dev in dev_list:
	phy_ch = nidaqmx.system._collections.physical_channel_collection.AIPhysicalChannelCollection(dev).channel_names
	print("="*80)
	print(f"dev: {dev}")
	print(f"ch_list: {phy_ch}")
	
	sys_dev = nidaqmx.system.device.Device(dev)
	print("")
	print(f"ai_couplings: {sys_dev.ai_couplings}")
	print(f"ai_dig_fltr_types: {sys_dev.ai_dig_fltr_types}")
	print(f"ai_freq_rngs: {sys_dev.ai_freq_rngs}")
	print(f"ai_gains: {sys_dev.ai_gains}")
	print(f"ai_max_multi_chan_rate: {sys_dev.ai_max_multi_chan_rate}")
	print(f"ai_max_single_chan_rate: {sys_dev.ai_max_single_chan_rate}")
	print(f"ai_meas_types: {sys_dev.ai_meas_types}")
	print(f"ai_samp_modes: {sys_dev.ai_samp_modes}")
	print(f"ai_simultaneous_sampling_supported: {sys_dev.ai_simultaneous_sampling_supported}")
