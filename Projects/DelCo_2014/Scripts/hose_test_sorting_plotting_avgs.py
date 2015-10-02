#!/usr/bin/env python

import os
import collections
import numpy as np
import pandas as pd
from pylab import *
import math
import inspect
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
sensor_groups = [['BDP_A6_'], ['BDP_A10_']]
# sensor_groups = [['TC_A1_'], ['TC_A2_'], ['TC_A3_'], ['TC_A4_'], ['TC_A5_'],
#                  ['TC_A6_'], ['TC_A7_'], ['TC_A8_'], ['TC_A9_'], ['TC_A10_'],
#                  ['TC_A11_'], ['TC_A12_'], ['TC_A13_'], ['TC_A14_'], ['TC_A15_'],
#                  ['TC_A16_'], ['TC_A17_'], ['TC_A18_'], ['TC_A19_'],
#                  ['TC_Ignition'],
#                  ['TC_Helmet_'],
#                  ['BDP_A4_'], ['BDP_A5_'], ['BDP_A6_'], ['BDP_A7_'],
#                  ['BDP_A8_'], ['BDP_A9_'], ['BDP_A10_'], ['BDP_A11_'],
#                  ['BDP_A12_'], ['BDP_A13_'], ['BDP_A14_'], ['BDP_A15_'],
#                  ['BDP_A18_'],
#                  ['HF_', 'RAD_'],
#                  ['GAS_', 'CO_', 'CO2_', 'O2_'],
#                  ['HOSE_']]

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

# ============================================
# Execute or skip specific parts of the code =
# ============================================

result_file = False			# Generate a .csv file with channel avgs for specified sensor groups
plotting = True	  			# Generate any plot?
all_channel_plot = False	# Plot individual channels
group_avg_plot = False		# Plot sensor group avgs

monitor_avgs_plot = True	# Plot BDP avgs from monitor experiments for SS, NF, WF application
west_monitor_labels = ['Hose on, near target', 'Stairwell door opened', '2nd floor, W door opened', 'Doors closed',
'Hose on, far target', 'Stairwell door opened', '2nd floor, W door opened', 'Doors closed']

handline_avgs_plot = False 	# Plot BDP avgs from handline experiments for SS, NF, WF application
west_handline_labels = ['Hose on, fixed', 'Stairwell door opened', '2nd floor, W door opened', 'Doors closed',
'Hose on, sweeping', 'Stairwell door opened', '2nd floor, W door opened', 'Doors closed', 'Hose on, rotate CW', 'Stairwell door opened', 
'2nd floor, W door opened', 'Doors closed', 'Hose on, rotate CCW', 'Stairwell door opened', '2nd floor, W door opened', 'Doors closed',]

latex_table_code = False    # Print code to generate tables in LaTeX?
if(latex_table_code):		# specify table properties (if applicable)
	# Create lists for column titles for desired latex tables
	streams = ['SS', 'NF', 'WF']
	stream_ls = pd.Series(['\\textit{Straight}', '\\textit{Narrow Fog}', '\\textit{Wide Fog}'], index = streams)

	# West handline table
	west_hand_caption = ('Average air velocity (m/s) through stairwell door with fully established flow path '
		'for stream and application pattern combinations during Tests 18 and 19')
	west_hand_label = 'table:west_hand_A10_avgs'
	west_hand_columns = ['\\textbf{Stream}', '\\textbf{Fixed}', '\\textbf{Sweeping}', '\\textbf{Clockwise}', 
		'\\begin{tabular}{@{}c@{}} \\textbf{Counter} \\\ \\textbf{Clockwise} \\\ \\end{tabular}']

	# West monitor table
	west_mon_caption = ('Average air velocity (m/s) through stairwell door with fully established flow path '
		'for stream and target location for all monitor tests')
	west_mon_label = 'table:all_mon_vel_avgs'
	west_mon_columns = ['\\textbf{Stream}', '\\textbf{Near}', '\\textbf{Far}', '\\textbf{Near}', '\\textbf{Far}', '\\textbf{Door AB}']

	# East handline table
	east_hand_caption = ('Average air velocity (m/s) through A6 with established flow path for the stream and application pattern '
		'combinations at each target (Room A and ceiling of Room B) during Test 34') 
	east_hand_label = 'table:east_hand_A6_avgs'
	east_hand_columns = ['\\textbf{Stream}', '\\textbf{Fixed}', '\\textbf{Clockwise}', 
		'\\begin{tabular}{@{}c@{}} \\textbf{Counter} \\\ \\textbf{Clockwise} \\\ \\end{tabular}', '\\textbf{Fixed}', 
		'\\textbf{Clockwise}', '\\begin{tabular}{@{}c@{}} \\textbf{Counter} \\\ \\textbf{Clockwise} \\\ \\end{tabular}']

	# East monitor table
	# east monitor data currently included in west monitor table #

#  ==================
#  = User functions =
#  ==================

# Allows printing of line number in code for custom printed error messages
def lineno():
    return inspect.currentframe().f_back.f_lineno

def save_plot(x_max_index, y_max, y_min, start_time, end_time, group, fig_name, plot_type):
	plt.errorbar(x_max_index, y_max, yerr=(.18)*y_max, ecolor='k')
	# Set axis options, legend, tickmarks, etc.
	ax1 = gca()
	y_tick_ls = []
	y_label_ls = []
	xlim([0, end_time])
	ylim(floor(y_min)-0.1, ceil(y_max)+0.1)
	ax1.xaxis.set_major_locator(MaxNLocator(8))
	# ax1_xlims = ax1.axis()[0:2]
	# grid(True)
	axhline(0, color='0.50', lw=1)
	xlabel('Time (s)', fontsize=20)
	xticks(fontsize=16)
	y_tick_ls = arange(floor(y_min), ceil(1.18*y_max)+1, 1)
	yticks(np.around(y_tick_ls,1), fontsize=16)

	ax2 = ax1.twinx()
	ax2.set_ylabel('Velocity (mph)', fontsize=20)
	plt.xticks(fontsize=16)
	ylim(floor(y_min)-0.1, ceil(y_max)+0.1)
	yticks(y_tick_ls, fontsize=16)
	y_label_ls = np.array(y_tick_ls) * 2.23694
	ax2.set_yticklabels(np.around(y_label_ls, 1))

	try:
		# Add vertical lines for timing information (if available)
		if plot_type != 'west monitor':
			x_ticks_ls = []
			for index, row in timings.iterrows():
				if pd.isnull(row[test_name]) or (index-start_time > end_time):
					continue
				axvline(index - start_time, color='0.50', lw=1)
				x_ticks_ls.append(index-start_time)

			# Add secondary x-axis labels for timing information
			ax3 = ax1.twiny()
			ax3.set_xlim([0, end_time])
			ax3.set_xticks(x_ticks_ls)
			setp(xticks()[1], rotation=60)
			if plot_type == 'west handline':
				ax3.set_xticklabels(west_handline_labels, fontsize=10, ha='left')	
			else:
				x3.set_xticklabels(timings[test_name].dropna().values, fontsize=10, ha='left')

		else:		# cheat for now and manually set tick marks, vertically lines for Tests 16, 17
			x_ticks_ls = [0,60,120,180,240,300,360,420]
			for value in x_ticks_ls:
				axvline(value, color='0.50', lw=1)

			# Add secondary x-axis labels for timing information
			ax3 = ax1.twiny()
			ax3.set_xlim([0, end_time])
			ax3.set_xticks(x_ticks_ls)
			setp(xticks()[1], rotation=60)
			ax3.set_xticklabels(west_monitor_labels, fontsize=10, ha='left')		

		# Increase figure size for plot labels at top
		fig.set_size_inches(8,8)
	except:
		pass

	gca().add_artist(ax1.legend(loc='lower right', fontsize=10, frameon = True))

	# Save plot to file
	print 'Saving plot for ', group
	print
	savefig(fig_name)
	close('all')

#  ===============================
#  = Loop through all data files =
#  ===============================

# Convert voltage to pascals
conv_inch_h2o = 0.4
conv_pascal = 248.8

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
				###########
				# Sorting #
				###########

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

				# calculate channel avg at each second and add to group_data
				channel_avg = []
				for index, row in group_data.iterrows():
					channel_avg.append(np.mean(row[1:]))
				group_data['Avg'] = channel_avg			

				if(result_file):
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

				if(latex_table_code):
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
							print '[ERROR, line '+lineno()+']:' 
							print 'Test is not a west handline test:'
							print 'Test = ' + test_name
							sys.exit()

					# Monitor
					else:
						near_ls = pd.Series(range(3), index = streams)
						far_ls = pd.Series(range(3), index = streams)
						# if-else due to flowrate of WF dropping during Test 17, so Test 17b was performed for WF at proper flowrate 
						if 'Test_17' not in test_name:
							for index, row in group_results.iterrows():
								if row['Door'] == 'BC open':
									start = row['Start']
									end = row['End']
									seq_data = group_data.iloc[start:end]
									if row['Location'] == 'Near':
										near_ls[row['Stream']] = str(round(np.mean(seq_data['Avg']), 1)) + ' $\pm' + str(round(np.std(seq_data['Avg']), 1)) + '$'
									elif row['Location'] == 'Far':
										far_ls[row['Stream']] = str(round(np.mean(seq_data['Avg']), 1)) + ' $\pm' + str(round(np.std(seq_data['Avg']), 1)) + '$'
									else:
										print '[ERROR, line '+lineno()+']:'
										print 'Read row[Door] as "BC open" but row[Location] is not a valid input'
										print 'row[Location] = ' + row['Location']
										sys.exit()
								else:
									continue
							near_16 = near_ls
							far_16 = far_ls

						else:
							if 'Test_17b' in test_name:
								for index, row in group_results.iterrows():
									if row['Door'] == 'BC open':
										start = row['Start']
										end = row['End']
										seq_data = group_data.iloc[start:end]
										if row['Location'] == 'Near':
											near_17_WF = str(round(np.mean(seq_data['Avg']), 1)) + ' $\pm' + str(round(np.std(seq_data['Avg']), 1)) + '$'
										elif row['Location'] == 'Far':
											far_17_WF = str(round(np.mean(seq_data['Avg']), 1)) + ' $\pm' + str(round(np.std(seq_data['Avg']), 1)) + '$'
										else:
											print '[ERROR, line '+lineno()+']:'
											print 'Read row[Door] as "BC open" but row[Location] is not a valid input'
											print 'row[Location] = ' + row['Location']
											sys.exit()
									else:
										continue

							else:
								for index, row in group_results.iterrows():
									if row['Door'] == 'BC open':
										start = row['Start']
										end = row['End']
										seq_data = group_data.iloc[start:end]
										if row['Location'] == 'Near':
											near_ls[row['Stream']] = str(round(np.mean(seq_data['Avg']), 1)) + ' $\pm' + str(round(np.std(seq_data['Avg']), 1)) + '$'
										elif row['Location'] == 'Far':
											far_ls[row['Stream']] = str(round(np.mean(seq_data['Avg']), 1)) + ' $\pm' + str(round(np.std(seq_data['Avg']), 1)) + '$'
										else:
											print '[ERROR, line '+lineno()+']:'
											print 'Read row[Door] as "BC open" but row[Location] is not a valid input'
											print 'row[Location] = ' + row['Location']
											sys.exit()
									else:
										continue

								near_17 = near_ls
								far_17 = far_ls

				############
				# Plotting #
				############
				if (plotting):
					y_min = 0
					y_max = 0
					start_plot = group_results['Start'].iloc[0]
					end_plot = end_data
					plot_data = group_data.iloc[start_plot:end_plot]
					t = range(0, len(plot_data['Time']))

					if(all_channel_plot):
						fig = plt.figure()
						ylabel('Velocity (m/s)', fontsize=20)
						line_style = '-'
						axis_scale = 'Y Scale BDP'
						fig_name = fig_dir + test_name + '_' + group[0].rstrip('_') + '.pdf'

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

						for channel in plot_data.columns[1:-1]:
							quantity = plot_data[channel]

							# check y min and max
							ma_quantity = pd.rolling_mean(quantity, 5)
							ma_quantity = ma_quantity.fillna(method='bfill')
							q_max = max(ma_quantity)
							q_min = min(ma_quantity)
							if q_max > y_max:
								y_max = q_max
								x_max_index = plot_data['Time'][ma_quantity.idxmax(y_max)]-start_plot
							if q_min < y_min:
								y_min = q_min

							plt.plot(t, ma_quantity, 
								marker=next(plot_markers), markevery=int((end_plot - start_plot)/10), mew=1.5, mec='none', ms=7, 
								lw=1.5, ls=line_style, label=scaling['Test Specific Name'][channel])
							print ' Plotting channel ' + channel

						save_plot(x_max_index, y_max, y_min, start_plot, end_plot, group, fig_name, 'all channels')
						y_min = 0
						y_max = 0

					if(group_avg_plot):
						fig = figure()
						ylabel('Velocity (m/s)', fontsize=20)
						line_style = '-'
						axis_scale = 'Y Scale BDP'
						fig_name = fig_dir + test_name + '_' + group[0].rstrip('_') + '_avg.pdf'
						plot_markers = cycle(['s', 'o', '^', 'd', 'h', 'p','v','8','D','*','<','>','H'])

						quantity = plot_data['Avg']
						ma_quantity = pd.rolling_mean(quantity, 5)
						ma_quantity = ma_quantity.fillna(method='bfill')
						y_max = max(ma_quantity)
						y_min = min(ma_quantity)

						plt.plot(t, ma_quantity, 
							marker=next(plot_markers), markevery=int((end_plot - start_plot)/10), mew=1.5, mec='none', ms=7, 
							lw=1.5, ls=line_style, label=scaling['Test Specific Name'][channel])

						save_plot(x_max_index, y_max, y_min, start_plot, end_plot, group, fig_name, 'group avgs')
						y_min = 0
						y_max = 0

					if P_or_L_heading == 'Pattern':
						if(handline_avgs_plot):
							fig = plt.figure()
							ylabel('Velocity (m/s)', fontsize=20)
							line_style = '-'
							axis_scale = 'Y Scale BDP'
							fig_name = fig_dir + test_name + '_' + group[0].rstrip('_') + '_stream_avgs.pdf'

							plot_markers = cycle(['s', 'o', '^', 'd', 'h', 'p','v','8','D','*','<','>','H'])

							for index, row in group_results.iterrows():
								if row['Pattern'] == 'fixed' and row['Door'] == 'All closed':
									start_pattern = row['Start']
									stream = row['Stream']
								elif row['Pattern'] == 'CCW' and row['Door'] == 'BC open':
									end_pattern = row['End']
									# Calculate moving average and plot sequence
									quantity = plot_data['Avg'].iloc[start_pattern:end_pattern]
									ma_quantity = pd.rolling_mean(quantity, 5)
									ma_quantity = ma_quantity.fillna(method='bfill')

									q_max = max(ma_quantity)
									q_min = min(ma_quantity)
									if q_max > y_max:
										y_max = q_max
										x_max_index = plot_data['Time'][ma_quantity.idxmax(y_max)]-SS_near1_start
									if q_min < y_min:
										y_min = q_min

									if stream == 'SS':
										color = 'k'
									elif stream == 'NF':
										color = 'b'
									elif stream == 'WF':
										color = 'r'

									t = range(0, len(ma_quantity))

									plot(t, ma_quantity, 
										marker=next(plot_markers), markevery=int((len(t))/10), 
										mew=1.5, mec='none', ms=7, lw=1.5, ls=line_style, color = color,
										label=stream+' '+group[0].rstrip('_')+' Average')
								else:
									continue

							save_plot(x_max_index, y_max, y_min, start_plot, len(t), group, fig_name, 'west handline')
							y_min = 0
							y_max = 0

					if(monitor_avgs_plot):
						# if Test 16, plot immediately
						if 'Test_16' in test_name:
							fig = plt.figure()
							ylabel('Velocity (m/s)', fontsize=20)
							line_style = '-'
							axis_scale = 'Y Scale BDP'
							fig_name = fig_dir + test_name + '_' + group[0].rstrip('_') + '_stream_avgs.pdf'

							plot_markers = cycle(['s', 'o', '^', 'd', 'h', 'p','v','8','D','*','<','>','H'])

							# fill the start and end times for all sequences to be plotted
							for index, row in group_results.iterrows():
								if row['Door'] == 'All closed':		# start of a sequence
									if row['Location'] == 'Near':
										if row['Stream'] == 'SS':
											SS_near1_start = row['Start']
										elif row['Stream'] == 'NF':
											NF_near_start = row['Start']
										elif row['Stream'] == 'WF':
											WF_start = row['Start']
									elif row['Location'] == 'Far':
										if row['Stream'] == 'SS':
											SS_far_start = row['Start']-60
										elif row['Stream'] == 'NF':
											NF_far1_start = row['Start']-60
										else:
											continue

								elif row['Door'] == 'A open':	# door A was opened
									if row['Stream'] == 'SS':
										SS_near1_end = row['Start']
									elif row['Stream'] == 'NF':
										NF_far1_end = row['Start']
									else:
										print '[ERROR, line '+lineno()+']:'
										print 'Read row[Door] as "A open" but stream and location not valid combo'
										print 'Door, stream, location = '+row['Door']+', '+row['Stream']+', '+row['Location'] 
										sys.exit()

								elif row['Door'] == 'BC open':	# end of a sequence
									if row['Stream'] == 'SS':	# (and beginning Door A being closed if opened previously)
										if row['Location'] == 'Near':
											SS_near2_start = row['Start']
											SS_near2_end = row['End']
										elif row['Location'] == 'Far':
											SS_far_end = row['End']
										else:
											print '[ERROR, line '+lineno()+']:'
											print row
											sys.exit()
									elif row['Stream'] == 'NF':
										if row['Location'] == 'Near':
											NF_near_end = row['End']
										elif row['Location'] == 'Far':
											NF_far2_start = row['Start']
											NF_far2_end = row['End']
										else:
											print '[ERROR, line '+lineno()+']:'
											print row
											sys.exit()
									elif row['Stream'] == 'WF':
										if row['Location'] == 'Far':
											WF_end = row['End']
										else:
											continue

							# create lists for SS, NF, WF data

							SS_total = pd.concat([group_data['Avg'].iloc[SS_near1_start:SS_near1_end],
								group_data['Avg'].iloc[SS_near2_start:SS_near2_end],
								group_data['Avg'].iloc[SS_far_start:SS_far_end]])

							NF_total = pd.concat([group_data['Avg'].iloc[NF_near_start:NF_near_end],
								group_data['Avg'].iloc[NF_far1_start:NF_far1_end],
								group_data['Avg'].iloc[NF_far2_start:NF_far2_end]])

							WF_total = group_data['Avg'].iloc[WF_start:WF_end]

							test_16_plot = pd.DataFrame({'SS':SS_total.values,
							 	'NF':NF_total.values, 'WF':WF_total.values}, columns=['SS', 'NF', 'WF'])

							for stream_type in test_16_plot.columns[:]:
								if stream_type == 'SS':
									color = 'k'
								elif stream_type == 'NF':
									color = 'b'
								elif stream_type == 'WF':
									color = 'r'
								else:
									continue

								# Calculate moving average and plot stream data
								quantity = test_16_plot[stream_type]
								ma_quantity = pd.rolling_mean(quantity, 5)
								ma_quantity = ma_quantity.fillna(method='bfill')

								q_max = max(ma_quantity)
								q_min = min(ma_quantity)
								if q_max > y_max:
									y_max = q_max
									x_max_index = ma_quantity.idxmax(y_max)
								if q_min < y_min:
									y_min = q_min

								t = range(0, len(ma_quantity))

								plot(t, ma_quantity, 
									marker=next(plot_markers), markevery=int((len(t))/10), 
									mew=1.5, mec='none', ms=7, lw=1.5, ls=line_style, color = color,
									label=stream_type+' '+group[0].rstrip('_')+' Average')

							save_plot(x_max_index, y_max, y_min, start_plot, len(t), group, fig_name, 'west monitor')
							y_min = 0
							y_max = 0

						# if Test 17 or 17b create series to plot at end of script
						elif 'Test_17_' in test_name:
							# create figure name to reference when plotting at end of script
							fig_name_test_17_avgs = fig_dir + test_name + '_' + group[0].rstrip('_') + '_stream_avgs.pdf'
							group_test_17 = group

							for index, row in group_results.iterrows():
								if row['Stream'] == 'WF':		# skip WF due to pressure drop
									continue
								elif row['Door'] == 'All closed' and row['Location'] == 'Near':
									if row['Stream'] == 'SS':
										test_17_SS_start = row['Start']
									elif row['Stream'] == 'NF':
										test_17_NF_start = row['Start']
									else:
										print '[ERROR, line '+lineno()+']:'
										sys.exit()
								elif row['Door'] == 'BC open' and row['Location'] == 'Far':
									if row['Stream'] == 'SS':
										test_17_SS_end = row['End']
									elif row['Stream'] == 'NF':
										test_17_NF_end = row['End']
									else:
										print '[ERROR, line '+lineno()+']:'
										sys.exit()
								else:
									continue

							test_17_SS = group_data['Avg'].iloc[test_17_SS_start:test_17_SS_end]
							test_17_NF = group_data['Avg'].iloc[test_17_NF_start:test_17_NF_end]

						elif 'Test_17b' in test_name:
							for index, row in group_results.iterrows():
								if row['Door'] == 'All closed' and row['Location'] == 'Near':
									test_17_WF_start = row['Start']
								elif row['Door'] == 'BC open' and row['Location'] == 'Far':
									test_17_WF_end = row['End']
								else:
									continue

							test_17_WF = group_data['Avg'].iloc[test_17_WF_start:test_17_WF_end]					

			# # East Tests Sorting/Plotting
			# else:
			# 	###########
			# 	# Sorting #
			# 	###########

			# 	# initialize lists and start_seq value
			# 	start_seq = 0
			# 	door_status = 'C'
			# 	streams_ls = []
			# 	patterns_ls = []		
			# 	start_times_ls = []
			# 	end_times_ls = []
			# 	location_ls = []
			# 	door_status_ls = []
			# 	zero_time_ls = []

			# 	# gathers timing information from hose_times file
			# 	for index, row in timings.iterrows():
			# 		if pd.isnull(row[test_name]):
			# 			continue

			# 		else:
			# 			# mark event start time or add event info to lists
			# 			if start_seq == 0:
			# 				zero_time_ls.append(index)
			# 			else:
			# 				end_seq = index
			# 				streams_ls.append(stream)
			# 				patterns_ls.append(pattern)
			# 				start_times_ls.append(start_seq)
			# 				end_times_ls.append(end_seq)
			# 				location_ls.append(location)
			# 				door_status_ls.append(door_status)

			# 			# Determine stream type, pattern, and target location
			# 			if any('traight stream' in row[test_name]):
			# 				stream = 'SS'
			# 			elif any('arrow fog' in row[test_name]):
			# 				stream = 'NF'
			# 			elif any('ide fog' in row[test_name]):
			# 				stream = 'WF'
						
			# 			# stores location, door status, pattern, and start time for next row
			# 			if ' at ' in row[test_name]:
			# 				location = row[test_name].split(' at ')[1]

			# 			if 'door closed' in row[test_name]:
			# 				door_status = 'C'

			# 			if 'door opened' in row[test_name]:
			# 				door_status = 'O'
							
			# 			if any('ixed' in row[test_name]):
			# 				pattern = 'fixed'
			# 			elif any('rotated right' in row[test_name]):
			# 				pattern = 'CW'
			# 			elif any('rotated left' in row[test_name]):
			# 				pattern = 'CCW'
						
			# 			start_seq = index

			# 			if 'flow stopped' in row[test_name]:
			# 				start_seq = 0

			# 	group_set = {'Start': start_times_ls, 'End':end_times_ls, 'Stream':streams_ls, 'Pattern':patterns_ls,
			# 	'Location':location_ls, 'Door':door_status_ls}
			# 	group_results = pd.DataFrame(group_set, columns = ['Start', 'End', 'Stream', 'Pattern', 'Location', 'Door'])
				
			# 	# create empty df to fill with desired channel data
			# 	start_data = group_results['Start'].iloc[0] - 25
			# 	end_data = group_results['End'].iloc[-1]
			# 	group_data = pd.DataFrame(data['Time'].iloc[0:end_data], columns = ['Time'])

			# 	for channel in data.columns[1:]:
			# 		# Skip excluded channels listed in hose_info file
			# 		if any([substring in channel for substring in hose_info['Excluded Channels'][test_name].split('|')]):
			# 			continue

			# 		if any([substring in channel for substring in group]):
			# 			# calculate initial zero voltage, create empty list for calculated velocities
			# 			zero_start = zero_time_ls[0] - 25
			# 			zero_end = zero_time_ls[0] - 5
			# 			zero_voltage = np.mean(data[channel][zero_start:zero_end])
			# 			i = 1
			# 			quantity = []
			# 			# convert voltages to velocities
			# 			for index, row in data.iloc[0:end_data].iterrows():
			# 				# check if zero voltage needs to be re-calculated
			# 				if (zero_time_ls[i] - 25) == row['Time']:
			# 					zero_start = int(row['Time'])
			# 					zero_end = zero_start + 20
			# 					zero_voltage = np.mean(data[channel][zero_start:zero_end])
			# 					# iterate i if additional zero voltage will be calculated
			# 					if i < (len(zero_time_ls)-1):
			# 						i += 1
						
			# 				pressure = conv_inch_h2o * conv_pascal * (row[channel] - zero_voltage)
			# 				quantity.append(0.0698 * np.sqrt(np.abs(pressure) * (row['TC_' + channel[4:]] + 273.15)) * np.sign(pressure))
							
			# 			# add velocities to group_data df and add a column for channel to group_results df
			# 			group_data[channel] = quantity
			# 			group_results[channel] = ''
			# 			print ' Added data for ' + channel

			# 	# calculate channel avg at each second and add to group_data
			# 	channel_avg = []
			# 	for index, row in group_data.iterrows():
			# 		channel_avg.append(np.mean(row[1:]))
			# 	group_data['Avg'] = channel_avg
			# 	print ' Calculated average of all channels'		

			# 	if(result_file):
			# 		group_results['Avg'] = ''
			# 		for index, row in group_results.iterrows():
			# 			# grab start/end time for each event in new .csv file
			# 			start = row['Start']
			# 			end = row['End']
			# 			seq_data = group_data.iloc[start:end]

			# 			# Calculate average for each channel during sequence
			# 			for column in group_results.columns[6:]:
			# 				# calculate avg for each channel during event 
			# 				group_results.loc[index, column] = round(np.mean(seq_data[column]), 2)

			# 		# Saves results .csv file for sensor group
			# 		group_results.to_csv(results_dir + test_name + '_' + str(group)[2:-2]  + 'averages.csv')
			# 		print 'Saving ' + test_name + '_' + str(group)[2:-2]  + 'Averages'
			# 		print

			# 	if(latex_table_code):
			# 		# Handline
			# 		if test_name[7] == 'A':
			# 			# multiple 30 second increments of fixed streams, create list to store all data for each fixed stream
			# 			# and location combination and calc avgs at end
			# 			raw_fix_A_SS = []
			# 			raw_fix_A_NF = []
			# 			raw_fix_A_WF = []
			# 			raw_fix_B_SS = []
			# 			raw_fix_B_NF = []
			# 			raw_fix_B_WF = []
			# 			fixed_A = pd.Series(range(3), index = streams)
			# 			fixed_B = pd.Series(range(3), index = streams)
			# 			CW_A = pd.Series(range(3), index = streams)
			# 			CW_B = pd.Series(range(3), index = streams)
			# 			CCW_A = pd.Series(range(3), index = streams)
			# 			CCW_B = pd.Series(range(3), index = streams)

			# 			for index, row in group_results.iterrows():
			# 				start = row['Start']
			# 				end = row['End']
			# 				seq_data = group_data.iloc[start:end]
			# 				if row['Location'] == 'Room A':
			# 					if row['Pattern'] == 'fixed':
			# 						if row['Stream'] == 'SS':
			# 							raw_fix_A_SS.append(seq_data['Avg'])
			# 						elif row['Stream'] == 'NF':
			# 							raw_fix_A_NF.append(seq_data['Avg'])
			# 						elif row['Stream'] == 'WF':
			# 							raw_fix_A_WF.append(seq_data['Avg'])
			# 					elif row['Pattern'] == 'CW':
			# 						CW_A[row['Stream']] = str(round(np.mean(seq_data['Avg']), 1)) + ' $\pm' + str(round(np.std(seq_data['Avg']), 1)) + '$'
			# 					elif row['Pattern'] == 'CCW':
			# 						CCW_A[row['Stream']] = str(round(np.mean(seq_data['Avg']), 1)) + ' $\pm' + str(round(np.std(seq_data['Avg']), 1)) + '$'
			# 					else:
			# 						print '[ERROR, line '+lineno()+']:'
			# 						print 'Read "Room A" as location, invalid row[Pattern] input'
			# 						print 'row[Pattern] = ' + row['Pattern']
			# 						sys.exit()
			# 				elif 'Room B' in row['Location']:
			# 					if row['Pattern'] == 'fixed':
			# 						if row['Stream'] == 'SS':
			# 							raw_fix_B_SS.append(seq_data['Avg'])
			# 						elif row['Stream'] == 'NF':
			# 							raw_fix_B_NF.append(seq_data['Avg'])
			# 						elif row['Stream'] == 'WF':
			# 							raw_fix_B_WF.append(seq_data['Avg'])
			# 					elif row['Pattern'] == 'CW':
			# 						CW_B[row['Stream']] = str(round(np.mean(seq_data['Avg']), 1)) + ' $\pm' + str(round(np.std(seq_data['Avg']), 1)) + '$'
			# 					elif row['Pattern'] == 'CCW':
			# 						CCW_B[row['Stream']] = str(round(np.mean(seq_data['Avg']), 1)) + ' $\pm' + str(round(np.std(seq_data['Avg']), 1)) + '$'
			# 					else:
			# 						print '[ERROR, line '+lineno()+']:'
			# 						print 'Read "Room B ceiling" as location, invalid row[Pattern] input'
			# 						print 'row[Pattern] = ' + row['Pattern']
			# 						sys.exit()
			# 				else:
			# 					continue
			# 			# Calculate fixed Series values
			# 			fixed_A['SS'] = str(round(np.mean(raw_fix_A_SS), 1)) + ' $\pm' + str(round(np.std(raw_fix_A_SS), 1)) + '$'
			# 			fixed_A['NF'] = str(round(np.mean(raw_fix_A_NF), 1)) + ' $\pm' + str(round(np.std(raw_fix_A_NF), 1)) + '$'
			# 			fixed_A['WF'] = str(round(np.mean(raw_fix_A_WF), 1)) + ' $\pm' + str(round(np.std(raw_fix_A_WF), 1)) + '$'
			# 			fixed_B['SS'] = str(round(np.mean(raw_fix_B_SS), 1)) + ' $\pm' + str(round(np.std(raw_fix_B_SS), 1)) + '$'
			# 			fixed_B['NF'] = str(round(np.mean(raw_fix_B_NF), 1)) + ' $\pm' + str(round(np.std(raw_fix_B_NF), 1)) + '$'
			# 			fixed_B['WF'] = str(round(np.mean(raw_fix_B_WF), 1)) + ' $\pm' + str(round(np.std(raw_fix_B_WF), 1)) + '$'

			# 		# monitor
			# 		else:
			# 			AB_33 = pd.Series(range(3), index = streams)
			# 			raw_SS = []
			# 			raw_NF = []
			# 			raw_WF = []
			# 			for index, row in group_results.iterrows():
			# 				if row['Door'] == 'C':
			# 					start = row['Start']
			# 					end = row['End']
			# 					seq_data = group_data.iloc[start:end]
			# 					if row['Stream'] == 'SS':
			# 						raw_SS.append(seq_data['Avg'])
			# 					elif row['Stream'] == 'NF':
			# 						raw_NF.append(seq_data['Avg'])
			# 					elif row['Stream'] == 'WF':
			# 						raw_WF.append(seq_data['Avg'])
			# 				else:
			# 					continue

			# 			AB_33['SS'] = str(round(np.mean(raw_SS), 1)) + ' $\pm' + str(round(np.std(raw_SS), 1)) + '$'
			# 			AB_33['NF'] = str(round(np.mean(raw_NF), 1)) + ' $\pm' + str(round(np.std(raw_NF), 1)) + '$'
			# 			AB_33['WF'] = str(round(np.mean(raw_WF), 1)) + ' $\pm' + str(round(np.std(raw_WF), 1)) + '$'

			# 	############
			# 	# Plotting #
			# 	############
			# 	if(plotting):
			# 		y_min = 0
			# 		y_max = 0
			# 		start_plot = group_results['Start'].iloc[0]
			# 		end_plot = end_data
			# 		plot_data = group_data.iloc[start_plot:end_plot]
			# 		t = range(0, len(plot_data['Time']))

			# 		if(all_channel_plot):
			# 			print '[ERROR, line '+lineno()+']:' 
			# 			print 'Need to rewrite this section'
			# 			sys.exit()
			# 			fig = plt.figure()
			# 			ylabel('Velocity (m/s)', fontsize=20)
			# 			line_style = '-'
			# 			axis_scale = 'Y Scale BDP'
			# 			fig_name = fig_dir + test_name + '_' + group[0].rstrip('_') + '.pdf'

			# 			# Plot style - colors and markers
		 #            	# These are the "Tableau 20" colors as RGB.
			# 			tableau20 = [(31, 119, 180), (174, 199, 232), (255, 127, 14), (255, 187, 120),
			# 				(44, 160, 44), (152, 223, 138), (214, 39, 40), (255, 152, 150),
			# 				(148, 103, 189), (197, 176, 213), (140, 86, 75), (196, 156, 148),
			# 				(227, 119, 194), (247, 182, 210), (127, 127, 127), (199, 199, 199),
			# 				(188, 189, 34), (219, 219, 141), (23, 190, 207), (158, 218, 229)]

			# 			# Scale the RGB values to the [0, 1] range, which is the format matplotlib accepts.
			# 			for i in range(len(tableau20)):
			# 				r, g, b = tableau20[i]
			# 				tableau20[i] = (r / 255., g / 255., b / 255.)
			# 			plt.rc('axes', color_cycle=tableau20)

			# 			plot_markers = cycle(['s', 'o', '^', 'd', 'h', 'p','v','8','D','*','<','>','H'])

			# 			for channel in group_data.columns[1:-1]:
			# 				quantity = group_data[channel]

			# 				# check y min and max
			# 				ma_quantity = pd.rolling_mean(quantity, 5)
			# 				ma_quantity = ma_quantity.fillna(method='bfill')
			# 				q_max = max(ma_quantity)
			# 				q_min = min(ma_quantity)
			# 				if q_max > y_max:
			# 					y_max = q_max
			# 					x_max_index = t[ma_quantity.idxmax(y_max)]
			# 				if q_min < y_min:
			# 					y_min = q_min

			# 				plot(t, ma_quantity, marker=next(plot_markers), lw=1.5, ls=line_style, label=scaling['Test Specific Name'][channel])
			# 				print ' Plotting channel ' + channel

			# 		elif(group_avg_plot):
			# 			print '[ERROR, line '+lineno()+']:' 
			# 			print 'Need to rewrite this section'
			# 			sys.exit()
			# 			fig_name = fig_dir + test_name + '_' + group[0].rstrip('_') + '_avg.pdf'

			# 			quantity = group_data['Avg']
			# 			ma_quantity = movingaverage(quantity, 5)
			# 			y_max = max(ma_quantity)
			# 			y_min = min(ma_quantity)

			# 			plot(t, ma_quantity, marker=next(plot_markers), lw=1.5, ls=line_style, label=group_results.columns[6:-1], color = 'b')

			# 		elif(handline_avgs_plot):
			# 			# Handline
			# 			if test_name[7] == 'A':
			# 				fig = plt.figure()
			# 				ylabel('Velocity (m/s)', fontsize=20)
			# 				line_style = '-'
			# 				axis_scale = 'Y Scale BDP'
			# 				fig_name = fig_dir + test_name + '_' + group[0].rstrip('_') + '_stream_avgs.pdf'

			# 				for index, row in group_results.iterrows():
			# 					if row['Pattern'] == 'fixed' and row['Door'] == 'All closed':
			# 						start_pattern = row['Start']
			# 						stream = row['Stream']
			# 					elif row['Pattern'] == 'CCW' and row['Door'] == 'BC open':
			# 						end_pattern = row['End']
			# 						# Calculate moving average and plot sequence
			# 						quantity = plot_data['Avg'].iloc[start_pattern:end_pattern]
			# 						ma_quantity = pd.rolling_mean(quantity, 5)
			# 						ma_quantity = ma_quantity.fillna(method='bfill')

			# 						q_max = max(ma_quantity)
			# 						q_min = min(ma_quantity)
			# 						if q_max > y_max:
			# 							y_max = q_max
			# 							x_max_index = plot_data['Time'][ma_quantity.idxmax(y_max)]-SS_near1_start
			# 						if q_min < y_min:
			# 							y_min = q_min

			# 						if stream == 'SS':
			# 							color = 'k'
			# 						elif stream == 'NF':
			# 							color = 'b'
			# 						elif stream == 'WF':
			# 							color = 'r'

			# 						t = range(0, len(ma_quantity))

			# 						plot(t, ma_quantity, 
			# 							marker=next(plot_markers), markevery=int((len(t))/10), 
			# 							mew=1.5, mec='none', ms=7, lw=1.5, ls=line_style, color = color,
			# 							label=stream+' '+group[0].rstrip('_')+' Average')
			# 					else:
			# 						continue

			# 				save_plot(x_max_index, y_max, y_min, start_plot, len(t), group, fig_name, 'west handline')
			# 				y_min = 0
			# 				y_max = 0

			# 		if(monitor_avgs_plot):
			# 			# if Test 16, plot immediately
			# 			if 'Test_16' in test_name:
			# 				fig = plt.figure()
			# 				ylabel('Velocity (m/s)', fontsize=20)
			# 				line_style = '-'
			# 				axis_scale = 'Y Scale BDP'
			# 				fig_name = fig_dir + test_name + '_' + group[0].rstrip('_') + '_stream_avgs.pdf'

			# 				plot_markers = cycle(['s', 'o', '^', 'd', 'h', 'p','v','8','D','*','<','>','H'])

			# 				# fill the start and end times for all sequences to be plotted
			# 				for index, row in group_results.iterrows():
			# 					if row['Door'] == 'All closed':		# start of a sequence
			# 						if row['Location'] == 'Near':
			# 							if row['Stream'] == 'SS':
			# 								SS_near1_start = row['Start']
			# 							elif row['Stream'] == 'NF':
			# 								NF_near_start = row['Start']
			# 							elif row['Stream'] == 'WF':
			# 								WF_start = row['Start']
			# 						elif row['Location'] == 'Far':
			# 							if row['Stream'] == 'SS':
			# 								SS_far_start = row['Start']-60
			# 							elif row['Stream'] == 'NF':
			# 								NF_far1_start = row['Start']-60
			# 							else:
			# 								continue

			# 					elif row['Door'] == 'A open':	# door A was opened
			# 						if row['Stream'] == 'SS':
			# 							SS_near1_end = row['Start']
			# 						elif row['Stream'] == 'NF':
			# 							NF_far1_end = row['Start']
			# 						else:
			# 							print '[ERROR, line '+lineno()+']:'
			# 							print 'Read row[Door] as "A open" but stream and location not valid combo'
			# 							print 'Door, stream, location = '+row['Door']+', '+row['Stream']+', '+row['Location'] 
			# 							sys.exit()

			# 					elif row['Door'] == 'BC open':	# end of a sequence
			# 						if row['Stream'] == 'SS':	# (and beginning Door A being closed if opened previously)
			# 							if row['Location'] == 'Near':
			# 								SS_near2_start = row['Start']
			# 								SS_near2_end = row['End']
			# 							elif row['Location'] == 'Far':
			# 								SS_far_end = row['End']
			# 							else:
			# 								print '[ERROR, line '+lineno()+']:'
			# 								print row
			# 								sys.exit()
			# 						elif row['Stream'] == 'NF':
			# 							if row['Location'] == 'Near':
			# 								NF_near_end = row['End']
			# 							elif row['Location'] == 'Far':
			# 								NF_far2_start = row['Start']
			# 								NF_far2_end = row['End']
			# 							else:
			# 								print '[ERROR, line '+lineno()+']:'
			# 								print row
			# 								sys.exit()
			# 						elif row['Stream'] == 'WF':
			# 							if row['Location'] == 'Far':
			# 								WF_end = row['End']
			# 							else:
			# 								continue

			# 				# create lists for SS, NF, WF data
			# 				SS_total = []
			# 				NF_total = []

			# 				SS_total.append([group_data['Avg'].iloc[SS_near1_start:SS_near1_end],
			# 					group_data['Avg'].iloc[SS_near2_start:SS_near2_end],
			# 					group_data['Avg'].iloc[SS_far_start:SS_far_end]])

			# 				NF_total.append([group_data['Avg'].iloc[NF_near_start:NF_near_end],
			# 					group_data['Avg'].iloc[NF_far1_start:NF_far1_end],
			# 					group_data['Avg'].iloc[NF_far2_start:NF_far2_end]])

			# 				WF_total = group_data['Avg'].iloc[WF_start:WF_end]

			# 				print size(SS_total)
			# 				sys.exit()
			# 				test_16_plot = pd.DataFrame({'SS':SS_total,
			# 				 	'NF':NF_total, 'WF':WF_total}, index=range(0,len(SS_total)))

			# 				print test_16_plot['SS']
			# 				sys.exit()

			# 				for stream_type in test_16_plot.columns[:]:
			# 					if stream_type == 'SS':
			# 						color = 'k'
			# 					elif stream_type == 'NF':
			# 						color = 'b'
			# 					elif stream_type == 'WF':
			# 						color = 'r'
			# 					else:
			# 						continue

			# 					# Calculate moving average and plot stream data
			# 					quantity = test_16_plot[stream_type]
			# 					ma_quantity = pd.rolling_mean(quantity, 5)
			# 					ma_quantity = ma_quantity.fillna(method='bfill')

			# 					q_max = max(ma_quantity)
			# 					q_min = min(ma_quantity)
			# 					if q_max > y_max:
			# 						y_max = q_max
			# 						x_max_index = test_16_plot['Time'][ma_quantity.idxmax(y_max)]
			# 					if q_min < y_min:
			# 						y_min = q_min

			# 					if stream == 'SS':
			# 						color = 'k'
			# 					elif stream == 'NF':
			# 						color = 'b'
			# 					elif stream == 'WF':
			# 						color = 'r'

			# 					t = range(0, len(ma_quantity))

			# 					plot(t, ma_quantity, 
			# 						marker=next(plot_markers), markevery=int((len(t))/10), 
			# 						mew=1.5, mec='none', ms=7, lw=1.5, ls=line_style, color = color,
			# 						label=stream_type+' '+group[0].rstrip('_')+' Average')

			# 				save_plot(x_max_index, y_max, y_min, start_plot, len(t), group, fig_name, 'west monitor')
			# 				y_min = 0
			# 				y_max = 0

			# 			# if Test 17 or 17b create series to plot at end of script
			# 			elif 'Test_17_' in test_name:
			# 				for index, row in group_results.iterrows():
			# 					if row['Stream'] == 'WF':
			# 						continue
			# 					elif row['Door'] == 'All closed' and row['Location'] == 'Near':
			# 						if row['Stream'] == 'SS':
			# 							test_17_SS_start = row['Start']
			# 						elif row['Stream'] == 'NF':
			# 							test_17_NF_start = row['Start']
			# 						else:
			# 							print '[ERROR, line '+lineno()+']:'
			# 							sys.exit()
			# 					elif row['Door'] == 'BC open' and row['Location'] == 'Far':
			# 						if row['Stream'] == 'SS':
			# 							test_17_SS_end = row['End']
			# 						elif row['Stream'] == 'NF':
			# 							test_17_NF_start = row['End']
			# 						else:
			# 							print '[ERROR, line '+lineno()+']:'
			# 							sys.exit()
			# 					else:
			# 						continue

			# 				test_17_SS = group_data['Avg'].iloc[test_17_SS_start:test_17_SS_end]
			# 				test_17_NF = group_data['Avg'].iloc[test_17_NF_start:test_17_NF_end]
			# 				# do moving avg and max stuff

			# 			elif 'Test_17b' in test_name:
			# 				for index, row in group_results.iterrows():
			# 					if row['Door'] == 'All closed' and row['Location'] == 'Near':
			# 						test_17_WF_start = row['Start']
			# 					elif row['Door'] == 'BC open' and row['Location'] == 'Far':
			# 						test_17_WF_end = row['End']
			# 					else:
			# 						continue

			# 				test_17_WF = group_data['Avg'].iloc[test_17_WF_start:test_17_WF_end]						

if (monitor_avgs_plot):
	# Generate plot for Test_17 
	fig = plt.figure()
	ylabel('Velocity (m/s)', fontsize=20)
	line_style = '-'
	axis_scale = 'Y Scale BDP'

	plot_markers = cycle(['s', 'o', '^', 'd', 'h', 'p','v','8','D','*','<','>','H'])

	test_17_plot = pd.DataFrame({'SS':test_17_SS.values, 'NF':test_17_NF.values, 'WF':test_17_WF.values}, 
		columns=['SS', 'NF', 'WF'])

	for stream_type in test_17_plot.columns[:]:
		if stream_type == 'SS':
			color = 'k'
		elif stream_type == 'NF':
			color = 'b'
		elif stream_type == 'WF':
			color = 'r'
		else:
			continue

		# Calculate moving average and plot stream data
		quantity = test_17_plot[stream_type]
		ma_quantity = pd.rolling_mean(quantity, 5)
		ma_quantity = ma_quantity.fillna(method='bfill')

		q_max = max(ma_quantity)
		q_min = min(ma_quantity)
		if q_max > y_max:
			y_max = q_max
			x_max_index = ma_quantity.idxmax(y_max)
		if q_min < y_min:
			y_min = q_min

		t = range(0, len(ma_quantity))

		plot(t, ma_quantity, 
			marker=next(plot_markers), markevery=int((len(t))/10), 
			mew=1.5, mec='none', ms=7, lw=1.5, ls=line_style, color = color,
			label=stream_type+ ' BDP_10 Average')

	save_plot(x_max_index, y_max, y_min, start_plot, len(t), group_test_17, fig_name_test_17_avgs, 'west monitor')
	y_min = 0
	y_max = 0

if(latex_table_code):
	# Replace Test 17 with Test 17b results due to dropped flowrate 
	far_17['WF'] = far_17_WF
	near_17['WF'] = near_17_WF
	print 
	print '% #######################'
	print '% # West Handline Table #'
	print '% #######################'
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

	print
	print '% ######################'
	print '% # West Monitor Table #'
	print '% ######################'
	print
	print '\\begin{table}[!ht]'
	print '\\caption{' + west_mon_caption + '}'
	print '\\begin{tabular}{lccccc}'
	print '\\toprule'
	print ' & \\multicolumn{2}{c}{\\underline{Test 16}} & \\multicolumn{2}{c}{\\underline{Test 17}} & \\underline{Test 33}'
	print '\\\\'
	print ' & '.join(str(column) for column in west_mon_columns)
	print '\\\ \\midrule'
	for index in streams:
		print stream_ls[index] + ' & ' + near_16[index] + ' & ' + far_16[index] + ' & ' + near_17[index] + ' & ' + far_17[index] + ' & ' + AB_33[index]
		if index == 'WF':
			print '\\\ \\bottomrule'
		else:
			print '\\\ \\multicolumn{6}{c}{} \\\\'
	print '\\end{tabular}'
	print '\\label{' + west_mon_label + '}'
	print '\\end{table}'
	print

	print
	print '% #######################'
	print '% # East Handline Table #'
	print '% #######################'
	print
	print '\\begin{table}[!ht]'
	print '\\caption{' + east_hand_caption + '}'
	print '\\begin{tabular}{lcccccc}'
	print '\\toprule'
	print ' & \\multicolumn{3}{c}{\\underline{Room A}} & \\multicolumn{3}{c}{\\underline{Room B Ceiling}}'
	print '\\\\'
	print ' & '.join(str(column) for column in east_hand_columns)
	print '\\\ \\midrule'
	for index in streams:
		print stream_ls[index] + ' & ' + fixed_A[index] + ' & ' + CW_A[index] + ' & ' + CCW_A[index] + ' & ' + fixed_B[index] + ' & ' + CW_B[index] + ' & ' + CCW_B[index]
		if index == 'WF':
			print '\\\ \\bottomrule'
		else:
			print '\\\ \\multicolumn{7}{c}{} \\\\'
	print '\\end{tabular}'
	print '\\label{' + east_hand_label + '}'
	print '\\end{table}'
	print

	# print
	# print '% ######################'
	# print '% # East Monitor Table #'
	# print '% ######################'
	# print
	# print '\\begin{table}[!ht]'
	# print '\\caption{' + east_mon_caption + '}'
	# print '\\begin{tabular}{lcccccc}'
	# print '\\toprule'
	# print ' & \\multicolumn{3}{c}{\\underline{Room A}} & \\multicolumn{3}{c}{\\underline{Room B Ceiling}}'
	# print '\\\\'
	# print ' & '.join(str(column) for column in east_mon_columns)
	# print '\\\ \\midrule'
	# for index in streams:
	# 	print stream_ls[index] + ' & ' + fixed_A[index] + ' & ' + CW_A[index] + ' & ' + CCW_A[index] + ' & ' + fixed_B[index] + ' & ' + CW_B[index] + ' & ' + CCW_B[index]
	# 	if index == 'WF':
	# 		print '\\\ \\bottomrule'
	# 	else:
	# 		print '\\\ \\multicolumn{5}{c}{} \\\\'
	# print '\\end{tabular}'
	# print '\\label{' + east_mon_label + '}'
	# print '\\end{table}'
	# print