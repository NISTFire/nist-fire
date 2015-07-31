#!/usr/bin/env python

import os
import collections
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from itertools import cycle

import numpy.ma as ma
from pylab import *
import math
import string

from matplotlib import rcParams
rcParams.update({'figure.autolayout': True})

#  =================
#  = User Settings =
#  =================

# Choose Test Number
current_test = 'Test_46_West_71015'

# Constants for Calculations
Area_A5_A6 = 3.716/16
Area_A10 = 2.168/8

# Location of experimental data files
data_dir = '../Experimental_Data/'

# Location of file with timing information
all_times_file = '../Experimental_Data/All_Times.csv'

# Location of scaling conversion files
scaling_file_west = '../DAQ_Files/West_DelCo_DAQ_Channel_List.csv'
scaling_file_east = '../DAQ_Files/East_DelCo_DAQ_Channel_List.csv'

# Location of test description file
info_file = '../Experimental_Data/Description_of_Experiments.csv'

# Location to save/output figures
save_dir = '../Figures/HRR_Script_Figures/'
if not os.path.exists(save_dir):
    os.makedirs(save_dir)

# Time averaging window for data smoothing
data_time_averaging_window = 10

# Duration of pre-test time for bi-directional probes and heat flux gauges (s)
pre_test_time = 60

# Load exp. timings and description file
all_times = pd.read_csv(all_times_file)
all_times = all_times.set_index('Time')
info = pd.read_csv(info_file, index_col=3)

# List of sensor groups for each plot
sensor_groups = [['TC_A5_'],['TC_A6_'],['TC_A10_'],['BDP_A5_'],['BDP_A6_'],['BDP_A10_']]

# Files to skip
skip_files = ['_times', '_reduced', 'description_','zero_','_rh','east']

#  =============================
#  = Property Lookup Functions =
#  =============================

def density (T):

	density_temp = [10,15,20,25,30,40,50,60,70,80,90,100,200,300,400,500,1000]
	density_value = [1.247,1.225,1.204,1.184,1.165,1.127,1.109,1.060,
				1.029,.9996,.9721,.9461,.7461,.6159,.5243,.4565,.2772]

	rho = np.zeros(len(T))

	for h in range (0,len(T)):
		for i in range(0,len(density_temp)):
			if T[h] < density_temp[i] and T[h] > density_temp[i-1]:
				rho[h] = density_value[i] - (density_value[i]-density_value[i-1])*(density_temp[i]-T[h])/(density_temp[i]-density_temp[i-1])
			else:
				continue
	return rho;

def heatCapacity (T):

	T_Kelvin = T + 274.15

	cp_temp = [250,300,350,400,450,500,550,600,650,700,750,800,900,1000,1100,1200,1300,1400,1500]
	cp_value = [1.003,1.005,1.008,1.013,1.020,1.029,1.040,1.051,1.063,
				1.075,1.087,1.099,1.121,1.142,1.155,1.173,1.190,1.204,1.216]

	cp = np.zeros(len(T))

	for h in range(0,len(T)):
		for i in range(0,len(cp_temp)):
			if T_Kelvin[h] < cp_temp[i] and T_Kelvin[h] > cp_temp[i-1]:
				cp[h] = cp_value[i] - (cp_value[i]-cp_value[i-1])*(cp_temp[i]-T_Kelvin[h])/(cp_temp[i]-cp_temp[i-1])
			else:
				continue
	return cp;


#  ===============================
#  = Loop through all data files =
#  ===============================

for f in os.listdir(data_dir):
	if f.endswith('.csv'):

		# Skip files with time information or reduced data files
		if any([substring in f.lower() for substring in skip_files]):
		    continue

		# Strip test name from file name
		test_name = f[:-4]
		print 'Test ' + test_name

		# Option to specify which test is run
		# if test_name != current_test:
		# 	continue

		# Skip Test 39, it gets run its own unique script
		if test_name == 'Test_39_West_61315':
			continue

		# Load exp. scaling file
		if 'West' in test_name:
		    channel_list_file = scaling_file_west
		elif 'East' in test_name:
		    channel_list_file = scaling_file_east

		channel_list = pd.read_csv(channel_list_file)
		channel_groups = sensor_groups

		# Read in test times to offset plots
		start_of_test = info['Start of Test'][test_name]
		end_of_test = info['End of Test'][test_name]

		# Read in Ambient Temperature from Test day
		T_infinity = info['Ambient Temp'][test_name]

		# Load exp. data file
		data = pd.read_csv(data_dir + f)
		data = data.set_index('TimeStamp(s)')

		# Offset data time to start of test
		data['Time'] = data['Time'].values - start_of_test

		# Smooth all data channels with specified data_time_averaging_window
		data_copy = data.drop('Time', axis=1)
		data_copy = pd.rolling_mean(data_copy, data_time_averaging_window, center=True)
		data_copy.insert(0, 'Time', data['Time'])
		data_copy = data_copy.dropna()
		data = data_copy

		quantity_v = np.zeros((len(data),8))
		quantity_tc = np.zeros((len(data),8))

		rho = np.zeros((len(data),8))
		cp = np.zeros((len(data),8))
		mass_flow = np.zeros((len(data),8))
		q_dot_channels = np.zeros(len(data))
		q_dot_groups = np.zeros(len(data))

		#  ============
		#  = Get Data =
		#  ============

		for group in sensor_groups: #cycle through specified groups
			for channel in data.columns[1:]:	#go through the channels
				# Find Excluded Channels
				if any([substring in channel for substring in info['HRR Excluded Channels'][test_name].split('|')]):
					channel_name = channel[:-1]
					channel_number = int(channel[-1:])
					if channel_number is 1:	# Replace channel 1 with channel 2
						data[channel] = data[(channel_name + (channel_number + 1))]
					elif channel_number is 8:	# Replace channel 8 with channel 7
						data[channel] = data[(channel_name + (channel_number - 1))]
					else:	# Replace current channel with average of channels above and below
						data[channel] = np.mean([data[channel_name + str(channel_number-1)],data[channel_name + str(channel_number+1)]])
				if not 'BDP_' in channel:	#operate only on BDPs
					continue
				if any([substring in channel for substring in group]):
				# Scale channel and set plot options depending on quantity
					current_channel_data = data[channel]
					conv_inch_h2o = 0.4
					conv_pascal = 248.8
					zero_voltage = np.mean(data[channel][0:pre_test_time])
					pressure = conv_inch_h2o * conv_pascal * (current_channel_data - zero_voltage)  # Convert voltage to pascals
					# Calculate velocity
					quantity_v[:,int(channel[-1:])-1] = 0.0698 * np.sqrt(np.abs(pressure) * (data['TC_' + channel[4:]] + 273.15)) * np.sign(pressure)
					# Grab corresponding TC
					quantity_tc[:,int(channel[-1:])-1] = data['TC_' + channel[4:]] 

			# HRR Calculation
			if 'BDP_A5_' in group or 'BDP_A6_' in group or 'BDP_A10_' in group:
				for channel in range(0,8):
					rho[:,channel] = density(quantity_tc[:,channel])
					cp[:,channel] = heatCapacity(quantity_tc[:,channel])
					if 'BDP_A5_' in group or 'BDP_A6_' in group:
						mass_flow[:,channel] = rho[:,channel]*quantity_v[:,channel]*Area_A5_A6
					else:
						mass_flow[:,channel] = rho[:,channel]*quantity_v[:,channel]*Area_A10
					q_dot_channels[:] += mass_flow[:,channel]*cp[:,channel]*(quantity_tc[:,channel]-T_infinity)
				q_dot_groups += q_dot_channels
		#print max(q_dot_groups)

		#  ============
		#  = Plotting =
		#  ============

		fig = figure()
		# Set axis options, legend, tickmarks, etc.
		ax1 = plt.gca()
		handles1, labels1 = ax1.get_legend_handles_labels()
		plt.xlim([0, end_of_test - start_of_test])
		ax1.xaxis.set_major_locator(plt.MaxNLocator(8))
		ax1_xlims = ax1.axis()[0:2]
		plt.grid(True)
		plt.xlabel('Time (s)', fontsize=20)
		plt.xticks(fontsize=16)
		plt.yticks(fontsize=16)
		plt.ylabel('Heat Release Rate (kW)', fontsize=20)
		plt.ylim([0, 7000])
		plt.xticks(fontsize=16)
		plt.yticks(fontsize=16)
		grid(True)
		plot(data['Time'],q_dot_groups)

		#Add vertical lines and labels for timing information (if available)
		try:
			ax3 = ax1.twiny()
			ax3.set_xlim(ax1_xlims)
			events = all_times[test_name].dropna()
			events = events[~events.str.startswith('#')]
			[plt.axvline(_x - start_of_test, color='0.50', lw=1) for _x in events.index.values]
			ax3.set_xticks(events.index.values - start_of_test)
			plt.setp(plt.xticks()[1], rotation=60)
			ax3.set_xticklabels(events.values, fontsize=8, ha='left')
			plt.xlim([0, end_of_test - start_of_test])
			fig.set_size_inches(10, 6)
		except:
			pass
			
		savefig(save_dir + test_name + '_HRR.pdf',format='pdf')
		close()

