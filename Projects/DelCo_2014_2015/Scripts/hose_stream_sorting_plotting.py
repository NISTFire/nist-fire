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
#  = Specify files =
#  =================

# Specify name
specify_test = True
specific_name = 'Test_17_West_063014'

# Specify year
specify_year = False
specific_year = '2015'

# Specify structure
specify_struct = False
specific_struct = 'West'

# Specify monitor or handline
specify_type = False
specific_type = 'monitor'

# Files to skip
skip_files = ['_times', '_reduced', '_results', 'description_', 'hose_d', '_rh', '_burn', '_span', '_original']

# =============================
# = Specify files to generate =
# =============================

result_file = False       # Generate a .csv file with channel avgs for specified sensor groups
all_channel_plot = False    # Plot of individual channels in sensor group
group_avg_plot = False     # Plot avg of all channels for sensor group
stream_avgs_plot = True    # Plot avg of all channels for each stream tested during experiment

#  =======================
#  = Directory Locations =
#  =======================

# Location of directories
data_dir = '../Experimental_Data/'      # Location of experimental data files
results_dir = '../Results/Hose_Stream/'     # Location to save results files 
fig_dir = '../Reports/Hose_Stream_Report/Figures/Plots/'     # Location to save plots
all_times_file = '../Experimental_Data/All_Times.csv'       # Location of file with timing information
info_file = '../Experimental_Data/Description_of_Experiments.csv'       # Location of test description file

# Load exp. timings and description file
all_times = pd.read_csv(all_times_file)
all_times = all_times.set_index('Time')
info = pd.read_csv(info_file, index_col=3)

#  ==========================
#  = User defined functions =
#  ==========================

# Prints an error message and stops code
def error_message(message):
	lineno = inspect.currentframe().f_back.f_lineno
	print '[ERROR, line '+str(lineno)+']:'  
	print '  ' + message
	sys.exit()

# checks if file should be skipped
def check_name(test_name, test_year, test_type):
	if specify_test:        # Skip if not specified test
		if test_name != specific_name:
			return(True)

	if specify_struct:      # Skip if not specified structure
		if specific_struct == 'West': 
			if specific_struct not in test_name:
				return(True)
		elif specific_struct == 'East':
			if 'West' in test_name:
				return(True)
		else:
			error_message('Invalid name for specific_struct')
 
	if specify_type:        # Skip if not specified type of test
		if specific_type != test_type:
			return(True)

	if specify_year:        # Skip if not specified test year
		if test_year != specific_year:
			return(True)

	return(False)

# Divides hose stream data into different sequences
def sort_data(test_name, start_time, test_type):
	if 'West' in test_name:
		# initialize lists and start_seq value
		start_seq = -1
		door_status = 'All closed'
		streams_ls = []
		P_or_L_ls = []      
		start_times_ls = []
		end_times_ls = []
		door_status_ls = []
		zero_time_ls = []

		if test_type == 'handline':
			P_or_L_heading = 'Pattern'
		else:
			P_or_L_heading = 'Location'
			if 'Test_70' in test_name:
				door_status = 'BC closed'
				stream = 'SS'

		# gathers timing information from times file
		for index, row in all_times.iterrows():
			if pd.isnull(row[test_name]) or index == 0:
				continue
			else:
				# if new sequence, add time to array to re-zero voltages
				if ('Monitor on,' in row[test_name]) or ('Hose on,' in row[test_name]):
					zero_time_ls.append(index-start_time)

				if start_seq != -1:  # add information to event row
					end_seq = index-start_time
					streams_ls.append(stream)
					P_or_L_ls.append(P_or_L)
					start_times_ls.append(start_seq)
					end_times_ls.append(end_seq)
					door_status_ls.append(door_status)

				# Check if sequence has ended
				if row[test_name] == '1st floor BC and stairwell doors closed':
					door_status = 'All closed'
					row[test_name] = 'Doors closed'
					start_seq = -1
					continue
				elif 'water off' in row[test_name].lower():
					if 'doors closed' in row[test_name].lower():
						door_status = 'BC closed'
					start_seq = -1
					continue

				# Determine stream type, pattern/location
				if 'straight stream' in row[test_name].lower():
					stream = 'SS'
					row[test_name] = row[test_name].replace('straight stream', stream)
				elif 'narrow fog' in row[test_name].lower():
					stream = 'NF'
					row[test_name] = row[test_name].replace('narrow fog', stream)
				elif 'wide fog' in row[test_name].lower():
					stream = 'WF'
					row[test_name] = row[test_name].replace('wide fog', stream)
				elif 'smooth bore' in row[test_name].lower():
					stream = 'SB'
					row[test_name] = row[test_name].replace('smooth bore', stream)                
				
				# stores location, door status, pattern, and start time for next row
				if P_or_L_heading == 'Location':
					if 'near target' in row[test_name]:
						P_or_L = 'near'
						row[test_name] = row[test_name].replace('near target', 'near')
					elif 'far target' in row[test_name]:
						P_or_L = 'far'
						row[test_name] = row[test_name].replace('far target', 'far')
				else:
					if 'fixed' in row[test_name].lower():
						P_or_L = 'fixed'
					elif 'sweeping' in row[test_name].lower():
						P_or_L = 'sweep'
					elif ' clockwise' in row[test_name].lower():
						P_or_L = 'CW'
						row[test_name] = row[test_name].replace('clockwise', P_or_L)
					elif 'counterclockwise' in row[test_name].lower():
						P_or_L = 'CCW'
						row[test_name] = row[test_name].replace('counterclockwise', P_or_L)

				if 'opened' in row[test_name]:
					if 'BC door' in row[test_name]:
						door_status = 'BC open'
					elif 'stairwell door' in row[test_name].lower():
						door_status = 'Stair open'
					elif 'A door' in row[test_name]:
						door_status = 'A open'
					else:
						error_message('Read "opened" from info file, no door found')
				elif 'A door closed' in row[test_name]:
					door_status = 'Closed A'

				start_seq = index-start_time
		group_set = {'Start': start_times_ls, 'End':end_times_ls, 'Stream':streams_ls, 
		P_or_L_heading:P_or_L_ls,'Door':door_status_ls}
		group_results = pd.DataFrame(group_set, 
			columns = ['Start', 'End', 'Stream', P_or_L_heading, 'Door'])
	else:
		# initialize lists and start_seq value
		start_seq = -1
		door_status = 'C'
		streams_ls = []
		patterns_ls = []		
		start_times_ls = []
		end_times_ls = []
		location_ls = []
		door_status_ls = []
		zero_time_ls = []
		
		for index, row in all_times.iterrows():
			if pd.isnull(row[test_name]) or index == 0:
				continue
			else:
				# mark event start time or add event info to lists
				if start_seq == -1:
					zero_time_ls.append(index-start_time)
				else:
					end_seq = index-start_time
					streams_ls.append(stream)
					patterns_ls.append(pattern)
					start_times_ls.append(start_seq)
					end_times_ls.append(end_seq)
					location_ls.append(location)
					door_status_ls.append(door_status)

				# Determine stream type, pattern, and target location
				if 'straight stream' in row[test_name].lower():
					stream = 'SS'
					row[test_name] = row[test_name].replace('straight stream', stream)
				elif 'narrow fog' in row[test_name].lower():
					stream = 'NF'
					row[test_name] = row[test_name].replace('narrow fog', stream)
				elif 'wide fog' in row[test_name].lower():
					stream = 'WF'
					row[test_name] = row[test_name].replace('wide fog', stream)
				
				# stores location, door status, pattern, and start time for next row
				if ' at ' in row[test_name]:
					location = row[test_name].split(' at ')[1]

				if 'door closed' in row[test_name]:
					door_status = 'C'

				if 'door opened' in row[test_name]:
					door_status = 'O'
					
				if 'fixed' in row[test_name].lower():
					pattern = 'fixed'
				elif any('rotated right' in row[test_name]):
					pattern = 'CW'
					row[test_name] = row[test_name].replace('rotated right', pattern)
				elif any('rotated left' in row[test_name]):
					pattern = 'CCW'
					row[test_name] = row[test_name].replace('rotated left', pattern)
				
				start_seq = index-start_time

				if 'flow stopped' in row[test_name]:
					start_seq = -1

		group_set = {'Start': start_times_ls, 'End':end_times_ls, 'Stream':streams_ls, 'Pattern':patterns_ls,
		'Location':location_ls, 'Door':door_status_ls}
		group_results = pd.DataFrame(group_set, columns = ['Start', 'End', 'Stream', 'Pattern', 'Location', 'Door'])
	
	return group_results, zero_time_ls

def plot_stream_avgs(stream_data, updated_times, x_max_index, y_max, y_min, marker, color, plot_label):
	stream_data = pd.Series(data = stream_data, index=range(-3, len(stream_data)-3))
	ma_quantity = pd.rolling_mean(stream_data, 5, center=True)
	ma_quantity = ma_quantity.dropna()
	if max(ma_quantity) > y_max:
		y_max = max(ma_quantity)
		x_max_index = ma_quantity.idxmax(y_max)
	if min(ma_quantity) < y_min:
		y_min = min(ma_quantity)

	t = ma_quantity.index.values[1:updated_times[-1]+2]

	plt.plot(t, ma_quantity.loc[1:updated_times[-1]+1], 
		ls = line_style, color = color, lw=2,
		marker=marker, markevery=int(len(t))/10, 
		mew=1.5, mec='none', ms=7, label=plot_label)

	return x_max_index, y_max, y_min, t

def save_plot(x_max_index, y_max, y_min, start_time, end_time, group, fig_name, plot_type, tick_info):
	plt.errorbar(x_max_index, y_max, yerr=(.18)*y_max, ecolor='k')
	if 'West' not in fig_name and plot_type == 'stream avgs':
		end_time = end_time - 1
	ax1 = plt.gca()
	ax1.set_xlim([0, end_time])
	ax1.set_ylim(math.floor(y_min)-0.1, math.ceil(y_max)+0.1)
	ax1.xaxis.set_major_locator(plt.MaxNLocator(8))
	ax1_xlims = ax1.axis()[0:2]
	grid(True)
	plt.axhline(0, color='0.50', lw=1)
	ax1.set_xlabel('Time (s)', fontsize=20)
	ax1.set_ylabel('Velocity (m/s)', fontsize=20)
	y_tick_ls = np.arange(math.floor(y_min), math.ceil(1.18*y_max)+1, 1)
	ax1.set_yticks(np.around(y_tick_ls,1))
	plt.xticks(fontsize=16)
	plt.yticks(fontsize=16)

	ax2 = ax1.twinx()
	ax2.set_ylabel('Velocity (mph)', fontsize=20)
	ax2.set_ylim(math.floor(y_min)-0.1, math.ceil(y_max)+0.1)
	ax2.set_yticks(y_tick_ls)
	y_label_ls = np.array(y_tick_ls) * 2.23694
	ax2.set_yticklabels(np.around(y_label_ls, 1))
	plt.xticks(fontsize=16)
	plt.yticks(fontsize=16)

	# Add vertical lines for timing information (if available)
	try:
		# Add vertical lines and labels for timing information (if available)
		ax3 = ax1.twiny()
		ax3.set_xlim(ax1_xlims)
		if plot_type != 'stream avgs':
			events = all_times[test_name].dropna()  # Grab event labels and remove NaN items
			events = events[~events.str.startswith('#')]    # Ignore events that are commented starting with a pound sign
			tick_loc = events.index.values - start_time
			tick_labels = events.values
		else:
			tick_loc = tick_info[1]
			tick_labels = tick_info[0]
		if 'West' in fig_name:
			[plt.axvline(_x, color='0.50', lw=1) for _x in tick_loc[:-1]]	
		else:		
			[plt.axvline(_x, color='0.50', lw=1) for _x in tick_loc]
			ax1.set_xticks(tick_loc)
		ax3.set_xticks(tick_loc)
		plt.setp(plt.xticks()[1], rotation=60)
		ax3.set_xticklabels(tick_labels, fontsize=10, ha='left')
		plt.xlim([0, end_time])
		# Increase figure size for plot labels at top
		if plot_type == 'stream avgs':
			fig.set_size_inches(8, 8)
		else:
			fig.set_size_inches(12,8)
	except:
		pass

	plt.gca().add_artist(ax1.legend(loc='lower right', fontsize=10, frameon = True))

	# Save plot to file
	print ('   Saving plot of ' + plot_type + ' for ' + group)
	plt.savefig(fig_name)
	plt.close('all')

# Preset options for plots
# Plot style - colors and markers
# These are the "Tableau 20" colors as RGB.
tableau20 = [(31, 119, 180), (174, 199, 232), (255, 127, 14), (255, 187, 120),
			 (44, 160, 44), (152, 223, 138), (214, 39, 40), (255, 152, 150),
			 (148, 103, 189), (197, 176, 213), (140, 86, 75), (196, 156, 148),
			 (227, 119, 194), (247, 182, 210), (127, 127, 127), (199, 199, 199),
			 (188, 189, 34), (219, 219, 141), (23, 190, 207), (158, 218, 229)]

# tableau20 = [(174, 199, 232), (255, 187, 120), (152, 223, 138)]

# Scale the RGB values to the [0, 1] range, which is the format matplotlib accepts.
for i in range(len(tableau20)):
	r, g, b = tableau20[i]
	tableau20[i] = (r / 255., g / 255., b / 255.)

y_max = 0
y_min = 0

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
		
		# Skip if not a hose test or Test 20 (lost data)
		if info['Test Type'][test_name] != 'HOSE' or test_name == 'Test_20_West_063014':
			continue

		# Determine test year and type
		if int(info['Test Number'][test_name]) <= 63:
			test_year = '2014'
		else:
			test_year = '2015'

		if 'Monitor' in info['Test Description'][test_name]:
			test_type = 'monitor'
		elif 'Handline' in info['Test Description'][test_name]:
			test_type = 'handline'
		else:
			error_message('Check "Test Description" in info file')

		if check_name(test_name, test_year, test_type):     # check if file should be skipped
			continue
		else:   # Load exp. data file
			if 'Test_17' in test_name:
				f = test_name + '_original.csv'
			data = pd.read_csv(data_dir + f)
			data = data.set_index('TimeStamp(s)')
			print
			print ('--- Loaded ' + test_name + ' ---')

		# Create group and channel lists
		if test_year == '2014':
			if 'West' in test_name:
				channel_list_file = '../DAQ_Files/DAQ_Files_2014/West_DelCo_DAQ_Channel_List.csv'
			elif 'East' in test_name:
				channel_list_file = '../DAQ_Files/DAQ_Files_2014/East_DelCo_DAQ_Channel_List.csv'
			else:
				channel_list_file = '../DAQ_Files/DAQ_Files_2014/Delco_DAQ_Channel_List.csv'
		elif test_year == '2015':
			if 'West' in test_name:
				channel_list_file = '../DAQ_Files/DAQ_Files_2015/West_DelCo_DAQ_Channel_List.csv'
			else:
				channel_list_file = '../DAQ_Files/DAQ_Files_2015/East_DelCo_DAQ_Channel_List.csv'
		channel_list = pd.read_csv(channel_list_file)
		channel_list = channel_list.set_index('Device Name')
		channel_groups = channel_list.groupby('Group Name')

		# Read in test times to offset plots 
		start_of_test = int(info['Start of Test'][test_name])

		# Offset data time to start of test
		new_times = data['Time'].values - start_of_test
		data['Time'] = new_times
		data = data.set_index('Time')
		data['Time'] = new_times

		event_times, zero_time_ls = sort_data(test_name, start_of_test, test_type)
		end_data = event_times['End'].iloc[-1]

		if 'West' in test_name:
			included_groups = ['BDP A10']
		else:
			included_groups = ['BDP A6']

		# List through sensor groups to analyze
		for group in channel_groups.groups:
			# Skip excluded groups listed in test description file
			# if any([substring in group for substring in info['Excluded Groups'][test_name].split('|')]):
			#     continue

			if any([substring in group for substring in included_groups]) == False:
				continue
			 
			group_results = event_times

			# create empty df to fill with desired channel data
			group_data = pd.DataFrame(columns = ['Time'])
			group_data = group_data.set_index('Time')
			group_data['Time'] = data['Time'].loc[-10:end_data+10]

			if all_channel_plot:
				fig = plt.figure()
				plt.rc('axes', color_cycle=tableau20)
				plot_markers = cycle(['s', 'o', '^', 'd', 'h', 'p','v','8','D','*','<','>','H'])
				plt.ylabel('Velocity (m/s)', fontsize=20)
				axis_scale = 'Y Scale BDP'
				line_style = '-'
				secondary_axis_label = 'Velocity (mph)'
				secondary_axis_scale = np.float(info[axis_scale][test_name]) * 2.23694

			for channel in channel_groups.get_group(group).index.values:
				# Skip excluded channels listed in hose_info file
				if any([substring in channel for substring in info['Excluded Channels'][test_name].split('|')]):
					continue

				# calculate initial zero voltage, create empty list for calculated velocities
				zero_start = zero_time_ls[0] - 25
				zero_end = zero_start + 20
				zero_voltage = np.mean(data[channel][zero_start:zero_end])
				i = 1
				group_data[channel] = ''
				group_results[channel] = ''

				# convert voltages to velocities
				for index, row in group_data.iterrows():
					# check if zero voltage needs to be re-calculated
					if (zero_time_ls[i] - 25) == index:
						zero_start = int(row['Time'])
						zero_end = zero_start + 20
						zero_voltage = np.mean(data[channel][zero_start:zero_end])
						# iterate i if additional zero voltages will be calculated
						if i < (len(zero_time_ls)-1):
							i += 1
					pressure = conv_inch_h2o * conv_pascal * (data.loc[index, channel] - zero_voltage)
					group_data.loc[index, channel] = 0.0698 * np.sqrt(np.abs(pressure) * (data.loc[index, 'TC_' + channel[4:]] + 273.15)) * np.sign(pressure)

				if all_channel_plot:        # plot individual channels
					# check y min and max
					ma_quantity = pd.rolling_mean(group_data[channel], 5)
					ma_quantity = ma_quantity.fillna(method='bfill')
					ma_quantity = ma_quantity.loc[0:end_data]
					if max(ma_quantity) > y_max:
						y_max = max(ma_quantity)
						x_max_index = group_data['Time'][ma_quantity.idxmax(y_max)]
					if min(ma_quantity) < y_min:
						y_min = min(ma_quantity)

					plt.plot(ma_quantity.index.values, ma_quantity, 
						marker=next(plot_markers), markevery=int(len(group_data['Time'])/20),
						mew=1.5, mec='none', ms=7, ls=line_style, lw=2, label=channel)

			# calculate channel avg at each time step add to group_data df
			channel_avg = []
			for index, row in group_data.iterrows():
				channel_avg.append(np.mean(row[1:]))
			group_data['Avg'] = channel_avg

			if result_file:     # create file with averages for each channel at each event listed in group_results
				group_results['Avg'] = ''
				# SS_near_data = []
				# SS_far_data = []
				# SB_near_data = []
				# SB_far_data = []
				if 'West' in test_name:
					first_col = 5		# West results includes either a pattern or a location column
				else:
					first_col = 6		# East results include both a pattern and location column

				for index, row in group_results.iterrows():
					# create df for each event in new .csv file
					seq_data = group_data.loc[row['Start']:row['End']]

					# if row['Door'] == 'BC open':
					# 	if row['Stream'] == 'SS':
					# 		if row['Location'] == 'near':
					# 			SS_near_data.append(seq_data['Avg'])
					# 		elif row['Location'] == 'far':
					# 			SS_far_data.append(seq_data['Avg'])
					# 		else:
					# 			error_message('Invalid location read')
					# 	elif row['Stream'] == 'SB':
					# 		if row['Location'] == 'near':
					# 			SB_near_data.append(seq_data['Avg'])
					# 		elif row['Location'] == 'far':
					# 			SB_far_data.append(seq_data['Avg'])
					# 		else:
					# 			error_message('Invalid location read')
					# 	else:
					# 		error_message('Invalid stream read')

					# Calculate average for each channel during sequence
					for column in group_results.columns[first_col:]:
						# calculate avg for each channel during event 
						group_results.loc[index, column] = round(np.mean(seq_data[column]), 1)
						# group_results.loc[index, column] = str(round(np.mean(seq_data[column]), 1)) + ' +- ' + str(round(np.std(seq_data[column]), 1))


				# Saves results .csv file for sensor group
				group_results.to_csv(results_dir + test_name + '_' + group.replace(' ', '_')  + '_averages.csv')
				print ('   Saving result file for ' + group)
				# print 'SS Near: ' + str(round(np.mean(SS_near_data), 1)) + ' +- ' + str(round(np.std(SS_near_data), 1))
				# print 'SS Far: ' + str(round(np.mean(SS_far_data), 1)) + ' +- ' + str(round(np.std(SS_far_data), 1))
				# print 'SB Near: ' + str(round(np.mean(SB_near_data), 1)) + ' +- ' + str(round(np.std(SB_near_data), 1))
				# print 'SB Far: ' + str(round(np.mean(SB_far_data), 1)) + ' +- ' + str(round(np.std(SB_far_data), 1))

			if all_channel_plot:        # save plot of individual channels
				fig_name = fig_dir + test_name + '_' + group.replace(' ', '_') + '.pdf'
				save_plot(x_max_index, y_max, y_min, start_of_test, end_data, group, fig_name, 'all channels', [])
				y_min = 0
				y_max = 0
				sys.exit()

			if group_avg_plot:      # plot and save avg of all channels in group
				fig = plt.figure()
				plt.rc('axes', color_cycle=tableau20)
				plot_markers = cycle(['s', 'o', '^', 'd', 'h', 'p','v','8','D','*','<','>','H'])
				plt.ylabel('Velocity (m/s)', fontsize=20)
				axis_scale = 'Y Scale BDP'
				line_style = '-'
				secondary_axis_label = 'Velocity (mph)'
				secondary_axis_scale = np.float(info[axis_scale][test_name]) * 2.23694
				fig_name = fig_dir + test_name + '_' + group.replace(' ', '_') + '_average.pdf'

				# check y min and max
				ma_quantity = pd.rolling_mean(group_data['Avg'], 5)
				ma_quantity = ma_quantity.fillna(method='bfill')
				if max(ma_quantity) > y_max:
					y_max = max(ma_quantity)
					x_max_index = group_data['Time'][ma_quantity.idxmax(y_max)]
				if min(ma_quantity) < y_min:
					y_min = min(ma_quantity)

				plt.plot(group_data['Time'], ma_quantity, 
					marker=next(plot_markers), markevery=int(len(group_data['Time']))/20, mew=1.5, mec='none', ms=7, 
					ls=line_style, lw=2, label=group + ' Avg')

				save_plot(x_max_index, y_max, y_min, start_of_test, end_data, group, fig_name, 'group avg', [])
				y_min = 0
				y_max = 0

			if stream_avgs_plot:     # plot and save avg of all channels during each stream
				y_min = 0
				y_max = 0
				x_max_index = 0
				fig = plt.figure()
				SS_color, NF_color, WF_color, SB_color = tableau20[1], tableau20[3], tableau20[5], tableau20[7]
				SS_mark, NF_mark, WF_mark, SB_mark = 's', 'o', '^', 'd'
				plt.ylabel('Velocity (m/s)', fontsize=20)
				axis_scale = 'Y Scale BDP'
				line_style = '-'
				secondary_axis_label = 'Velocity (mph)'
				secondary_axis_scale = np.float(info[axis_scale][test_name]) * 2.23694
				fig_name = fig_dir + test_name + '_' + group.replace(' ', '_') + '_stream_avgs.pdf'
				
				xtick_labels = []
				test_streams = ['SS', 'NF', 'WF']
				if 'West' in test_name:
					if test_year == '2014':
						if test_type == 'monitor':
							variable_list = ['near target', 'far target']
						elif test_type == 'handline':
							variable_list = ['fixed', 'sweeping', 'rotate CW', 'rotate CCW']
						for variable in variable_list:
							xtick_labels.extend(['Water on, ' + variable, 'Stairwell door opened',
								'2nd floor, W door opened', 'Water off, doors closed'])
					else:
						test_streams = ['SS', 'SB']
						variable_list = ['near target', 'far target']
						for variable in variable_list:
							xtick_labels.extend(['Water on, ' + variable, '2nd floor, W door opened', 'Water off',
								'Water on, ' + variable, 'Water off', 
								'Water on, ' + variable, 'Water off, doors closed'])

					xlabel_times = []
					stream_num = 1
					stream_names = []
					time_btwn_seq = []
					for index, row in group_results.iterrows():
						if row['Door'] == 'A open' or row['Door'] == 'Closed A':	# skips part of Test 16
							continue
						start_seq = row['Start']
						if index == 0:      # first row, set initial values
							end_seq = row['End']
							stream = row['Stream']
							stream_names.append(stream)
							xlabel_times.extend([start_seq, end_seq])
							continue

						if stream_num == 1:     # first stream pattern
							if stream == row['Stream']:
								time_btwn_seq.append(start_seq-end_seq)
								end_seq = row['End']
								xlabel_times.extend([start_seq, end_seq])
								continue
							else: # set up dataframe, move to next stream
								stream_times_setup = {stream:xlabel_times}
								stream_times = pd.DataFrame(stream_times_setup, columns = [stream])
								current_stream_times = []
								end_seq = row['End']
								current_stream_times.extend([start_seq, end_seq])
								stream = row['Stream']
								stream_names.append(stream)
								stream_num = stream_num + 1
								i = 0
								continue
						else:
							if stream == row['Stream']:
								current_time_btwn = start_seq-end_seq
								if time_btwn_seq[i] > current_time_btwn:    # new minimum time between seqs
									time_btwn_seq[i] = current_time_btwn
								end_seq = row['End']
								current_stream_times.extend([start_seq, end_seq])
								i = i + 1
							else:
								stream_times[stream] = current_stream_times
								current_stream_times = []
								end_seq = row['End']
								current_stream_times.extend([start_seq, end_seq])
								stream = row['Stream']
								stream_names.append(stream)
								stream_num = stream_num + 1
								i = 0                                   
					stream_times[stream] = current_stream_times
					current_stream_times = []
					end_seq = row['End']
					current_stream_times.extend([start_seq, end_seq])
					stream = row['Stream']
					stream_names.append(stream)
					stream_num = stream_num + 1
					count = 1
					updated_times = [0]
					# Find smallest time between each event and updated times for plot and labels
					while count < (len(xlabel_times)):
						if count % 2 == 0:
							current_diff = time_btwn_seq[(count/2)-1]
						else:
							current_diff = xlabel_times[count]-xlabel_times[count-1]
						next_time = updated_times[-1] + current_diff
						if next_time != updated_times[-1]:
							updated_times.append(next_time)
						count = count+1
					column_num = 0
					for column in test_streams:
						plot_label = column + ' A10 Avg'
						if column == 'SS':
							color, marker = SS_color, SS_mark
						elif column == 'NF':
							color, marker = NF_color, NF_mark
						elif column == 'WF':
							color, marker = WF_color, WF_mark
						elif column == 'SB':
							color, marker = SB_color, SB_mark
						
						stream_data = []
						i = 0
						for index, row in stream_times.iterrows():
							if index % 2 == 0:
								start_loc = row[column]+1
								if index == 0:
									start_loc = start_loc-3
								continue
							else:
								if i > (len(time_btwn_seq)-1):        # last end time
									end_loc = row[column]+4
								else:       # in between times, add in time between seq
									end_loc = row[column] + time_btwn_seq[i]
									# print start_loc, end_loc
								i = i + 1
								stream_data.extend(group_data['Avg'].loc[start_loc:end_loc])

						x_max_index, y_max, y_min, t = plot_stream_avgs(stream_data, updated_times, 
														x_max_index, y_max, y_min, marker, color, plot_label)

				else:
					if test_name[7] == 'A':
						locations = ['Room B ceiling', 'S doorway in Room B']
						patterns = ['Fixed', 'CW']
						loop = 0
						while (loop < 2):
							if loop == 1:
								patterns[1] = 'CCW'
							for l in locations:
								for p in patterns:
									xtick_labels.append(p + ' at ' + l)
							loop += 1
						xtick_labels.append(' Water off')
						updated_times = [0, 30, 60, 90, 120, 150, 180, 210, 240]
					else:
						xtick_labels = [' Water on, S doorway in Room B', ' Water flow stopped']
						updated_times = [0, 60]
					
					SS_remain = True
					NF_remain = True
					WF_remain = True
					while(SS_remain or NF_remain or WF_remain):
						stream_data = []
						if (SS_remain):
							iteration = 1
							for index, row in group_results.iterrows():
								if row['Door'] == 'O':
									continue
								if row['Stream'] == 'SS':
									seq_start = int(row['Start'])+1
									seq_end = int(row['End'])
									if iteration == 1:	# fill extra 3 for moving average
										seq_start = seq_start-3
									stream_data.extend(group_data['Avg'].loc[seq_start:seq_end])
									iteration += 1
							# fill extra 3 at end for moving average
							stream_data.extend(group_data['Avg'].loc[seq_end:seq_end+4])
							SS_remain = False
							column = 'SS'
						elif (NF_remain):
							iteration = 1
							for index, row in group_results.iterrows():
								if row['Door'] == 'O':
									continue
								if row['Stream'] == 'NF':
									seq_start = int(row['Start'])+1
									seq_end = int(row['End'])
									if iteration == 1:	# fill extra 3 for moving average
										seq_start = seq_start-3
									stream_data.extend(group_data['Avg'].loc[seq_start:seq_end])
									iteration += 1
							# fill extra 3 at end for moving average
							stream_data.extend(group_data['Avg'].loc[seq_end:seq_end+4])
							NF_remain = False
							column = 'NF'
						elif (WF_remain):
							iteration = 1
							for index, row in group_results.iterrows():
								if row['Door'] == 'O':
									continue
								if row['Stream'] == 'WF':
									seq_start = int(row['Start'])+1
									seq_end = int(row['End'])
									if iteration == 1:	# fill extra 3 for moving average
										seq_start = seq_start-3
									stream_data.extend(group_data['Avg'].loc[seq_start:seq_end])
									iteration += 1
							# fill extra 3 at end for moving average
							stream_data.extend(group_data['Avg'].loc[seq_end:seq_end+4])
							WF_remain = False
							column = 'WF'
						
						# check y min and max

						stream_data = pd.Series(data = stream_data, index=range(-3, len(stream_data)-3))
						ma_quantity = pd.rolling_mean(stream_data, 5, center=True)
						ma_quantity = ma_quantity.dropna()
						if max(ma_quantity) > y_max:
							y_max = max(ma_quantity)
							x_max_index = ma_quantity.idxmax(y_max)
						if min(ma_quantity) < y_min:
							y_min = min(ma_quantity)

						t = ma_quantity.index.values[1:updated_times[-1]+2]

						plt.plot(t, ma_quantity.loc[1:updated_times[-1]+1], 
							marker=next(plot_markers), markevery=int(len(t))/10, 
							mew=1.5, mec='none', ms=7, ls=line_style, lw=2, label=column + ' A6 Avg')
								 
				# updated_times[-1] = t[-1]+1

				tick_info = (xtick_labels, updated_times)
				save_plot(x_max_index, y_max, y_min, start_of_test, len(t), group, 
					fig_name, 'stream avgs', tick_info)
				y_min = 0
				y_max = 0
