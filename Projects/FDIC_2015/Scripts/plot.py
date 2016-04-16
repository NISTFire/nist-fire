# -*- coding: utf-8 -*-
from __future__ import unicode_literals
#!/usr/bin/env python

import os
import collections
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from itertools import cycle

from matplotlib import rcParams
rcParams.update({'figure.autolayout': True})

#  =================
#  = User Settings =
#  =================

# Choose Test Number
current_test = 'Test_2_04202015'

# Plot mode: figure or video
plot_mode = 'figure'

# Location of experimental data files
data_dir = '../Experimental_Data/'

# Location of file with timing information
all_times_file = '../Experimental_Data/All_Times.csv'

# Location of scaling conversion files
scaling_file_day1 = '../DAQ_Files/Day1_DAQ_Channel_List.csv'
scaling_file_day2 = '../DAQ_Files/Day2_DAQ_Channel_List.csv'
scaling_file_day2_2 = '../DAQ_Files/Day2_DAQ_Channel_List_2.csv'

# Location of test description file
info_file = '../Experimental_Data/Description_of_Experiments.csv'

# Location to save/output figures
if plot_mode == 'figure':
    save_dir = '../Figures/Script_Figures/'
elif plot_mode == 'video':
    save_dir = '../Figures/Video_Figures/'

# Time averaging window for data smoothing
data_time_averaging_window = 5

# Duration of pre-test time for bi-directional probes and heat flux gauges (s)
pre_test_time = 60

# Load exp. timings and description file
all_times = pd.read_csv(all_times_file)
all_times = all_times.set_index('Time')
info = pd.read_csv(info_file, index_col=2)

# Files to skip
skip_files = ['_times', '_reduced', 'description_',]

#  ===================
#  = Video Plot Mode =
#  ===================

video_test_name = 'Test_1_04202015'
video_groups = ['Heat Flux']
video_channels = ['Heat Flux 1 V West','Heat Flux 1 H West','Heat Flux Mask']
video_line_colors = ['yellow', 'cyan', 'green']
video_ylabel = 'Heat Flux (kW/m$^2$)'
video_rescale_factor = 1
video_rescale_offset = 0
video_xlim_lower, video_xlim_upper, video_ylim_lower, video_ylim_upper = [0, 400, 0, 30]
video_plots = collections.OrderedDict()

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
        print ('Test ' + test_name)

        # Option to specify which test is run
        # if test_name != current_test:
        #   continue

        # If video plot mode is enabled, then plot from only one test
        if plot_mode == 'video':
            if video_test_name not in test_name:
                continue

        # Load exp. scaling file
        if '04202015' in test_name:
            channel_list_file = scaling_file_day1
        elif '04212015' in test_name:
            if int(test_name[5:-9]) < 7:
                channel_list_file = scaling_file_day2
            else:
                channel_list_file = scaling_file_day2_2
        channel_list = pd.read_csv(channel_list_file)
        channel_list = channel_list.set_index('Channel Name')
        channel_groups = channel_list.groupby('Group Name')

        # Read in test times to offset plots
        start_of_test = info['Start of Test'][test_name]
        end_of_test = info['End of Test'][test_name]
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

        #  ============
        #  = Plotting =
        #  ============

        # Generate a plot for each quantity group
        for group in channel_groups.groups:
            # Skip excluded groups listed in test description file
            if any([substring in group for substring in info['Excluded Groups'][test_name].split('|')]):
                continue

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

            for channel in channel_groups.get_group(group).index.values:

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

                # Scale channel and set plot options depending on quantity
                current_channel_data = data[channel_list['Device Name'][channel]]
                calibration_slope = float(channel_list['Calibration Slope'][channel])
                calibration_intercept = float(channel_list['Calibration Intercept'][channel])
                secondary_axis_label = None  # Reset secondary axis variable

                # Plot temperatures
                if channel_list['Measurement Type'][channel] == 'Temperature':
                    current_channel_data = current_channel_data * calibration_slope + calibration_intercept
                    plt.ylabel('Temperature ($^\circ$C)', fontsize=20)
                    line_style = '-'
                    axis_scale = 'Y Scale TC'
                    secondary_axis_label = 'Temperature ($^\circ$F)'
                    secondary_axis_scale = np.float(info[axis_scale][test_name]) * 9/5 + 32

                # Plot velocities
                if channel_list['Measurement Type'][channel] == 'Velocity':
                    conv_inch_h2o = 0.4
                    conv_pascal = 124.54
                    if test_name[5:-9] == '2' and 'BDP Stairwell Door 0.46 m BS' in channel:
                        zero_voltage = np.mean(current_channel_data[836:1000])
                    else:
                        zero_voltage = np.mean(current_channel_data[0:pre_test_time])  # Get zero voltage from pre-test data
                    pressure = conv_inch_h2o * conv_pascal * (current_channel_data - zero_voltage)  # Convert voltage to pascals
                    # Calculate velocity
                    current_channel_data = 0.0698 * np.sqrt(np.abs(pressure) *
                                                            (data[channel_list['Device Name']['TC ' + channel[4:]]] + 273.15)) * np.sign(pressure)
                    if test_name[5:-9] == '1' and 'BDP D Side Garage Door' in group:
                        current_channel_data=-1*current_channel_data
                    if test_name[5:-9] == '2' and 'BDP Stairwell Door' in group:
                        current_channel_data=-1*current_channel_data
                    if test_name[5:-9] == '5' and 'BDP Frontdoor' in group:
                        current_channel_data=-1*current_channel_data
                    if test_name[5:-9] == '6' and 'BDP Bedroom 4 Door 0.76 m BS' in channel:
                        current_channel_data=-1*current_channel_data

                    plt.ylabel('Velocity (m/s)', fontsize=20)
                    line_style = '-'
                    axis_scale = 'Y Scale BDP'
                    secondary_axis_label = 'Velocity (mph)'
                    secondary_axis_scale = np.float(info[axis_scale][test_name]) * 2.23694

                # Plot heat fluxes
                if channel_list['Measurement Type'][channel] == 'Heat Flux':
                    zero_voltage = np.mean(current_channel_data[0:pre_test_time])  # Get zero voltage from pre-test data
                    current_channel_data = (current_channel_data - zero_voltage) * calibration_slope + calibration_intercept
                    plt.ylabel('Heat Flux (kW/m$^2$)', fontsize=20)
                    if ' H' in channel:
                        line_style = '-'
                    elif ' V' in channel:
                        line_style = '--'
                    if 'Radiometer' in channel:
                        line_style = '--'
                    elif 'Heat Flux' in channel:
                        line_style = '-'
                    axis_scale = 'Y Scale HF'

                # Plot pressures
                if channel_list['Measurement Type'][channel] == 'Pressure':
                    conv_inch_h2o = 0.4
                    conv_pascal = 124.54
                    zero_voltage = np.mean(current_channel_data[0:pre_test_time])  # Convert voltage to pascals
                    current_channel_data = conv_inch_h2o * conv_pascal * (current_channel_data - zero_voltage)  # Get zero voltage from pre-test data

                    plt.ylabel('Pressure (Pa)', fontsize=20)
                    line_style = '-'
                    axis_scale = 'Y Scale PRESSURE'

                # Plot gas measurements
                if channel_list['Measurement Type'][channel] == 'Gas':
                    zero_voltage = np.mean(current_channel_data[0:pre_test_time])
                    if 'Carbon ' in channel:
                        current_channel_data = (current_channel_datac) * calibration_slope + calibration_intercept
                    else:
                        current_channel_data = (current_channel_data) * calibration_slope
                    plt.ylabel('Concentration (%)', fontsize=20)
                    line_style = '-'
                    axis_scale = 'Y Scale GAS'

                # Plot channel data or save channel data for later usage, depending on plot mode
                if plot_mode == 'figure':
                    plt.plot(data['Time'],
                             current_channel_data,
                             lw=2,
                             marker=next(plot_markers),
                             markevery=int((end_of_test - start_of_test)/10),
                             mew=1.5,
                             mec='none',
                             ms=7,
                             ls=line_style,
                             label=channel)
                    # Save converted channel data back to exp. dataframe
                    data[channel_list['Device Name'][channel]] = current_channel_data
                    plots_exist = True

                elif plot_mode == 'video':
                    # Save quantities for later video plotting
                    video_time = data['Time']
                    video_plots[channel] = current_channel_data
                    plots_exist = True
            # Skip plot quantity if there are no plots to show
            if plots_exist:
                plots_exist = False
            else:
                continue

            # Skip plot quantity if disabled in test description file
            if info[axis_scale][test_name] == 'None':
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
                if test_name[5:-9] == '5' and 'Pressure' in group:
                    plt.legend(handles1, labels1, loc='upper right', fontsize=8, handlelength=3)
                elif test_name[5:-9] == '3b' and 'TC' in group:
                    plt.legend(handles1, labels1, loc='upper right', fontsize=8, handlelength=3)               
                else:
                    plt.legend(handles1, labels1, loc='upper left', fontsize=8, handlelength=3)

                # Save plot to file
                print ('Plotting', group)
                plt.savefig(save_dir + test_name + '_' + group.replace(' ', '_') + '.pdf')
                plt.close('all')

        plt.close('all')
        print()

        # Rename data column headers from device names to descriptive channel names for reduced data file
        old_name = channel_list['Device Name']
        new_name = channel_list.index
        channel_name_mapping = dict(zip(old_name, new_name))
        data.rename(columns=channel_name_mapping, inplace=True)

        # Write offset times and converted quantities back to reduced exp. data file
        data.to_csv(data_dir + test_name + '_Reduced.csv')

        if plot_mode == 'video':
            rcParams.update({'figure.autolayout': True,
                             'axes.facecolor': 'black',
                             'figure.facecolor': 'black',
                             'figure.edgecolor': 'black',
                             'savefig.facecolor': 'black',
                             'savefig.edgecolor': 'black',
                             'axes.edgecolor': 'white',
                             'axes.labelcolor': 'white',
                             'lines.color': 'white',
                             'grid.color': 'white',
                             'patch.edgecolor': 'white',
                             'text.color': 'white',
                             'xtick.color': 'white',
                             'ytick.color': 'white'})

            # Save plot frames to file
            for frame_number, frame_time in enumerate(video_time):
                # Constrain plots to positive times less than the upper y-axis limit
                if (frame_time >= 0) and (frame_time <= video_xlim_upper):
                    print ('Plotting Frame:', frame_time)
                    fig = plt.figure()
                    for channel_number, channel_name in enumerate(video_plots):
                        video_data = video_plots[channel_name] * video_rescale_factor + video_rescale_offset
                        plt.plot(video_time[:frame_number],
                                 video_data[:frame_number],
                                 lw=4,
                                 color=video_line_colors[channel_number])
                    ax1 = plt.gca()
                    ax1.spines['top'].set_visible(False)
                    ax1.spines['right'].set_visible(False)
                    ax1.xaxis.set_ticks_position('none')
                    ax1.yaxis.set_ticks_position('none')
                    plt.xlim([video_xlim_lower, video_xlim_upper])
                    plt.ylim([video_ylim_lower, video_ylim_upper])
                    plt.xlabel('Time (s)', fontsize=24, fontweight='bold')
                    plt.ylabel(video_ylabel, fontsize=24, fontweight='bold')
                    plt.xticks(fontsize=20, fontweight='bold')
                    plt.yticks(fontsize=20, fontweight='bold')
                    ### Begin custom plot code
                    plt.text(71, 20, 'Position 1 Vertical', color='cyan', fontsize=16, fontweight='bold', ha='center')
                    plt.text(82, 18, 'Position 1 Horizontal', color='green', fontsize=16, fontweight='bold', ha='center')
                    plt.text(54, 16, 'Interior Mask', color='yellow', fontsize=16, fontweight='bold', ha='center')
                    if frame_time >= 271:
                        plt.axvline(x=271,linestyle='-',color = 'white')
                    if frame_time >= 295:
                        plt.axvline(x=295,linestyle='-',color = 'white')
                    #### End custom plot code
                    plt.savefig(save_dir + video_test_name + '_' + str(frame_time) + '.png')
                    plt.close('all')

