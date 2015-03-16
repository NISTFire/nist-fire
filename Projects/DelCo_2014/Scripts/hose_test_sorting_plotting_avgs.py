#!/usr/bin/env python

import os
import numpy as np
import pandas as pd
from pylab import *
import math

from matplotlib import rcParams
rcParams.update({'figure.autolayout': True})

#  =================
#  = User Settings =
#  =================

# Location of experimental data files
data_dir = '../Experimental_Data/'
results_dir = '../Results/'

# Location of file with timing information
timings_file = '../Experimental_Data/All_Hose_Times.csv'

# Location of scaling conversion files
scaling_file_default = '../DAQ_Files/Delco_DAQ_Channel_List.csv'
scaling_file_master = '../DAQ_Files/Master_DelCo_DAQ_Channel_List.csv'
scaling_file_west = '../DAQ_Files/West_DelCo_DAQ_Channel_List.csv'
scaling_file_east = '../DAQ_Files/East_DelCo_DAQ_Channel_List.csv'
results_loc = '../Experimental_Data/'

# Location of test description file
info_file = '../Experimental_Data/Description_of_Experiments.csv'
# Hose description file
hose_info_file = '../Experimental_Data/Description_Hose_Experiments.csv'

# Duration of pre-test time for bi-directional probes and heat flux gauges (s)
pre_test_time = 60

# List of sensor groups for each plot
sensor_groups = [['TC_A1_'], ['TC_A2_'], ['TC_A3_'], ['TC_A4_'], ['TC_A5_'],
                 ['TC_A6_'], ['TC_A7_'], ['TC_A8_'], ['TC_A9_'], ['TC_A10_'],
                 ['TC_A11_'], ['TC_A12_'], ['TC_A13_'], ['TC_A14_'], ['TC_A15_'],
                 ['TC_A16_'], ['TC_A17_'], ['TC_A18_'], ['TC_A19_'],
                 ['TC_Ignition'],
                 ['TC_Helmet_'],
                 ['BDP_A4_'], ['BDP_A5_'], ['BDP_A6_'], ['BDP_A7_'],
                 ['BDP_A8_'], ['BDP_A9_'], ['BDP_A10_'], ['BDP_A11_'],
                 ['BDP_A12_'], ['BDP_A13_'], ['BDP_A14_'], ['BDP_A15_'],
                 ['BDP_A18_'],
                 ['HF_', 'RAD_'],
                 ['GAS_', 'CO_', 'CO2_', 'O2_'],
                 ['HOSE_']]

# Common quantities for y-axis labelling
heat_flux_quantities = ['HF_', 'RAD_']
gas_quantities = ['CO_', 'CO2_', 'O2_']

# Load exp. timings, description, and averages file
timings = pd.read_csv(timings_file, index_col=0)
desired_tests = list(timings.columns.values)			# creates list of  column headers which correspond
hose_info = pd.read_csv(hose_info_file, index_col=0) 	# to desired tests listed in All_Hose_Time.csv file
info = pd.read_csv(info_file, index_col=3)

# Files to skip
skip_files = ['_times', '_reduced', '_results', 'description_']

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
		print 'Loaded ' + test_name

		# Skips undesired tests
		if test_name not in desired_tests:
			continue

		# Load exp. data file
		data = pd.read_csv(data_dir + f, index_col=0)

		# Load exp. scaling file
		if 'West' in test_name:
			scaling_file = scaling_file_west
		elif 'East' in test_name:
			scaling_file = scaling_file_east
		else:
			scaling_file = scaling_file_default

		scaling = pd.read_csv(scaling_file, index_col=2)

		# Read in test times to offset plots 
		start_of_test = info['Start of Test'][test_name]
		end_of_test = info['End of Test'][test_name]

		# Offset data time to start of test
		t = data['Time'].values - start_of_test

		# Save converted time back to dataframe
		data['Time'] = t

		#  ============
		#  = Sorting =
		#  ============

		# Generate a plot for each quantity group
		for group in sensor_groups:
			# Skips all groups not in "included groups" in hose_info file
			if any([substring in group for substring in hose_info['Included Groups'][test_name].split('|')]) == False:
				continue

			# creates empty "stream" list for the sensor group's results file
			blank_list = []
			group_set = {'Stream': blank_list}
 			group_results = pd.DataFrame(group_set, columns = ['Stream'])

 			# reads in the stream patterns based on hose_info file
			for diff in hose_info['Difference'][test_name].split('|'):
				group_results[diff] = ' '
			row_num = 0

			fig = figure()

			# resets max and min y values
			max_y = 0
			min_y = 0

			# Defines start and end times for different stream patterns
			for stream in hose_info.columns[2:5]:
				# ignores streams not involved in test (specified in hose_info file)
				if hose_info[stream][test_name] == False:
					continue

				# reads start and end times for current stream from hose_info file
				start_name = stream + '_start'
				start = hose_info[start_name][test_name]
				end_name = stream + '_end'
				end = hose_info[end_name][test_name]

				# Creates data set of start and end times for current hose stream 
				stream_data = data.iloc[start:end]
				t_stream = stream_data['Time']

				# Creates empty data frame (with time index) to plot average of channels for each stream and sensor group
				stream_group = pd.DataFrame(t_stream)

				for channel in stream_data.columns[1:]:
					# Skip excluded channels listed in hose_info file
					if any([substring in channel for substring in hose_info['Excluded Channels'][test_name].split('|')]):
						continue

					if any([substring in channel for substring in group]):

						calibration_slope = float(scaling['Calibration Slope'][channel])
						calibration_intercept = float(scaling['Calibration Intercept'][channel])

						# Plot velocities
						if 'BDP_' in channel:
							plt.rc('axes', color_cycle=['k', 'b', 'r', 'b', '0.75', 'c', 'm', 'y'])
							conv_inch_h2o = 0.4
							conv_pascal = 248.8

							# Convert voltage to pascals
							# Get zero voltage from pre-test data
							zero_voltage = np.mean(stream_data[channel][0:pre_test_time])
							pressure = conv_inch_h2o * conv_pascal * (stream_data[channel] - zero_voltage)

							# Calculate velocity
							quantity = 0.0698 * np.sqrt(np.abs(pressure) * (stream_data['TC_' + channel[4:]] + 273.15)) * np.sign(pressure)
							ylabel('Velocity (m/s)', fontsize=20)
							line_style = '-'
							axis_scale = 'Y Scale BDP'

						# # Plot hose pressure
						# if 'HOSE_' in channel:
						# 	plt.rc('axes', color_cycle=['k', 'r', 'g', 'b', '0.75', 'c', 'm', 'y'])
						# 	# Skip data other than sensors on 2.5 inch hoseline
						# 	if '2p5' not in channel:
						# 		continue
						# 	quantity = stream_data[channel] * calibration_slope + calibration_intercept
						# 	ylabel('Pressure (psi)', fontsize=20)
						# 	line_style = '-'
						# 	axis_scale = 'Y Scale HOSE'

						# Save converted quantity back to exp. dataframe and sensor group dataframe
						stream_data[channel] = quantity
						stream_group[channel] = quantity

				# Calculates the average of all channels in sensor group from recently created sensor group dataframe
				group_avg = []
				for index, row in stream_group.iterrows():
					avg = np.mean(row[1:])
					group_avg.append(avg)

				# Adds a column of the average of all channels to the dataframe 
				stream_group['Average of Channels'] = group_avg

				# determines the max and min y values for the sensor group averages
				if max(group_avg) > max_y:
					max_y = math.ceil(max(group_avg))
				if min(group_avg) < min_y:
					min_y = math.floor(min(group_avg))

				# reads time before first experiment begins
				start_time = hose_info['Start'][test_name]
				# reads in time after beginning of experiment to when FP is complete
				FP_beg = hose_info['Flowpath complete'][test_name]
				# Averages for when flow path is completely established for each hose stream
				diff_avgs = []
				for diff in hose_info['Difference'][test_name].split('|'):
					FP_end = FP_beg + hose_info['Duration'][test_name]
					diff_avgs.append(round(np.mean(stream_group['Average of Channels'][int(FP_beg):int(FP_end)]), 2))
					FP_beg = hose_info['Flowpath complete'][test_name] + FP_end + hose_info['Time Between'][test_name]
				
				# creates an array for data file for current sensor group
				data_row = np.append(stream, diff_avgs)
				group_results.loc[row_num]  = np.array(data_row)
				row_num = row_num + 1

				t = arange(len(stream_group.index))

				# plots average for current stream in current sensor group
				plot(t, group_avg, lw=1.5, ls='-', label=stream + ' Average')

			#Saves results .csv file for sensor group
			group_results.to_csv(results_dir + test_name + '_' + str(group)[2:-2]  + 'averages.csv')
			print 'Saving ' + test_name + '_' + str(group)[2:-2]  + 'Averages'

			# format plot of averages for different streams in sensor group
			ylim([min_y, max_y])

			# Set axis options, legend, tickmarks, etc.
			ax1 = gca()
			xlim(0, len(t))
			ax1.xaxis.set_major_locator(MaxNLocator(8))
			ax1_xlims = ax1.axis()[0:2]
			ax1.axhspan(0, 0, color='0.50', lw=1)
			#grid(True)
			xlabel('Time', fontsize=20)
			ylabel('Velocity (m/s)', fontsize=20)
			xticks(fontsize=16)
			yticks(fontsize=16)
			legend(loc='lower right', fontsize=8)

			try:
				# Add vertical lines for timing information (if available)
				for index, row in timings.iterrows():
					if pd.isnull(row[test_name]):
						continue
					axvline(index-start_of_test-start_time, color='0.50', lw=1)

				# Add secondary x-axis labels for timing information
				ax2 = ax1.twiny()
				ax2.set_xlim(ax1_xlims)
				ax2.set_xticks(timings[test_name].dropna().index.values - (start_of_test)-start_time)
				setp(xticks()[1], rotation=60)
				ax2.set_xticklabels(timings[test_name].dropna().values, fontsize=8, ha='left')
				xlim(0, t)

			except:
				pass

			# Increase figure size for plot labels at top
			fig.set_size_inches(8, 8)

			# Save plot to file
			print 'Plotting ' + str(group)[2:-2] + ' Channel Average'
			savefig('../Figures/Hose_Test_Figures/' + test_name + '_' + str(group)[2:-2] + 'Avg.pdf')
			close('all')