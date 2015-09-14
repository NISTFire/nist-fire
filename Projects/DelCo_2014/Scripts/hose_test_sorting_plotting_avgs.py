#!/usr/bin/env python

import os
import collections
import numpy as np
import pandas as pd
from pylab import *
import math
from itertools import cycle

from matplotlib import rcParams
rcParams.update({'figure.autolayout': True})

#  =================
#  = User Settings =
#  =================

# Location of experimental data files
data_dir = '../Experimental_Data/'
results_dir = '../Results/'
fig_dir = '../Figures/Hose_Test_Figures/'

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
desired_tests = []			
for name in list(timings.columns.values):				# creates list of  column headers which correspond
	if 'HOSE_D' in name:								# to desired tests listed in All_Hose_Times.csv file
		continue
	else:
		desired_tests.append(name)
hose_info = pd.read_csv(hose_info_file, index_col=0)
info = pd.read_csv(info_file, index_col=3)

# Files to skip
skip_files = ['_times', '_reduced', '_results', 'description_']

def movingaverage(interval, window_size):
    window = np.ones(int(window_size))/float(window_size)
    return np.convolve(interval, window, 'same')

#  ===============================
#  = Loop through all data files =
#  ===============================

# Convert voltage to pascals
conv_inch_h2o = 0.4
conv_pascal = 248.8

# Create lists for column titles for desired latex tables
streams = ['SS', 'NF', 'WF']
stream_ls = pd.Series(['\\textit{Straight}', '\\textit{Narrow Fog}', '\\textit{Wide Fog}'], index = streams)
west_hand_caption = 'Average air velocity (m/s) through stairwell door with fully established flow path for stream and pattern combinations during Tests 18 and 19'
west_hand_label = 'table:west_hand_A10_avgs'
west_mon_columns = ['\\textbf{Stream}', '\\textbf{Near}', '\\textbf{Far}', '\\textbf{Near}', '\\textbf{Far}']
west_hand_columns = ['\\textbf{Stream}', '\\textbf{Fixed}', '\\textbf{Sweeping}', '\\textbf{Clockwise}', '\\begin{tabular}{@{}c@{}} \\textbf{Counter} \\\ \\textbf{Clockwise} \\\ \\end{tabular}']
# east_mon_columns = 
east_hand_columns = ['\\textbf{Stream}', '\\textbf{Fixed}', '\\textbf{Clockwise}', '\\begin{tabular}{@{}c@{}} \\textbf{Counter} \\\ \\textbf{Clockwise} \\\ \\end{tabular}']


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

		# Find desired sensor groups to analyze
		for group in sensor_groups:
			# Skips all groups not in "included groups" in hose_info file
			if any([substring in group for substring in hose_info['Included Groups'][test_name].split('|')]) == False:
				continue

			# West Test Sorting/Plotting
			if 'Test' in test_name:
				########################################################
				# Generates event times and information for each event #
				########################################################

				# initialize lists and start_seq value
				start_seq = 0
				door_status = 'All closed'
				streams_ls = []
				P_or_L_ls = []		
				start_times_ls = []
				end_times_ls = []
				door_status_ls = []
				zero_time_ls = []

				if 'Test_16' in test_name or 'Test_17' in test_name:
					P_or_L_heading = 'Location'
				else:
					P_or_L_heading = 'Pattern'

				# gathers timing information from hose_times file
				for index, row in timings.iterrows():
					if pd.isnull(row[test_name]):
						continue

					else:
					# check if event in beginning of new test, if so add to array to re-zero voltages
						if ('Monitor on,' in row[test_name]) or ('Hose on,' in row[test_name]):
							zero_time_ls.append(index)

						# add information to event row
						if start_seq != 0:
							end_seq = index
							streams_ls.append(stream)
							P_or_L_ls.append(P_or_L)
							start_times_ls.append(start_seq)
							end_times_ls.append(end_seq)
							door_status_ls.append(door_status)

						if row[test_name] == '1st floor BC and stairwell doors closed':
							# experiment has ended
							door_status = 'All closed'
							row[test_name] = 'Doors closed'
							start_seq = 0
							continue

						# Determine stream type, pattern/location
						if any('traight stream' in row[test_name]):
							stream = 'SS'
							if 'straight stream' in row[test_name]:
								row[test_name] = row[test_name].replace('straight stream', stream)
							else:
								row[test_name] = row[test_name].replace('Straight stream', stream)
						elif any('arrow fog' in row[test_name]):
							stream = 'NF'
							if 'narrow fog' in row[test_name]:
								row[test_name] = row[test_name].replace('narrow fog', stream)
							else:
								row[test_name] = row[test_name].replace('Narrow fog', stream)
						elif any('ide fog' in row[test_name]):
							stream = 'WF'
							if 'wide fog' in row[test_name]:
								row[test_name] = row[test_name].replace('wide fog', stream)
							else:
								row[test_name] = row[test_name].replace('Wide fog', stream)
						
						# stores location, door status, pattern, and start time for next row
						if P_or_L_heading == 'Location':
							if 'near target' in row[test_name]:
								P_or_L = 'Near'
								row[test_name] = row[test_name].replace('near target', 'near')
							elif 'far target' in row[test_name]:
								P_or_L = 'Far'
								row[test_name] = row[test_name].replace('far target', 'far')
						else:
							if any('ixed' in row[test_name]):
								P_or_L = 'fixed'
							elif any('weeping' in row[test_name]):
								P_or_L = 'sweep'
							elif ' clockwise' in row[test_name]:
								P_or_L = 'CW'
								row[test_name] = row[test_name].replace('clockwise', P_or_L)
							elif any('counterclockwise' in row[test_name]):
								P_or_L = 'CCW'
								row[test_name] = row[test_name].replace('counterclockwise', P_or_L)

						if 'opened' in row[test_name]:
							if 'BC door' in row[test_name]:
								door_status = 'BC open'
							elif any('tairwell door' in row[test_name]):
								door_status = 'Stair open'
							elif 'A door' in row[test_name]:
								door_status = 'A open'
							else:
								print '[Error] "Opened read", no door found..'
								print '..reading line: ' + row[test_name]
								sys.exit()
						
						if 'A door closed' in row[test_name]:
							door_status = 'Closed A'

						start_seq = index

				group_set = {'Start': start_times_ls, 'End':end_times_ls, 'Stream':streams_ls, P_or_L_heading:P_or_L_ls,'Door':door_status_ls}
				group_results = pd.DataFrame(group_set, columns = ['Start', 'End', 'Stream', P_or_L_heading, 'Door'])
				
				# create empty df to fill with desired channel data
				start_data = group_results['Start'].iloc[0] - 25
				end_data = group_results['End'].iloc[-1]
				group_data = pd.DataFrame(data['Time'].iloc[0:end_data], columns = ['Time'])
				
				# find desired channel data, convert to velocity and add to group_data df
				for channel in data.columns[1:]:
					# Skip excluded channels listed in hose_info file
					if any([substring in channel for substring in hose_info['Excluded Channels'][test_name].split('|')]):
						continue

					if any([substring in channel for substring in group]):
						# calculate initial zero voltage, create empty list for calculated velocities
						zero_start = zero_time_ls[0] - 25
						zero_end = zero_time_ls[0] - 5
						zero_voltage = np.mean(data[channel][zero_start:zero_end])
						i = 1
						quantity = []
						# convert voltages to velocities
						for index, row in data.iloc[0:end_data].iterrows():
							# check if zero voltage needs to be re-calculated
							if (zero_time_ls[i] - 25) == row['Time']:
								zero_start = int(row['Time'])
								zero_end = zero_start + 20
								zero_voltage = np.mean(data[channel][zero_start:zero_end])
								# iterate i if additional zero voltages will be calculated
								if i < (len(zero_time_ls)-1):
									i += 1
						
							pressure = conv_inch_h2o * conv_pascal * (row[channel] - zero_voltage)
							quantity.append(0.0698 * np.sqrt(np.abs(pressure) * (row['TC_' + channel[4:]] + 273.15)) * np.sign(pressure))
							
						# add velocities to group_data df and add a column for channel to group_results df
						group_data[channel] = quantity
						group_results[channel] = ''
						print ' Added data for ' + channel

				# calculate channel avg at each second and add to group_data
				channel_avg = []
				for index, row in group_data.iterrows():
					channel_avg.append(np.mean(row[1:]))
				group_data['Avg'] = channel_avg
				print ' Calculated average of all channels'				

				###########################################################################
				# uncomment to produce .csv result files with channel avgs for each event #
				###########################################################################
				group_results['Avg'] = ''
				for index, row in group_results.iterrows():
					# grab start/end time for each event in new .csv file
					start = row['Start']
					end = row['End']
					seq_data = group_data.iloc[start:end]

					# Calculate average for each channel during sequence
					for column in group_results.columns[5:]:
						# calculate avg for each channel during event 
						group_results.loc[index, column] = round(np.mean(seq_data[column]), 2)

				# Saves results .csv file for sensor group
				group_results.to_csv(results_dir + test_name + '_' + str(group)[2:-2]  + 'averages.csv')
				print 'Saving ' + test_name + '_' + str(group)[2:-2]  + 'Averages'
				print

				###########################################################
				# uncomment to populate lists used for LaTeX table values #
				###########################################################
				# Handline
				if P_or_L_heading == 'Pattern':
					fixed_ls = pd.Series(range(3), index = streams)
					sweep_ls = pd.Series(range(3), index = streams)
					CW_ls = pd.Series(range(3), index = streams)
					CCW_ls = pd.Series(range(3), index = streams)
					for index, row in group_results.iterrows():
						if row['Door'] == 'BC open':
							start = row['Start']
							end = row['End']
							seq_data = group_data.iloc[start:end]
							if row['Pattern'] == 'fixed':
								fixed_ls[row['Stream']] = str(round(np.mean(seq_data['Avg']), 1)) + ' $\pm' + str(round(np.std(seq_data['Avg']), 1)) + '$'
							elif row['Pattern'] == 'sweep':
								sweep_ls[row['Stream']] = str(round(np.mean(seq_data['Avg']), 1)) + ' $\pm' + str(round(np.std(seq_data['Avg']), 1)) + '$'
							elif row['Pattern'] == 'CW':
								CW_ls[row['Stream']] = str(round(np.mean(seq_data['Avg']), 1)) + ' $\pm' + str(round(np.std(seq_data['Avg']), 1)) + '$'
							elif row['Pattern'] == 'CCW':
								CCW_ls[row['Stream']] = str(round(np.mean(seq_data['Avg']), 1)) + ' $\pm' + str(round(np.std(seq_data['Avg']), 1)) + '$'

						else:
							continue

					if 'Test_18' in test_name:
						fixed_18 = fixed_ls
						sweep_18 = sweep_ls
						CW_18 = CW_ls
						CCW_18 = CCW_ls
					elif 'Test_19' in test_name:
						fixed_19 = fixed_ls
						sweep_19 = sweep_ls
						CW_19 = CW_ls
						CCW_19 = CCW_ls
					else:
						print '[ERROR]: Creating west_handline table, neither Test 18 nor Test 19 read'
						sys.exit()

				# # Monitor
				# else:

				############
				# Plotting #
				############
				# set new figure, figure name; re-set y min and max
				fig = figure()
				y_min = 0
				y_max = 0
				t = group_data['Time']
				ylabel('Velocity (m/s)', fontsize=20)
				line_style = '-'
				axis_scale = 'Y Scale BDP'

				#############################################
				# uncomment to plot individual channel data #
				#############################################
				# Plot style - colors and markers
            	# These are the "Tableau 20" colors as RGB.
				tableau20 = [(31, 119, 180), (174, 199, 232), (255, 127, 14), (255, 187, 120),
					(44, 160, 44), (152, 223, 138), (214, 39, 40), (255, 152, 150),
					(148, 103, 189), (197, 176, 213), (140, 86, 75), (196, 156, 148),
					(227, 119, 194), (247, 182, 210), (127, 127, 127), (199, 199, 199),
					(188, 189, 34), (219, 219, 141), (23, 190, 207), (158, 218, 229)]

				# Scale the RGB values to the [0, 1] range, which is the format matplotlib accepts.
				for i in range(len(tableau20)):
					r, g, b = tableau20[i]
					tableau20[i] = (r / 255., g / 255., b / 255.)
				plt.rc('axes', color_cycle=tableau20)
				plot_markers = cycle(['s', 'o', '^', 'd', 'h', 'p','v','8','D','*','<','>','H'])
				fig_name = fig_dir + test_name + '_' + group[0].rstrip('_') + '.pdf'

				for channel in group_data.columns[1:-1]:
					quantity = group_data[channel]

					# check y min and max
					ma_quantity = movingaverage(quantity,5)
					q_max = max(ma_quantity)
					q_min = min(ma_quantity)
					if q_max > y_max:
						y_max = q_max
					if q_min < y_min:
						y_min = q_min

					plot(t, ma_quantity, lw=1.5, ls=line_style, label=scaling['Test Specific Name'][channel])
					print ' Plotting channel ' + channel

				#############################################
				# uncomment to plot average of all channels #
				#############################################
				# fig_name = fig_dir + test_name + '_' + group[0].rstrip('_') + '_avg.pdf'

				# quantity = group_data['Avg']
				# ma_quantity = movingaverage(quantity, 5)
				# y_max = max(ma_quantity)
				# y_min = min(ma_quantity)

				# plot(t, ma_quantity, lw=1.5, ls=line_style, label=group_results.columns[5:-1], color = 'b')

			# East Tests Sorting/Plotting
			else:
				########################################################
				# Generates event times and information for each event #
				########################################################

				# initialize lists and start_seq value
				start_seq = 0
				door_status = 'C'
				streams_ls = []
				patterns_ls = []		
				start_times_ls = []
				end_times_ls = []
				location_ls = []
				door_status_ls = []
				zero_time_ls = []

				# gathers timing information from hose_times file
				for index, row in timings.iterrows():
					if pd.isnull(row[test_name]):
						continue

					else:
						# mark event start time or add event info to lists
						if start_seq == 0:
							zero_time_ls.append(index)
						else:
							end_seq = index
							streams_ls.append(stream)
							patterns_ls.append(pattern)
							start_times_ls.append(start_seq)
							end_times_ls.append(end_seq)
							location_ls.append(location)
							door_status_ls.append(door_status)

						# Determine stream type, pattern, and target location
						if any('traight stream' in row[test_name]):
							stream = 'SS'
						elif any('arrow fog' in row[test_name]):
							stream = 'NF'
						elif any('ide fog' in row[test_name]):
							stream = 'WF'
						
						# stores location, door status, pattern, and start time for next row
						if ' at ' in row[test_name]:
							location = row[test_name].split(' at ')[1]

						if 'door closed' in row[test_name]:
							door_status = 'C'

						if 'door opened' in row[test_name]:
							door_status = 'O'
							
						if any('ixed' in row[test_name]):
							pattern = 'fixed'
						elif any('rotated right' in row[test_name]):
							pattern = 'CW'
						elif any('rotated left' in row[test_name]):
							pattern = 'CCW'
						
						start_seq = index

						if 'flow stopped' in row[test_name]:
							start_seq = 0

				group_set = {'Start': start_times_ls, 'End':end_times_ls, 'Stream':streams_ls, 'Pattern':patterns_ls,
				'Location':location_ls, 'Door':door_status_ls}
				group_results = pd.DataFrame(group_set, columns = ['Start', 'End', 'Stream', 'Pattern', 'Location', 'Door'])
				
				# create empty df to fill with desired channel data
				start_data = group_results['Start'].iloc[0] - 25
				end_data = group_results['End'].iloc[-1]
				group_data = pd.DataFrame(data['Time'].iloc[0:end_data], columns = ['Time'])

				for channel in data.columns[1:]:
					# Skip excluded channels listed in hose_info file
					if any([substring in channel for substring in hose_info['Excluded Channels'][test_name].split('|')]):
						continue

					if any([substring in channel for substring in group]):
						# calculate initial zero voltage, create empty list for calculated velocities
						zero_start = zero_time_ls[0] - 25
						zero_end = zero_time_ls[0] - 5
						zero_voltage = np.mean(data[channel][zero_start:zero_end])
						i = 1
						quantity = []
						# convert voltages to velocities
						for index, row in data.iloc[0:end_data].iterrows():
							# check if zero voltage needs to be re-calculated
							if (zero_time_ls[i] - 25) == row['Time']:
								zero_start = int(row['Time'])
								zero_end = zero_start + 20
								zero_voltage = np.mean(data[channel][zero_start:zero_end])
								# iterate i if additional zero voltage will be calculated
								if i < (len(zero_time_ls)-1):
									i += 1
						
							pressure = conv_inch_h2o * conv_pascal * (row[channel] - zero_voltage)
							quantity.append(0.0698 * np.sqrt(np.abs(pressure) * (row['TC_' + channel[4:]] + 273.15)) * np.sign(pressure))
							
						# add velocities to group_data df and add a column for channel to group_results df
						group_data[channel] = quantity
						group_results[channel] = ''
						print ' Added data for ' + channel

				# calculate channel avg at each second and add to group_data
				channel_avg = []
				for index, row in group_data.iterrows():
					channel_avg.append(np.mean(row[1:]))
				group_data['Avg'] = channel_avg
				print ' Calculated average of all channels'		

				###########################################################################
				# uncomment to produce .csv result files with channel avgs for each event #
				###########################################################################
				group_results['Avg'] = ''
				for index, row in group_results.iterrows():
					# grab start/end time for each event in new .csv file
					start = row['Start']
					end = row['End']
					seq_data = group_data.iloc[start:end]

					# Calculate average for each channel during sequence
					for column in group_results.columns[6:]:
						# calculate avg for each channel during event 
						group_results.loc[index, column] = round(np.mean(seq_data[column]), 2)

				# Saves results .csv file for sensor group
				group_results.to_csv(results_dir + test_name + '_' + str(group)[2:-2]  + 'averages.csv')
				print 'Saving ' + test_name + '_' + str(group)[2:-2]  + 'Averages'
				print

				############
				# Plotting #
				############
				# set new figure, figure name; re-set y min and max
				fig = figure()
				y_min = 0
				y_max = 0
				t = group_data['Time']
				ylabel('Velocity (m/s)', fontsize=20)
				line_style = '-'
				axis_scale = 'Y Scale BDP'

				#############################################
				# uncomment to plot individual channel data #
				#############################################
				# Plot style - colors and markers
				# These are the "Tableau 20" colors as RGB.
				tableau20 = [(31, 119, 180), (174, 199, 232), (255, 127, 14), (255, 187, 120),
					(44, 160, 44), (152, 223, 138), (214, 39, 40), (255, 152, 150),
					(148, 103, 189), (197, 176, 213), (140, 86, 75), (196, 156, 148),
					(227, 119, 194), (247, 182, 210), (127, 127, 127), (199, 199, 199),
					(188, 189, 34), (219, 219, 141), (23, 190, 207), (158, 218, 229)]

				# Scale the RGB values to the [0, 1] range, which is the format matplotlib accepts.
				for i in range(len(tableau20)):
					r, g, b = tableau20[i]
					tableau20[i] = (r / 255., g / 255., b / 255.)
				plt.rc('axes', color_cycle=tableau20)
				plot_markers = cycle(['s', 'o', '^', 'd', 'h', 'p','v','8','D','*','<','>','H'])
				fig_name = fig_dir + test_name + '_' + group[0].rstrip('_') + '.pdf'

				for channel in group_data.columns[1:-1]:
					quantity = group_data[channel]

					# check y min and max
					ma_quantity = movingaverage(quantity,5)
					q_max = max(ma_quantity)
					q_min = min(ma_quantity)
					if q_max > y_max:
						y_max = q_max
					if q_min < y_min:
						y_min = q_min

					plot(t, ma_quantity, lw=1.5, ls=line_style, label=scaling['Test Specific Name'][channel])
					print ' Plotting channel ' + channel


				#############################################
				# uncomment to plot average of all channels #
				#############################################
				# fig_name = fig_dir + test_name + '_' + group[0].rstrip('_') + '_avg.pdf'

				# quantity = group_data['Avg']
				# ma_quantity = movingaverage(quantity, 5)
				# y_max = max(ma_quantity)
				# y_min = min(ma_quantity)

				# plot(t, ma_quantity, lw=1.5, ls=line_style, label=group_results.columns[6:-1], color = 'b')


			# Set axis options, legend, tickmarks, etc.
			ax1 = gca()
			xlim([0, end_of_test - start_of_test])
			ylim(floor(y_min), ceil(y_max))
			ax1.xaxis.set_major_locator(MaxNLocator(8))
			ax1_xlims = ax1.axis()[0:2]
			# grid(True)
			axhline(0, color='0.50', lw=1)
			xlabel('Time', fontsize=20)
			xticks(fontsize=16)
			yticks(arange(floor(y_min), ceil(y_max)+1, 1), fontsize=16)
			legend(loc='lower right', fontsize=8)

			try:
				# Add vertical lines for timing information (if available)
				for index, row in timings.iterrows():
					if pd.isnull(row[test_name]):
						continue
					axvline(index - start_of_test, color='0.50', lw=1)

				# Add secondary x-axis labels for timing information
				ax2 = ax1.twiny()
				ax2.set_xlim(ax1_xlims)
				ax2.set_xticks(timings[test_name].dropna().index.values - start_of_test)
				setp(xticks()[1], rotation=60)
				ax2.set_xticklabels(timings[test_name].dropna().values, fontsize=8, ha='left')
				xlim([0, end_of_test - start_of_test])

				# Increase figure size for plot labels at top
				fig.set_size_inches(12, 9)
			except:
				pass

			# Save plot to file
			print 'Saving plot for ', group
			print
			savefig(fig_name)
			close('all')

######################################################################
# uncomment to print latex code for tables containing average values #
######################################################################
print
print '#######################'
print '# West Handline Table #'
print '#######################'
print
print '\\begin{table}[!ht]'
print '\\caption{' + west_hand_caption + '}'
print '\\begin{tabular}{lcccc}'
print '\\toprule'
print ' & \\multicolumn{4}{c}{\\underline{Test 18}}'
print '\\\\'
print ' & '.join(str(column) for column in west_hand_columns)
print '\\\ \\midrule'
for index in streams:
	print stream_ls[index] + ' & ' + fixed_18[index] + ' & ' + sweep_18[index] + ' & ' + CW_18[index] + ' & ' + CCW_18[index]
	if index == 'WF':
		print '\\\ \\midrule'
	else:
		print '\\\ \\multicolumn{5}{c}{} \\\\'
print ' & \\multicolumn{4}{c}{\\underline{Test 19}}'
print '\\\\'
print ' & '.join(str(column) for column in west_hand_columns)
print '\\\ \\midrule'
for index in streams:
	print stream_ls[index] + ' & ' + fixed_19[index] + ' & ' + sweep_19[index] + ' & ' + CW_19[index] + ' & ' + CCW_19[index]
	if index == 'WF':
		print '\\\ \\bottomrule'
	else:
		print '\\\ \\multicolumn{5}{c}{} \\\\'
print '\\end{tabular}'
print '\\label{' + west_hand_label + '}'
print '\\end{table}'
print




