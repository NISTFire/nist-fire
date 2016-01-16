# -*- coding: utf-8 -*-
from __future__ import unicode_literals
#!/usr/bin/env python

import os
import collections
import numpy as np
import pandas as pd
import math
import matplotlib.pyplot as plt
from itertools import cycle
import sys

from matplotlib import rcParams
rcParams.update({'figure.autolayout': True})

#  =================
#  = User Settings =
#  =================

# Specify name
specify_test = False
# specific_name = 'Test_25_West_070214'

# Specify year to skip
specify_year = True
skip_year = '2014'
# skip_year = '2015'

# Specify type 
specify_type = True
specific_type = 'HOSE'

# Specify structure
specify_struct = True
specific_struct = 'West'

# Different file output options
result_file = True          # Generate a .csv file with channel avgs for specified sensor groups
all_channel_plot = True    # Plot each individual channel
group_avg_plot = True      # Plot avgs of all channels in group
# Plot BDP avgs from monitor experiments for SS, NF, WF application
monitor_avgs_plot = False
west_monitor_labels = ['Hose on, near target', 'Stairwell door opened', '2nd floor, W door opened', 'Doors closed',
'Hose on, far target', 'Stairwell door opened', '2nd floor, W door opened', 'Doors closed']
# monitor_avgs_plot_2015 = True
# west_monitor_labels = ['Hose on, near target', 'Stairwell door opened', '2nd floor, W door opened', 'Doors closed',
# 'Hose on, far target', 'Stairwell door opened', '2nd floor, W door opened', 'Doors closed']
# Plot BDP avgs from handline experiments for SS, NF, WF application
handline_avgs_plot = False 
west_handline_labels = ['Hose on, fixed', 'Stairwell door opened', '2nd floor, W door opened', 'Doors closed',
'Hose on, sweeping', 'Stairwell door opened', '2nd floor, W door opened', 'Doors closed', 'Hose on, rotate CW', 'Stairwell door opened', 
'2nd floor, W door opened', 'Doors closed', 'Hose on, rotate CCW', 'Stairwell door opened', '2nd floor, W door opened', 'Doors closed',]

# Plot mode: figure or video
plot_mode = 'figure'

# Files to skip
skip_files = ['_times', '_reduced', 'description_','zero_','_rh','burn','helmet']

# Time averaging window for data smoothing
data_time_averaging_window = 5

# Duration of pre-test time for bi-directional probes and heat flux gauges (s)
pre_test_time = 60

# DelCo 2014 sensor grouping
sensor_groups_2014 = [['TC_A1_'], ['TC_A2_'], ['TC_A3_'], ['TC_A4_'], ['TC_A5_'],
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

plot_temp = False
plot_vel = False
plot_HF = False
plot_press = False
plot_gas = False
plot_hose = False

# Location of experimental data files
data_dir = '../Experimental_Data/'

# Location of file with timing information
all_times_file = '../Experimental_Data/All_Times.csv'

# Location of test description file
info_file = '../Experimental_Data/Description_of_Experiments.csv'

# Location to save results file
results_dir = '../Results/'

# Location to save hose stream plots
hose_fig_dir = '../Figures/Hose_Stream_Figures/'

# Location to save/output figures
if plot_mode == 'figure':
    save_dir = '../Figures/Script_Figures/'
elif plot_mode == 'video':
    save_dir = '../Figures/Video_Figures/'

# Load exp. timings and description file
all_times = pd.read_csv(all_times_file)
all_times = all_times.set_index('Time')
info = pd.read_csv(info_file, index_col=3)

#  ===================
#  = Video Plot Mode =
#  ===================

video_test_name = 'Test_38_West_61315'
video_groups = ['Heat Flux']
video_channels = ['Heat Flux 1 V West','Heat Flux 1 H West','Heat Flux Mask']
video_line_colors = ['yellow', 'cyan', 'green']
video_ylabel = 'Heat Flux (kW/m$^2$)'
video_rescale_factor = 1
video_rescale_offset = 0
video_xlim_lower, video_xlim_upper, video_ylim_lower, video_ylim_upper = [0, 400, 0, 30]
video_plots = collections.OrderedDict()


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
    # lost data during Test 20
    if 'Test_20_West_063014' == test_name:
        return(True)

    # Skip if not specified test
    if specify_test:
        if test_name != specific_name:
            return(True)

    # Skip if not specified structure
    if specify_struct:
        if specific_struct == 'West': 
            if specific_struct not in test_name:
                return(True)
        elif specific_struct == 'East':
            if 'West' in test_name:
                return(True)
        else:
            error_message('Invalid name for specific_struct')
 
    # Skip if not specified type of test
    if specify_type:
        if test_type != specific_type:
            return(True)

    # Skip if not specified test year
    if specify_year:
        if test_year == skip_year:
            return(True)

    # If video plot mode is enabled, then plot from only one test
    if plot_mode == 'video':
        if video_test_name not in test_name:
            return(True)

    return(False)

# Divides hose stream data into different sequences
def sort_hose_group(group, test_name):
    if 'West' in test_name:
        # initialize lists and start_seq value
        start_seq = 0
        door_status = 'All closed'
        streams_ls = []
        P_or_L_ls = []      
        start_times_ls = []
        end_times_ls = []
        door_status_ls = []
        zero_time_ls = []

        if 'Test_18' in test_name or 'Test_19' in test_name:
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
                # check if event in beginning of new sequence, if so add to array to re-zero voltages
                if ('Monitor on,' in row[test_name]) or ('Hose on,' in row[test_name]):
                    zero_time_ls.append(index)

                if start_seq != 0:  # add information to event row
                    end_seq = index
                    streams_ls.append(stream)
                    P_or_L_ls.append(P_or_L)
                    start_times_ls.append(start_seq)
                    end_times_ls.append(end_seq)
                    door_status_ls.append(door_status)

                if row[test_name] == '1st floor BC and stairwell doors closed': # experiment has ended
                    door_status = 'All closed'
                    row[test_name] = 'Doors closed'
                    start_seq = 0
                    continue

                if 'water off' in row[test_name].lower():
                    row[test_name] = row[test_name].lower()
                    if 'doors closed' in row[test_name]:
                        door_status = 'BC closed'
                    start_seq = 0
                    continue

                # Determine stream type, pattern/location
                if 'straight stream' in row[test_name].lower():
                    stream = 'SS'
                    row[test_name] = row[test_name].lower()
                    row[test_name] = row[test_name].replace('straight stream', stream)
                elif 'narrow fog' in row[test_name].lower():
                    stream = 'NF'
                    row[test_name] = row[test_name].lower()
                    row[test_name] = row[test_name].replace('narrow fog', stream)
                elif 'wide fog' in row[test_name].lower():
                    stream = 'WF'
                    row[test_name] = row[test_name].lower()
                    row[test_name] = row[test_name].replace('wide fog', stream)
                elif 'smooth bore' in row[test_name].lower():
                    stream = 'SB'
                    row[test_name] = row[test_name].lower()
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

                start_seq = index

        group_set = {'Start': start_times_ls, 'End':end_times_ls, 'Stream':streams_ls, P_or_L_heading:P_or_L_ls,'Door':door_status_ls}
        group_results = pd.DataFrame(group_set, columns = ['Start', 'End', 'Stream', P_or_L_heading, 'Door'])
        return group_results, zero_time_ls
    else:
        print 'Need to write code for sorting East Tests'
        sys.exit()

# Finishes formatting and saves plots for hose stream tests
def save_hose_plot(x_max_index, y_max, y_min, start_time, end_time, group, fig_name, plot_type):
    plt.errorbar(x_max_index, y_max, yerr=(.18)*y_max, ecolor='k')
    # Set axis options, legend, tickmarks, etc.
    ax1 = plt.gca()
    y_tick_ls = []
    y_label_ls = []
    ax1.set_xlim([0, end_time])
    ax1.set_ylim(math.floor(y_min)-0.1, math.ceil(y_max)+0.1)
    # ax1.xaxis.set_major_locator(MaxNLocator(8))
    # ax1_xlims = ax1.axis()[0:2]
    # grid(True)
    plt.axhline(0, color='0.50', lw=1)
    ax1.set_xlabel('Time (s)', fontsize=20)
    ax1.set_ylabel('Velocity (m/s)', fontsize=20)
    y_tick_ls = np.arange(math.floor(y_min), math.ceil(1.18*y_max)+1, 1)
    ax1.set_yticks(np.around(y_tick_ls,1))

    ax2 = ax1.twinx()
    ax2.set_ylabel('Velocity (mph)', fontsize=20)
    ax2.set_ylim(math.floor(y_min)-0.1, math.ceil(y_max)+0.1)
    ax2.set_yticks(y_tick_ls)
    y_label_ls = np.array(y_tick_ls) * 2.23694
    ax2.set_yticklabels(np.around(y_label_ls, 1))

    plt.xticks(fontsize=16)
    plt.yticks(fontsize=16)

    # Add vertical lines for timing information (if available)
    if plot_type != 'west monitor':
        x_ticks_ls = []
        for index, row in all_times.iterrows():
            if pd.isnull(row[test_name]) or start_time > index or index-start_time > end_time:
                continue
            plt.axvline(int(index) - start_time, color='0.50', lw=1)
            x_ticks_ls.append(int(index)-start_time)
    try:
        # Add vertical lines and labels for timing information (if available)
        ax3 = ax1.twiny()
        ax3.set_xlim([0, end_time])
        # Remove NaN items from event timeline
        events = all_times[test_name].dropna()
        # Ignore events that are commented starting with a pound sign
        events = events[~events.str.startswith('#')]
        # [plt.axvline(_x - start_of_test, color='0.50', lw=1) for _x in events.index.values]
        ax3.set_xticks(events.index.values - start_of_test)
        plt.setp(plt.xticks()[1], rotation=60)
        ax3.set_xticklabels(events.values, fontsize=8, ha='left')
        plt.xlim([0, end_time])
        # Increase figure size for plot labels at top
        fig.set_size_inches(10, 6)
    except:
        pass
    # try:

    #         # Add secondary x-axis labels for timing information
    #         ax3 = ax1.twiny()
    #         ax3.set_xlim([0, end_time])
    #         ax3.set_xticks(x_ticks_ls)
    #         setp(xticks()[1], rotation=60)
    #         if plot_type == 'west handline':
    #             ax3.set_xticklabels(west_handline_labels, fontsize=10, ha='left')   
    #         else:
    #             x3.set_xticklabels(all_times[test_name].dropna().values, fontsize=10, ha='left')

    #     else:       # cheat for now and manually set tick marks, vertically lines for Tests 16, 17
    #         x_ticks_ls = [0,60,120,180,240,300,360,420]
    #         for value in x_ticks_ls:
    #             axvline(value, color='0.50', lw=1)

    #         # Add secondary x-axis labels for timing information
    #         ax3 = ax1.twiny()
    #         ax3.set_xlim([0, end_time])
    #         ax3.set_xticks(x_ticks_ls)
    #         setp(xticks()[1], rotation=60)
    #         ax3.set_xticklabels(west_monitor_labels, fontsize=10, ha='left')        

    #     # Increase figure size for plot labels at top
    #     fig.set_size_inches(8,8)
    # except:
    #     pass

    plt.gca().add_artist(ax1.legend(loc='lower right', fontsize=10, frameon = True))

    # Save plot to file
    print '  Saving ' + plot_type + ' plot for ' + group
    plt.savefig(fig_name)
    plt.close('all')

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

        # Determine test year and type
        if int(info['Test Number'][test_name]) <= 63:
            test_year = '2014'
        else:
            test_year = '2015'

        test_type = info['Test Type'][test_name]
        
        if check_name(test_name, test_year, test_type):     # check if file should be skipped
            continue
        else:   # Load exp. data file
            data = pd.read_csv(data_dir + f)
            data = data.set_index('TimeStamp(s)')
            print
            print '--- Loaded ' + test_name + ' ---'

        # Read in test times to offset plots
        start_of_test = info['Start of Test'][test_name]
        end_of_test = info['End of Test'][test_name]

        # Offset data time to start of test
        data['Time'] = data['Time'].values - start_of_test

        if test_type != 'HOSE':
            # Smooth all data channels with specified data_time_averaging_window
            data_copy = data.drop('Time', axis=1)
            data_copy = pd.rolling_mean(data_copy, data_time_averaging_window, center=True)
            data_copy.insert(0, 'Time', data['Time'])
            data_copy = data_copy.dropna()
            data = data_copy

        # Create group and channel lists
        sensor_group_list = []
        if test_year == '2014':
            if 'West' in test_name:
                channel_list_file = '../DAQ_Files/DAQ_Files_2014/West_DelCo_DAQ_Channel_List.csv'
            elif 'East' in test_name:
                channel_list_file = '../DAQ_Files/DAQ_Files_2014/East_DelCo_DAQ_Channel_List.csv'
            else:
                channel_list_file = '../DAQ_Files/DAQ_Files_2014/Delco_DAQ_Channel_List.csv'
            channel_list = pd.read_csv(channel_list_file)
            channel_list = channel_list.set_index('Device Name')
            sensor_group_list = sensor_groups_2014
        elif test_year == '2015':
            if 'West' in test_name:
                channel_list_file = '../DAQ_Files/West_DelCo_DAQ_Channel_List.csv'
            else:
                channel_list_file = '../DAQ_Files/East_DelCo_DAQ_Channel_List.csv'
            channel_list = pd.read_csv(channel_list_file)
            channel_list = channel_list.set_index('Device Name')
            channel_groups = channel_list.groupby('Group Name')
            for sensor_group in channel_groups.groups:
                sensor_group_list.append(sensor_group)

        #  ============
        #  = Plotting =
        #  ============

        # Generate a plot for each quantity group
        for group in sensor_group_list:
            # Skip excluded groups listed in test description file
            if any([substring in group for substring in info['Excluded Groups'][test_name].split('|')]):
                continue

            # generate list of channel names for current group
            channel_names = []
            if test_year == '2015':
                for name in channel_groups.get_group(group).index.values:
                    channel_names.append(name)
            else:
                for name in data.columns[1:]:
                    if any([substring in channel for substring in group]):
                        channel_names.append(name)

            # If video plot mode is enabled, then plot only specified groups
            if plot_mode == 'video':
                if any([substring in group for substring in video_groups]):
                    pass
                else:
                    continue

            fig = plt.figure()

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

            if test_type == 'HOSE':
                group_results, zero_time_ls = sort_hose_group(group, test_name)
                # create empty df to fill with desired channel data
                start_plot = group_results['Start'].iloc[0]
                end_data = group_results['End'].iloc[-1]
                group_data = pd.DataFrame(data['Time'].iloc[0:end_data], columns = ['Time'])
                # set plot properties
                line_style = '-'
                axis_scale = 'Y Scale BDP'
                y_min = 0
                y_max = 0
                x_max_index = 0
                t = range(0, len(group_data['Time'])-start_plot)
                line_width = 1.5

            for channel in channel_names:

                # Skip plot quantity if channel name is blank
                if pd.isnull(channel):
                    continue

                # Skip excluded channels listed in test description file
                if any([substring in channel for substring in info['Excluded Channels'][test_name].split('|')]):
                    continue

                # If video plot mode is enabled, then plot only specified channels
                if plot_mode == 'video':
                    if any([substring in channel for substring in video_channels]):
                        pass
                    else:
                        continue

                if test_type == 'HOSE':
                    # calculate initial zero voltage, create list and populate with calculated velocities
                    zero_start = zero_time_ls[0] - 25
                    zero_end = zero_time_ls[0] - 5
                    zero_voltage = np.mean(data[channel][zero_start:zero_end])
                    i = 1
                    conv_vel = []
                    conv_inch_h2o = 0.4
                    conv_pascal = 248.8
                    for index, row in data.iloc[0:end_data].iterrows():
                        # check if zero voltage needs to be re-calculated for next sequence
                        if (zero_time_ls[i] - 25) == row['Time']:
                            zero_start = int(row['Time'])
                            zero_end = zero_start + 20
                            zero_voltage = np.mean(data[channel][zero_start:zero_end])
                            # iterate i if additional zero voltages will be calculated
                            if i < (len(zero_time_ls)-1):
                                i += 1
                        pressure = conv_inch_h2o * conv_pascal * (row[channel] - zero_voltage)
                        conv_vel.append(0.0698 * np.sqrt(np.abs(pressure) * (row['TC_' + channel[4:]] + 273.15)) * np.sign(pressure))
                    group_data[channel] = conv_vel
                    group_results[channel] = ''

                    # plot individual channels
                    if all_channel_plot:
                        current_channel_data = group_data[channel].iloc[start_plot:end_data]
                        current_channel_data = pd.rolling_mean(current_channel_data, 5)
                        current_channel_data = current_channel_data.fillna(method='bfill')
                        q_max = max(current_channel_data)
                        q_min = min(current_channel_data)
                        if q_max > y_max:
                            y_max = q_max
                            x_max_index = group_data['Time'][current_channel_data.idxmax(y_max)]-start_plot
                        if q_min < y_min:
                            y_min = q_min
                    else:
                        continue
                else:
                    # Scale channel and set plot options depending on quantity
                    current_channel_data = data[channel]
                    calibration_slope = float(channel_list['Calibration Slope'][channel])
                    calibration_intercept = float(channel_list['Calibration Intercept'][channel])
                    secondary_axis_label = None  # Reset secondary axis variable

                    if test_year == '2015':
                        if channel_list['Measurement Type'][channel] == 'Temperature':
                            if 'TC Helmet ' in channel or 'TC_Helmet_' in channel:
                                axis_scale = 'Y Scale TC_Helmet'
                            elif 'TC Gear' in group:
                                axis_scale = 'Y Scale TC_Gear'
                            elif 'TC Manikin ' in channel:
                                axis_scale = 'Y Scale TC_Manikin'
                            else:
                                axis_scale = 'Y Scale TC'
                            plot_temp = True
                        elif channel_list['Measurement Type'][channel] == 'Velocity':
                            if int(info['Test Number'][test_name]) >= 91 and 'East' in test_name and 'BDP A7' in group:
                                axis_scale = 'Y Scale PRESSURE'
                            else:
                                axis_scale = 'Y Scale BDP'
                            plot_vel = True
                        elif channel_list['Measurement Type'][channel] == 'Heat Flux':
                            axis_scale = 'Y Scale HF'
                            plot_HF = True
                        elif channel_list['Measurement Type'][channel] == 'Pressure':
                            axis_scale = 'Y Scale PRESSURE'
                            plot_press = True
                        elif channel_list['Measurement Type'][channel] == 'Gas':
                            axis_scale = 'Y Scale GAS'
                            plot_gas = True
                        elif channel_list['Measurement Type'][channel] == 'Hose':
                            axis_scale = 'Y Scale HOSE'
                            plot_hose = True
                    elif test_year == '2014':
                        if 'TC_' in channel:
                            if 'TC Helmet ' in channel or 'TC_Helmet_' in channel:
                                axis_scale = 'Y Scale TC_Helmet'
                            elif 'TC Gear' in group:
                                axis_scale = 'Y Scale TC_Gear'
                            elif 'TC Manikin ' in channel:
                                axis_scale = 'Y Scale TC_Manikin'
                            else:
                                axis_scale = 'Y Scale TC'
                            plot_temp = True
                        elif 'BDP_' in channel:
                            axis_scale = 'Y Scale BDP'
                            plot_vel = True
                        elif any([substring in channel for substring in heat_flux_quantities]):
                            axis_scale = 'Y Scale HF'
                            plot_HF = True
                        elif any([substring in channel for substring in gas_quantities]):
                            axis_scale = 'Y Scale GAS'
                            plot_gas = True
                        elif 'HOSE_' in channel:
                            axis_scale = 'Y Scale HOSE'
                            plot_hose = True

                    # Skip plot quantity if disabled in test description file
                    if info[axis_scale][test_name] == 'None':
                        continue

                    # Plot temperatures
                    if plot_temp:
                        current_channel_data = current_channel_data * calibration_slope + calibration_intercept
                        plt.ylabel('Temperature ($^\circ$C)', fontsize=20)
                        line_style = '-'
                        secondary_axis_label = 'Temperature ($^\circ$F)'
                        secondary_axis_scale = np.float(info[axis_scale][test_name]) * 9/5 + 32
                        plot_temp = False

                    # Plot velocities
                    elif plot_vel:
                        conv_inch_h2o = 0.4
                        conv_pascal = 248.8
                        zero_voltage = np.mean(current_channel_data[0:pre_test_time])  # Get zero voltage from pre-test data
                        pressure = conv_inch_h2o * conv_pascal * (current_channel_data - zero_voltage)  # Convert voltage to pascals
                        if int(info['Test Number'][test_name]) >= 91 and 'East' in test_name and 'BDP A7' in group:
                            current_channel_data = conv_inch_h2o * conv_pascal * (current_channel_data - zero_voltage)
                            plt.ylabel('Pressure (Pa)', fontsize=20)
                        else:
                            current_channel_data = 0.0698 * np.sqrt(np.abs(pressure) * (data['TC_' + channel[4:]] + 273.15)) * np.sign(pressure)
                            plt.ylabel('Velocity (m/s)', fontsize=20)
                        line_style = '-'
                        secondary_axis_label = 'Velocity (mph)'
                        secondary_axis_scale = np.float(info[axis_scale][test_name]) * 2.23694
                        plot_vel = False

                    # Plot heat fluxes
                    elif plot_HF:
                        zero_voltage = np.mean(current_channel_data[0:pre_test_time])  # Get zero voltage from pre-test data
                        current_channel_data = (current_channel_data - zero_voltage) * calibration_slope + calibration_intercept
                        plt.ylabel('Heat Flux (kW/m$^2$)', fontsize=20)
                        if ' H' in channel or 'HF' in channel or 'Heat Flux' in channel:
                            line_style = '-'
                        elif ' V' in channel or 'RAD' in channel or 'Radiometer' in channel:
                            line_style = '--'
                        plot_HF = False

                    # Plot pressures
                    elif plot_press:
                        conv_inch_h2o = 0.4
                        conv_pascal = 248.8
                        zero_voltage = np.mean(current_channel_data[0:pre_test_time])  # Convert voltage to pascals
                        current_channel_data = conv_inch_h2o * conv_pascal * (current_channel_data - zero_voltage)  # Get zero voltage from pre-test data
                        plt.ylabel('Pressure (Pa)', fontsize=20)
                        line_style = '-'
                        plot_press = False

                    # Plot gas measurements
                    elif plot_gas:
                        if test_year == '2015':
                            zero_voltage = np.mean(current_channel_data[0:pre_test_time])
                            if int(test_name[5:-12]) >= 45:
                                if 'Carbon Dioxide ' in channel:
                                    current_channel_data = (current_channel_data-zero_voltage) * 10/(5.-zero_voltage)
                                elif 'Carbon Monoxide ' in channel:
                                    current_channel_data = (current_channel_data-zero_voltage) * 5.0/(5.-zero_voltage)
                                else:
                                    calibration_slope = 20.9/(zero_voltage-1.)
                                    current_channel_data = current_channel_data * 4.18 * 1.2
                            else:
                                if 'Carbon ' in channel:
                                    current_channel_data = (current_channel_data-zero_voltage) * calibration_slope + calibration_intercept
                                else:
                                    calibration_slope = 20.95/(zero_voltage-1.)
                                    current_channel_data = (current_channel_data-1.) * calibration_slope
                        elif test_year == '2014':
                            quantity = current_channel_data * calibration_slope + calibration_intercept
                        plt.ylabel('Concentration (%)', fontsize=20)
                        line_style = '-'
                        plot_gas = False

                    # Plot hose pressure
                    elif plot_hose:
                        # Skip data other than sensors on 2.5 inch hoseline
                        if '2p5' not in channel:
                            continue
                        current_channel_data = current_channel_data * calibration_slope + calibration_intercept
                        plt.ylabel('Pressure (psi)', fontsize=20)
                        line_style = '-'
                        axis_scale = 'Y Scale HOSE'
                        plot_hose = False

                    t = data['Time']
                    line_width = 2
                    # Save converted channel data back to exp. dataframe
                    data[channel] = current_channel_data

                # Plot channel data or save channel data for later usage, depending on plot mode
                if plot_mode == 'figure':
                    plt.plot(t, current_channel_data, 
                        lw=line_width, marker=next(plot_markers), markevery=int((end_of_test - start_of_test)/10),
                        mew=1.5, mec='none', ms=7, ls=line_style, label=channel.replace('_', ' '))
                    plots_exist = True

                elif plot_mode == 'video':
                    # Save quantities for later video plotting
                    video_time = t
                    video_plots[channel] = current_channel_data
                    plots_exist = True

            if test_type == 'HOSE':
                if all_channel_plot:
                    fig_name = hose_fig_dir + test_name + '_' + group.replace(' ', '_') + '.pdf'
                    save_hose_plot(x_max_index, y_max, y_min, start_plot, end_data, group, fig_name, 'all channels')
                    y_min = 0
                    y_max = 0
                    x_max_index = 0
                if result_file or group_avg_plot:
                    # add column for avg velocity of all channels in the group
                    channel_avg = [] 
                    for index, row in group_data.iterrows():
                        channel_avg.append(np.mean(row[1:]))
                    group_data['Avg'] = channel_avg 
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

                    if result_file:
                        # Saves results .csv file for sensor group
                        group_results.to_csv(results_dir + test_name + '_' + group.replace(' ', '_') + '_averages.csv')
                        print '  Saving ' + group.replace(' ', '_') + ' averages in result file'

                    if group_avg_plot:
                        plt.close('all')
                        fig = plt.figure()
                        fig_name = hose_fig_dir + test_name + '_' + group.replace(' ', '_') + '_avg.pdf'
                        plot_markers = cycle(['s', 'o', '^', 'd', 'h', 'p','v','8','D','*','<','>','H'])
                        
                        avg_vel = group_data['Avg'].iloc[start_plot:end_data]
                        avg_vel = pd.rolling_mean(avg_vel, 5)
                        avg_vel = avg_vel.fillna(method='bfill')
                        
                        y_max = max(avg_vel)
                        y_min = min(avg_vel)
                        x_max_index = group_data['Time'][avg_vel.idxmax(y_max)]-start_plot

                        plt.plot(t, avg_vel, 
                            marker=next(plot_markers), markevery=int((end_data - start_plot)/10), mew=1.5, mec='none', ms=7, 
                            lw=1.5, ls=line_style, label=group + ' Avg')

                        save_hose_plot(x_max_index, y_max, y_min, start_plot, end_data, group, fig_name, 'group avgs')
                        y_min = 0
                        y_max = 0

            else:
                # Skip plot quantity if there are no plots to show
                if plots_exist:
                    plots_exist = False
                else:
                    continue

                # Plot options for figure plotting
                if plot_mode == 'figure':
                    # Scale y-axis limit based on specified range in test description file
                    if axis_scale == 'Y Scale BDP':
                        plt.ylim([-np.float(info[axis_scale][test_name]), np.float(info[axis_scale][test_name])])
                    elif axis_scale == 'Y Scale PRESSURE':
                        plt.ylim([-np.float(info[axis_scale][test_name]), np.float(info[axis_scale][test_name])])
                    else:
                        plt.ylim([0, np.float(info[axis_scale][test_name])])

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

                    # Secondary y-axis parameters
                    if secondary_axis_label:
                        ax2 = ax1.twinx()
                        ax2.set_ylabel(secondary_axis_label, fontsize=20)
                        plt.xticks(fontsize=16)
                        plt.yticks(fontsize=16)
                        if axis_scale == 'Y Scale BDP':
                            ax2.set_ylim([-secondary_axis_scale, secondary_axis_scale])
                        else:
                            ax2.set_ylim([0, secondary_axis_scale])

                    try:
                        # Add vertical lines and labels for timing information (if available)
                        ax3 = ax1.twiny()
                        ax3.set_xlim(ax1_xlims)
                        # Remove NaN items from event timeline
                        events = all_times[test_name].dropna()
                        # Ignore events that are commented starting with a pound sign
                        events = events[~events.str.startswith('#')]
                        [plt.axvline(_x - start_of_test, color='0.50', lw=1) for _x in events.index.values]
                        ax3.set_xticks(events.index.values - start_of_test)
                        plt.setp(plt.xticks()[1], rotation=60)
                        ax3.set_xticklabels(events.values, fontsize=8, ha='left')
                        plt.xlim([0, end_of_test - start_of_test])
                        # Increase figure size for plot labels at top
                        fig.set_size_inches(10, 6)
                    except:
                        pass

                    plt.legend(handles1, labels1, loc='upper left', fontsize=8, handlelength=3)

                    # Save plot to file
                    if test_year == '2015':
                        print '     Plotting ' + group.replace(' ', '_')
                        plt.savefig(save_dir + test_name + '_' + group.replace(' ', '_') + '.pdf')
                    elif test_year == '2014':
                        print '     Plotting ' + group[0].rstrip('_')
                        plt.savefig('../Figures/Script_Figures/' + test_name + '_' + group[0].rstrip('_') + '.pdf')
                    plt.close('all')

        plt.close('all')
        print

        # if test_year == '2015':
        #     # Rename data column headers from device names to descriptive channel names for reduced data file
        #     old_name = channel_list.index
        #     new_name = channel_list['Channel Name']
        #     channel_name_mapping = dict(zip(old_name, new_name))
        #     data.rename(columns=channel_name_mapping, inplace=True)

        # # Write offset times and converted quantities back to reduced exp. data file
        # data.to_csv(data_dir + test_name + '_Reduced.csv')

        # if plot_mode == 'video':
        #     rcParams.update({'figure.autolayout': True,
        #                      'axes.facecolor': 'black',
        #                      'figure.facecolor': 'black',
        #                      'figure.edgecolor': 'black',
        #                      'savefig.facecolor': 'black',
        #                      'savefig.edgecolor': 'black',
        #                      'axes.edgecolor': 'white',
        #                      'axes.labelcolor': 'white',
        #                      'lines.color': 'white',
        #                      'grid.color': 'white',
        #                      'patch.edgecolor': 'white',
        #                      'text.color': 'white',
        #                      'xtick.color': 'white',
        #                      'ytick.color': 'white'})

        #     # Save plot frames to file
        #     for frame_number, frame_time in enumerate(video_time):
        #         # Constrain plots to positive times less than the upper y-axis limit
        #         if (frame_time >= 0) and (frame_time <= video_xlim_upper):
        #             print ('Plotting Frame:', frame_time)
        #             fig = plt.figure()
        #             for channel_number, channel_name in enumerate(video_plots):
        #                 video_data = video_plots[channel_name] * video_rescale_factor + video_rescale_offset
        #                 plt.plot(video_time[:frame_number],
        #                          video_data[:frame_number],
        #                          lw=4,
        #                          color=video_line_colors[channel_number])
        #             ax1 = plt.gca()
        #             ax1.spines['top'].set_visible(False)
        #             ax1.spines['right'].set_visible(False)
        #             ax1.xaxis.set_ticks_position('none')
        #             ax1.yaxis.set_ticks_position('none')
        #             plt.xlim([video_xlim_lower, video_xlim_upper])
        #             plt.ylim([video_ylim_lower, video_ylim_upper])
        #             plt.xlabel('Time (s)', fontsize=24, fontweight='bold')
        #             plt.ylabel(video_ylabel, fontsize=24, fontweight='bold')
        #             plt.xticks(fontsize=20, fontweight='bold')
        #             plt.yticks(fontsize=20, fontweight='bold')
        #             ### Begin custom plot code
        #             plt.text(71, 20, 'Position 1 Vertical', color='cyan', fontsize=16, fontweight='bold', ha='center')
        #             plt.text(82, 18, 'Position 1 Horizontal', color='green', fontsize=16, fontweight='bold', ha='center')
        #             plt.text(54, 16, 'Interior Mask', color='yellow', fontsize=16, fontweight='bold', ha='center')
        #             if frame_time >= 271:
        #                 plt.axvline(x=271,linestyle='-',color = 'white')
        #             if frame_time >= 295:
        #                 plt.axvline(x=295,linestyle='-',color = 'white')
        #             #### End custom plot code
        #             plt.savefig(save_dir + video_test_name + '_' + str(frame_time) + '.png')
        #             plt.close('all')

