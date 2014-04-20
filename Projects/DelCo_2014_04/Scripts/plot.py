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
data_dir = '../Experimental_Data/HOSE/'

# Location of scaling conversion file
scaling_file = '../DAQ_Files/Delco_DAQ_Channel_List.csv'

timings_file = '../Experimental_Data/HOSE/All_Times.csv'

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

#  ================
#  = Read in data =
#  ================

scaling = pd.read_csv(scaling_file, index_col=2)
timings = pd.read_csv(timings_file, index_col=0)

#  ===============================
#  = Loop through all data files =
#  ===============================

for f in os.listdir(data_dir):
    if f.endswith('.csv'):

        # Skip files with time information
        if 'times' in f.lower():
            continue

        test_name = f[:-4]
        print 'Test ' + test_name

        #  ================
        #  = Read in data =
        #  ================

        data = np.genfromtxt(data_dir + f, delimiter=',', names=True)

        #  ============
        #  = Plotting =
        #  ============

        # Generate a plot for each quantity group
        for group in sensor_groups:
            print 'Plotting ', group

            fig = figure()
            t = data['Time']

            for channel in data.dtype.names[2:]:

                if any([substring in channel for substring in group]):

                    scale_factor = float(scaling['Calibration'][channel])

                    # Scale channel and set plot options depending on quantity
                    # Plot temperatures
                    if 'TC_' in channel:
                        quantity = data[channel] * scale_factor
                        ylabel('Temperature ($^\circ$C)', fontsize=20)
                        ylim([0, np.max(quantity*1.2)])
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
                    # Plot heat fluxes
                    if any([substring in channel for substring in heat_flux_quantities]):
                        quantity = data[channel] * scale_factor
                        ylabel('Heat Flux (kW/m$^2$)', fontsize=20)
                        ylim([0, np.max(quantity*1.2)])
                    # Plot gas measurements
                    if any([substring in channel for substring in gas_quantities]):
                        quantity = data[channel] * scale_factor
                        ylabel('Concentration (%)', fontsize=20)
                        ylim([0, np.max(quantity*1.2)])
                    # Plot hose pressure and flow
                    if 'HOSE_' in channel:
                        quantity = data[channel] * scale_factor
                        ylabel('Pressure (psi)', fontsize=20)
                        ylim([0, np.max(quantity*1.2)])

                    plot(t, quantity, lw=2, label=channel)

            ax1 = gca()
            legend(loc='lower right', fontsize=8)
            xlabel('Time', fontsize=20)
            xticks(fontsize=16)
            yticks(fontsize=16)
            grid(True)

            try:
                # Add vertical lines for timing information (if available)
                for index, row in timings.iterrows():
                    if pd.isnull(row[test_name]):
                        continue
                    axvline(index, color='k', lw=2)

                # Add secondary x-axis labels for timing information
                ax2 = ax1.twiny()
                ax2.set_xticks(timings[test_name].dropna().index)
                setp(xticks()[1], rotation=60)
                ax2.set_xticklabels(timings[test_name].dropna().values, fontsize=10, ha='left')
            except:
                pass

            # Save to appropriate plot figure directory
            if 'PPV_' in test_name:
                folder_name = 'PPV/'
            elif 'HOSE_' in test_name:
                folder_name = 'HOSE/'

            savefig('../Figures/' + folder_name + test_name + '_' + group[0].rstrip('_') + '.pdf')
            close('all')
