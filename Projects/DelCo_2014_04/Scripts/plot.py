#!/usr/bin/env python

import numpy as np
import pandas as pd
from pylab import *

from matplotlib import rcParams
rcParams.update({'figure.autolayout': True})

#  =================
#  = User Settings =
#  =================

# Name of the test
test_name = 'PPV_YoOOlNY'

# Location of data file
data_file = '../Experimental_Data/PPV/PPV_YoOOlNY.csv'

# Location of scaling conversion file
scaling_file = '../DAQ_Files/Delco_DAQ_Channel_List.csv'

# Duration of pre-test time (s)
pre_test_time = 60

# Common quantities for y-axis labelling
heat_flux_quantities = ['HF_', 'RAD_']
gas_quantities = ['CO_', 'CO2_', 'O2_']

#  ================
#  = Read in data =
#  ================

data = np.genfromtxt(data_file, delimiter=',', names=True)
scaling = pd.read_csv(scaling_file, index_col=2)

#  ============
#  = Plotting =
#  ============

# Generate a plot for each quantity
for channel in data.dtype.names[2:]:
    print 'Plotting ' + channel 

    scale_factor = float(scaling['Calibration'][channel])

    figure()
    t = data['Time']

    # Scale channel and set plot options depending on quantity
    if 'TC_' in channel:
        quantity = data[channel] * scale_factor
        ylabel('Temperature ($^\circ$C)', fontsize=20)
        ylim([0, np.max(quantity*1.2)])
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
    if any([substring in channel for substring in heat_flux_quantities]):
        quantity = data[channel] * scale_factor
        ylabel('Heat Flux (kW/m$^2$)', fontsize=20)
        ylim([0, np.max(quantity*1.2)])
    if any([substring in channel for substring in gas_quantities]):
        quantity = data[channel] * scale_factor
        ylabel('Concentration (%)', fontsize=20)
        ylim([0, np.max(quantity*1.2)])

    plot(t, quantity, lw=2, label=channel)
    xlabel('Time', fontsize=20)
    xticks(fontsize=16)
    yticks(fontsize=16)
    legend(loc='lower right')
    grid(True)
    savefig('../Figures/' + test_name + '_' + channel + '.png')
    close('all')
