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
specify_test = False
specific_name = 'Test_16_West_063014'

# Specify year
specify_year = False
specific_year = '2015'

# Specify structure
specify_struct = True
specific_struct = 'West'

# Specify monitor or handline
specify_type = False
specific_type = 'monitor'

# Files to skip
skip_files = ['_times', '_reduced', '_results', 'description_', 'HOSE_D']

# =============================
# = Specify files to generate =
# =============================

result_file = True         # Generate a .csv file with channel avgs for specified sensor groups
all_channel_plot = True    # Plot of individual channels in sensor group
group_avg_plot = True      # Plot of channel avg for sensor group
stream_compare_plot = True # Plot of channel avg for each stream tested during experiment

latex_table_code = False    # Print code to generate tables in LaTeX?
if(latex_table_code):       # specify table properties (if applicable)
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

#  =======================
#  = Directory Locations =
#  =======================

# Location of directories
data_dir = '../Experimental_Data/'      # Location of experimental data files
results_dir = '../Results/'     # Location to save results files 
fig_dir = '../Figures/Hose_Stream_Figures/'     # Location to save plots
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
        start_seq = 0
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
            if pd.isnull(row[test_name]):
                continue
            else:
                # if new sequence, add time to array to re-zero voltages
                if ('Monitor on,' in row[test_name]) or ('Hose on,' in row[test_name]):
                    zero_time_ls.append(index-start_time)

                if start_seq != 0:  # add information to event row
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
                    start_seq = 0
                    continue
                elif 'water off' in row[test_name].lower():
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

                start_seq = index-start_time

        group_set = {'Start': start_times_ls, 'End':end_times_ls, 'Stream':streams_ls, 
            P_or_L_heading:P_or_L_ls,'Door':door_status_ls, 'zero times':zero_time_ls}
        group_results = pd.DataFrame(group_set, 
            columns = ['Start', 'End', 'Stream', P_or_L_heading, 'Door', 'zero times'])
        return group_results
    else:
        print ('Need to write code for sorting East Tests')
        sys.exit()

def save_plot(x_max_index, y_max, y_min, start_time, end_time, group, fig_name, plot_type, tick_labels):
    plt.errorbar(x_max_index, y_max, yerr=(.18)*y_max, ecolor='k')

    ax1 = plt.gca()
    ax1.set_xlim([0, end_time])
    ax1.set_ylim(math.floor(y_min)-0.1, math.ceil(y_max)+0.1)
    ax1.xaxis.set_major_locator(plt.MaxNLocator(8))
    ax1_xlims = ax1.axis()[0:2]
    # grid(True)
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
        # Remove NaN items from event timeline
        events = all_times[test_name].dropna()
        # Ignore events that are commented starting with a pound sign
        events = events[~events.str.startswith('#')]
        tick_values = events.index.values - start_time
        if plot_type != 'stream comparison':
            tick_labels = events.values
        else:
            tick_values = tick_values[0:(len(tick_labels)-1)]
        [plt.axvline(_x, color='0.50', lw=1) for _x in tick_values]
        ax3.set_xticks(tick_values)
        plt.setp(plt.xticks()[1], rotation=60)
        ax3.set_xticklabels(tick_labels, fontsize=8, ha='left')
        plt.xlim([0, end_time])
        # Increase figure size for plot labels at top
        fig.set_size_inches(10, 6)
    except:
        pass

    plt.gca().add_artist(ax1.legend(loc='lower right', fontsize=10, frameon = True))

    # Save plot to file
    print ('  Saving plot of ' + plot_type + ' for ' + group)
    plt.savefig(fig_name)
    plt.close('all')

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
            data = pd.read_csv(data_dir + f)
            data = data.set_index('TimeStamp(s)')
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
        start_of_test = info['Start of Test'][test_name]

        # Offset data time to start of test
        data['Time'] = data['Time'].values - start_of_test

        event_times = sort_data(test_name, start_of_test, test_type)
        zero_time_ls = event_times['zero times']
        event_times = event_times.drop('zero times', axis=1)
        end_data = event_times['End'].iloc[-1]

        # List through sensor groups to analyze
        for group in channel_groups.groups:
            # Skip excluded groups listed in test description file
            if any([substring in group for substring in info['Excluded Groups'][test_name].split('|')]):
                continue
             
            group_results = event_times

            # create empty df to fill with desired channel data
            group_data = pd.DataFrame(data['Time'].iloc[0:end_data], columns = ['Time'])

            if all_channel_plot:
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
                
                plt.ylabel('Velocity (m/s)', fontsize=20)
                axis_scale = 'Y Scale BDP'
                line_style = '-'
                secondary_axis_label = 'Velocity (mph)'
                secondary_axis_scale = np.float(info[axis_scale][test_name]) * 2.23694
                y_max = 0
                y_min = 0

            for channel in channel_groups.get_group(group).index.values:
                # Skip excluded channels listed in hose_info file
                if any([substring in channel for substring in hose_info['Excluded Channels'][test_name].split('|')]):
                    continue

                # calculate initial zero voltage, create empty list for calculated velocities
                zero_start = zero_time_ls[0] - 25
                zero_end = zero_start + 20
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

                if all_channel_plot:        # plot individual channels
                    # check y min and max
                    ma_quantity = pd.rolling_mean(quantity, 5)
                    ma_quantity = ma_quantity.fillna(method='bfill')
                    if max(ma_quantity) > y_max:
                        y_max = max(ma_quantity)
                        x_max_index = group_data['Time'][ma_quantity.idxmax(y_max)]
                    if min(ma_quantity) < y_min:
                        y_min = min(ma_quantity)

                    plt.plot(group_data['Time'], ma_quantity, 
                        marker=next(plot_markers), markevery=int(len(group_data['Time'])/10),
                        mew=1.5, mec='none', ms=7, ls=line_style, lw=2, label=channel)

            # calculate channel avg at each time step add to group_data df
            channel_avg = []
            for index, row in group_data.iterrows():
                channel_avg.append(np.mean(row[1:]))
            group_data['Avg'] = channel_avg   

            if all_channel_plot:        # save plot of individual channels
                fig_name = fig_dir + test_name + '_' + group.replace(' ', '_') + '.pdf'
                save_plot(x_max_index, y_max, y_min, start_of_test, end_data, group, fig_name, 'all channels', [])
                y_min = 0
                y_max = 0

            if group_avg_plot:      # plot and save avg of all channels in group
                fig = plt.figure()
                plt.rc('axes', color_cycle=tableau20)
                plot_markers = cycle(['s', 'o', '^', 'd', 'h', 'p','v','8','D','*','<','>','H'])
                plt.ylabel('Velocity (m/s)', fontsize=20)
                axis_scale = 'Y Scale BDP'
                line_style = '-'
                secondary_axis_label = 'Velocity (mph)'
                secondary_axis_scale = np.float(info[axis_scale][test_name]) * 2.23694
                fig_dir + test_name + '_' + group.replace(' ', '_') + '_average.pdf'

                # check y min and max
                ma_quantity = pd.rolling_mean(channel_avg, 5)
                ma_quantity = ma_quantity.fillna(method='bfill')
                if max(ma_quantity) > y_max:
                    y_max = max(ma_quantity)
                    x_max_index = group_data['Time'][ma_quantity.idxmax(y_max)]
                if min(ma_quantity) < y_min:
                    y_min = min(ma_quantity)

                plt.plot(group_data['Time'], ma_quantity, 
                    marker=next(plot_markers), markevery=int(len(group_data['Time']))/10,
                    mew=1.5, mec='none', ms=7, ls=line_style, lw=2, label=channel)

                save_plot(x_max_index, y_max, y_min, start_of_test, end_data, group, fig_name, 'group avg', [])
                y_min = 0
                y_max = 0

            if stream_compare_plot:     # plot and save avg of all channels during each stream
                fig = plt.figure()
                plt.rc('axes', color_cycle=tableau20)
                plot_markers = cycle(['s', 'o', '^', 'd', 'h', 'p','v','8','D','*','<','>','H'])
                plt.ylabel('Velocity (m/s)', fontsize=20)
                axis_scale = 'Y Scale BDP'
                line_style = '-'
                secondary_axis_label = 'Velocity (mph)'
                secondary_axis_scale = np.float(info[axis_scale][test_name]) * 2.23694
                
                x_tick_labels = []
                if test_year == '2014':
                    if 'West' in test_name:
                        if test_type == 'monitor':
                            variable_list = ['near target', 'far target']
                        elif test_type == 'handline':
                            variable_list = ['fixed', 'sweeping', 'rotate CW', 'rotate CCW']
                        for variable in variable_list:
                            xtick_labels.extend('Hose on, ' + variable,'Stairwell door opened',
                                '2nd floor, W door opened', 'Doors closed')
                else:
                    
                fig_name = fig_dir + test_name + '_' + group.replace(' ', '_') + '_stream_comparison.pdf'
                save_plot(x_max_index, y_max, y_min, start_of_test, end_data, group, 
                    fig_name, 'stream comparison', xtick_labels)
                y_min = 0
                y_max = 0

            if result_file:
                group_results['Avg'] = ''
                for index, row in group_results.iterrows():
                    # grab start/end time for each event in new .csv file
                    start = row['Start'] - start_data
                    end = row['End'] - start_data
                    seq_data = group_data.iloc[start:end]
                    # Calculate average for each channel during sequence
                    for column in group_results.columns[5:]:
                        # calculate avg for each channel during event 
                        group_results.loc[index, column] = round(np.mean(seq_data[column]), 2)

                # Saves results .csv file for sensor group
                group_results.to_csv(results_dir + test_name + '_' + group.replace(' ', '_')  + 'averages.csv')
                print ('    Saving result file for ' + group)
                print
