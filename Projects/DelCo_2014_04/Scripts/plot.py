#!/usr/bin/env python

import os
import numpy as np
import pandas as pd
from pylab import *

from matplotlib import rcParams
rcParams.update({'figure.autolayout': True})

#  =================
#  = User Settings =
#  =================

# Location of experimental data files
data_dir = '../Experimental_Data/'

# Location of file with timing information
timings_file = '../Experimental_Data/All_Times.csv'

# Location of scaling conversion file
scaling_file = '../DAQ_Files/Delco_DAQ_Channel_List.csv'

# Duration of pre-test time (s)
pre_test_time = 60

# List of sensor groups for each plot
sensor_groups = [['TC_A1_'], ['TC_A2_'], ['TC_A3_'], ['TC_A4_'], ['TC_A5_'],
                 ['TC_A6_'], ['TC_A7_'], ['TC_A8_'], ['TC_A9_'], ['TC_A10_'],
                 ['TC_Ignition'],
                 ['BDP_A6_'], ['BDP_A7_'], ['BDP_A8_'], ['BDP_A9_'],
                 ['BDP_A10_'],
                 ['HF_', 'RAD_'],
                 ['GAS_', 'CO_', 'CO2', 'O2_'],
                 ['HOSE_']]

# Common quantities for y-axis labelling
heat_flux_quantities = ['HF_', 'RAD_']
gas_quantities = ['CO_', 'CO2_', 'O2_']

# Load exp. scaling file
scaling = pd.read_csv(scaling_file, index_col=2)

# Files to skip
skip_files = ['_times', '_reduced', 'description_']

#  ===============================
#  = Loop through all data files =
#  ===============================

# Load exp. timings file
timings = pd.read_csv(timings_file, index_col=0)

for f in os.listdir(data_dir):
    if f.endswith('.csv'):

        # Skip files with time information or reduced data files
        if any([substring in f.lower() for substring in skip_files]):
            continue

        test_name = f[:-4]
        print 'Test ' + test_name

        # Load exp. data file
        data = pd.read_csv(data_dir + f, index_col=1)

        #  ============
        #  = Plotting =
        #  ============

        # Generate a plot for each quantity group
        for group in sensor_groups:
            print 'Plotting ', group

            fig = figure()
            t = data.index

            quantity_max = 0

            for channel in data.columns[1:]:

                if any([substring in channel for substring in group]):

                    scale_factor = float(scaling['Calibration'][channel])

                    # Scale channel and set plot options depending on quantity
                    # Plot temperatures
                    if 'TC_' in channel:
                        quantity = data[channel] * scale_factor
                        ylabel('Temperature ($^\circ$C)', fontsize=20)
                        axis_scale = 'auto'
                    # Plot velocities
                    if 'BDP_' in channel:
                        conv_inch_h2o = 0.4;
                        conv_pascal = 248.8;
                        # Convert voltage to pascals
                        pressure = conv_inch_h2o * conv_pascal * \
                                   (data[channel] - np.mean(data[channel][0:pre_test_time]))
                        # Calculate velocity
                        quantity = 0.0698 * np.sqrt(np.abs(pressure) * \
                                   (data['TC_' + channel[4:]] + 273.15)) * np.sign(pressure)
                        ylabel('Velocity (m/s)', fontsize=20)
                        ylim([-10, 10])
                        axis_scale = 'mirror'
                    # Plot heat fluxes
                    if any([substring in channel for substring in heat_flux_quantities]):
                        quantity = data[channel] * scale_factor
                        ylabel('Heat Flux (kW/m$^2$)', fontsize=20)
                        axis_scale = 'auto'
                    # Plot gas measurements
                    if any([substring in channel for substring in gas_quantities]):
                        quantity = data[channel] * scale_factor
                        ylabel('Concentration (%)', fontsize=20)
                        axis_scale = 'auto'
                    # Plot hose pressure and flow
                    if 'HOSE_' in channel:
                        # Skip data other than sensors on 2.5 inch hoseline
                        if '2p5' not in channel:
                            continue
                        quantity = data[channel] * scale_factor
                        ylabel('Pressure (psi)', fontsize=20)
                        axis_scale = 'auto'

                    # Store maximum quantity value
                    if np.max(quantity) > quantity_max:
                        quantity_max = np.max(quantity)

                    # Save converted quantity back to exp. data array
                    data[channel] = quantity

                    plot(t, quantity, lw=1.5, label=channel, rasterized=True)

            # Scale y-axis limit based on specified option
            # auto: Scale 10% above maximum value on plot
            if axis_scale == 'auto':
                ylim([0, quantity_max*1.1])
            # mirror: Scale positive and negative values around auto scale criteria
            elif axis_scale == 'mirror':
                ylim([-quantity_max*1.1, quantity_max*1.1])

            ax1 = gca()
            grid(True)
            xlabel('Time', fontsize=20)
            xticks(fontsize=16)
            yticks(fontsize=16)
            legend(loc='lower right', fontsize=8)

            try:
                # Add vertical lines for timing information (if available)
                for index, row in timings.iterrows():
                    if pd.isnull(row[test_name]):
                        continue
                    axvline(index, color='0.50', lw=1)

                # Add secondary x-axis labels for timing information
                ax2 = ax1.twiny()
                ax2.set_xticks(timings[test_name].dropna().index)
                setp(xticks()[1], rotation=60)
                ax2.set_xticklabels(timings[test_name].dropna().values, fontsize=8, ha='left')

                # Increase figure size for plot labels at top
                fig.set_size_inches(8, 8)
            except:
                pass

            savefig('../Figures/' + test_name + '_' + group[0].rstrip('_') + '.pdf')
            close('all')

        print

        # Write converted quantities back to reduced exp. data file
        data.to_csv(data_dir + test_name + '_Reduced.csv')