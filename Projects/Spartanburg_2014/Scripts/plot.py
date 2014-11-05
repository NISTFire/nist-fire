#!/usr/bin/env python

from __future__ import division

import os
import numpy as np
import pandas as pd
from pylab import *

from matplotlib import rcParams
rcParams.update({'figure.autolayout': True})

#  =================
#  = User Settings =
#  =================

# Plot mode: figure or video
plot_mode = 'figure'

# Location of experimental data files
data_dir = '../Experimental_Data/'

# Location of file with timing information
timings_file = '../Experimental_Data/All_Times.csv'

# Location of test description file
info_file = '../Experimental_Data/Description_of_Experiments.csv'

# Duration of pre-test time for bi-directional probes and heat flux gauges (s)
pre_test_time = 60

# List of sensor groups for each plot
sensor_groups = [['TC_A1_'], ['TC_A2_'], ['TC_A3_'], ['TC_A4_'],
                 ['TC_A5_'], ['TC_A6_'], ['TC_A7_'], ['TC_A8_'],
                 ['TC_S_1', 'TC_S_2', 'TC_S_3', 'TC_S_4',
                  'TC_S_5', 'TC_S_6', 'TC_S_7', 'TC_S_8'],
                 ['TC_Ignition'],
                 ['HF_'],
                 ['Voltage_'],
                 ['P_S_1', 'P_S_2', 'P_S_3', 'P_S_4', 'P_S_5',
                  'P_S_6', 'P_S_7', 'P_S_8', 'P_S_9'],
                 ['GAS_', 'CO_', 'CO2_', 'O2_']]

# Common quantities for y-axis labelling
gas_quantities = ['CO_', 'CO2_', 'O2_']

# Load exp. timing and description files
timings = pd.read_csv(timings_file, index_col=0)
info = pd.read_csv(info_file, index_col=1)

# Files to skip
skip_files = ['_times', '_reduced', 'description_']

# Location to save/output figures
if plot_mode == 'figure':
    save_dir = '../Figures/Script_Figures/'
elif plot_mode == 'video':
    save_dir = '../Figures/Video_Figures/'

#  ===================
#  = Video Plot Mode =
#  ===================

video_test_name = '286_College_Test_1'
video_groups = ['TC_A3_']
video_channels = ['TC_A3_1', 'TC_A3_5']
video_line_colors = ['yellow', 'cyan']
video_ylabel = 'Temperature ($^\circ$F)'
video_rescale_factor = 9/5
video_rescale_offset = 32
xlim_lower, xlim_upper, ylim_lower, ylim_upper = [0, 150, 0, 300]
video_plots = {}

#  ===============================
#  = Loop through all data files =
#  ===============================

for f in os.listdir(data_dir):
    if f.endswith('.csv'):

        # Skip files with time information or reduced data files
        if any([substring in f.lower() for substring in skip_files]):
            continue

        # Strip group and test name from file name
        group_name = f.split('_Test_', 1)[0]
        test_name = f[:-4]
        print 'Test ' + test_name

        # If video plot mode is enabled, then plot from only one test
        if plot_mode == 'video':
            if video_test_name not in test_name:
                continue

        # Location of channel list file w/ scaling and channel name information
        channel_list_file = '../DAQ_Files/' + group_name + '_DAQ_Channel_List.csv'
        channel_list = pd.read_csv(channel_list_file, index_col=2)

        # Load exp. data file
        data = pd.read_csv(data_dir + f, index_col=0)

        # Read in test times to offset plots
        start_of_test = info['Start of Test'][test_name]
        end_of_test = info['End of Test'][test_name]

        # Offset data time to start of test
        t = data['Time'].values - start_of_test

        # Save converted time back to dataframe
        data['Time'] = t

        #  ============
        #  = Plotting =
        #  ============

        # Generate a plot for each quantity group
        for group in sensor_groups:

            # Skip excluded groups listed in test description file
            if any([substring in group for substring in info['Excluded Groups'][test_name].split('|')]):
                continue

            # If video plot mode is enabled, then plot only specified groups
            if plot_mode == 'video':
                if any([substring in group for substring in video_groups]):
                    pass
                else:
                    continue

            fig = figure()

            for channel in data.columns[1:]:

                # Skip excluded channels listed in test description file
                if any([substring in channel for substring in info['Excluded Channels'][test_name].split('|')]):
                    continue

                # Skip plot quantity if channel name is blank
                if pd.isnull(channel_list['Test Specific Name'][channel]):
                    continue

                # If video plot mode is enabled, then plot only specified channels
                if plot_mode == 'video':
                    if any([substring in channel for substring in video_channels]):
                        pass
                    else:
                        continue

                if any([substring in channel for substring in group]):
                    calibration_slope = float(channel_list['Calibration Slope'][channel])
                    calibration_intercept = float(channel_list['Calibration Intercept'][channel])

                    # Scale channel and set plot options depending on quantity
                    # Plot temperatures
                    if 'TC_' in channel:
                        plt.rc('axes', color_cycle=['k', 'r', 'g', 'b', '0.75', 'c', 'm', 'y'])
                        quantity = data[channel] * calibration_slope + calibration_intercept
                        ylabel('Temperature ($^\circ$C)', fontsize=20)
                        line_style = '-'
                        axis_scale = 'Y Scale TC'

                    # Plot velocities
                    if 'BDP_' in channel:
                        plt.rc('axes', color_cycle=['k', 'r', 'g', 'b', '0.75', 'c', 'm', 'y'])
                        conv_inch_h2o = 0.4
                        conv_pascal = 248.8

                        # Convert voltage to pascals
                        # Get zero voltage from pre-test data
                        zero_voltage = np.mean(data[channel][0:pre_test_time])
                        pressure = conv_inch_h2o * conv_pascal * (data[channel] - zero_voltage)

                        # Calculate velocity
                        quantity = 0.0698 * np.sqrt(np.abs(pressure) *
                                                    (data['TC_' + channel[4:]] + 273.15)) * np.sign(pressure)
                        ylabel('Velocity (m/s)', fontsize=20)
                        line_style = '-'
                        axis_scale = 'Y Scale BDP'

                    # Plot heat fluxes
                    if 'HF_' in channel:
                        plt.rc('axes', color_cycle=['k', 'k',
                                                    'r', 'r',
                                                    'g', 'g',
                                                    'b', 'b',
                                                    'c', 'c'])

                        # Get zero voltage from pre-test data
                        zero_voltage = np.mean(data[channel][0:pre_test_time])
                        quantity = (data[channel] - zero_voltage) * calibration_slope + calibration_intercept
                        ylabel('Heat Flux (kW/m$^2$)', fontsize=20)
                        if 'HF' in channel:
                            line_style = '-'
                        elif 'RAD' in channel:
                            line_style = '--'
                        axis_scale = 'Y Scale HF'

                    # Plot pressures
                    if 'P_' in channel:
                        plt.rc('axes', color_cycle=['k', 'r', 'g', 'b', '0.75', 'c', 'm', 'y'])
                        conv_inch_h2o = 0.4
                        conv_pascal = 248.8

                        # Convert voltage to pascals
                        # Get zero voltage from pre-test data
                        zero_voltage = np.mean(data[channel][0:pre_test_time])
                        quantity = conv_inch_h2o * conv_pascal * (data[channel] - zero_voltage)

                        ylabel('Pressure (Pa)', fontsize=20)
                        line_style = '-'
                        axis_scale = 'Y Scale PRESSURE'

                    # Plot gas measurements
                    if any([substring in channel for substring in gas_quantities]):
                        plt.rc('axes', color_cycle=['k', 'r', 'g', 'b', '0.75', 'c', 'm', 'y'])
                        quantity = data[channel] * calibration_slope + calibration_intercept
                        ylabel('Concentration (%)', fontsize=20)
                        line_style = '-'
                        axis_scale = 'Y Scale GAS'

                    # Plot hose pressure
                    if 'HOSE_' in channel:
                        plt.rc('axes', color_cycle=['k', 'r', 'g', 'b', '0.75', 'c', 'm', 'y'])
                        # Skip data other than sensors on 2.5 inch hoseline
                        if '2p5' not in channel:
                            continue
                        quantity = data[channel] * calibration_slope + calibration_intercept
                        ylabel('Pressure (psi)', fontsize=20)
                        line_style = '-'
                        axis_scale = 'Y Scale HOSE'

                    # Plot quantity or save quantity for later usage, depending on plot mode
                    if plot_mode == 'figure':
                        plot(t, quantity, lw=1.5, ls=line_style, label=channel_list['Test Specific Name'][channel])
                        # Save converted quantity back to exp. dataframe
                        data[channel] = quantity
                    elif plot_mode == 'video':
                        # Save quantities for later video plotting
                        video_time = t
                        video_plots[channel] = quantity

            # Skip plot quantity if disabled in test description file
            if info[axis_scale][test_name] == 'None':
                continue

            # Plot options for figure plotting
            if plot_mode == 'figure':
                # Scale y-axis limit based on specified range in test description file
                if axis_scale == 'Y Scale BDP':
                    ylim([-np.float(info[axis_scale][test_name]), np.float(info[axis_scale][test_name])])
                else:
                    ylim([0, np.float(info[axis_scale][test_name])])

                # Set axis options, legend, tickmarks, etc.
                ax1 = gca()
                xlim([0, end_of_test - start_of_test])
                ax1.xaxis.set_major_locator(MaxNLocator(8))
                ax1_xlims = ax1.axis()[0:2]
                grid(True)
                xlabel('Time (s)', fontsize=20)
                xticks(fontsize=16)
                yticks(fontsize=16)
                legend(loc='upper right', fontsize=8)
                try:
                    # Add vertical lines and labels for timing information (if available)
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
                    fig.set_size_inches(8, 8)
                except:
                    pass

            if plot_mode == 'figure':
                # Save plot to file
                print 'Plotting ', group
                savefig(save_dir + test_name + '_' + group[0].rstrip('_') + '.pdf')
                close('all')
        
        close('all')
        print

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

            # Save plot to file
            for frame_number, frame_time in enumerate(video_time):
                # Constrain plots to positive times less than the upper y-axis limit
                if (frame_time >= 0) and (frame_time <= xlim_upper):
                    print 'Plotting Frame:', frame_time
                    fig = figure()
                    for channel_number, channel_name in enumerate(video_plots):
                        plot(video_time[:frame_number],
                             video_plots[channel_name][:frame_number] * video_rescale_factor + video_rescale_offset,
                             lw=4,
                             color=video_line_colors[channel_number])
                    ax1 = gca()
                    ax1.spines['top'].set_visible(False)
                    ax1.spines['right'].set_visible(False)
                    ax1.xaxis.set_ticks_position('none')
                    ax1.yaxis.set_ticks_position('none')
                    xlim([xlim_lower, xlim_upper])
                    ylim([ylim_lower, ylim_upper])
                    xlabel('Time (s)', fontsize=24, fontweight='bold')
                    ylabel(video_ylabel, fontsize=24, fontweight='bold')
                    xticks(fontsize=20, fontweight='bold')
                    yticks(fontsize=20, fontweight='bold')
                    # Begin custom plot code
                    text(35, 120, 'Temperature\nnear ceiling', color='yellow', fontsize=16, fontweight='bold', ha='center')
                    text(35, 30, 'Temperature\n5 feet above floor', color='cyan', fontsize=16, fontweight='bold', ha='center')
                    if frame_time >= 102:
                        text(128, 230, 'Sprinkler\nactivates at\n102 seconds', color='white', fontsize=16, fontweight='bold', ha='center')
                    # End custom plot code
                    savefig(save_dir + video_test_name + '_' + str(frame_time) + '.png')
                    close('all')
