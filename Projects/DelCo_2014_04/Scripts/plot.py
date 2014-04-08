#!/usr/bin/env python

import numpy as np
from pylab import *

from matplotlib import rcParams
rcParams.update({'figure.autolayout': True})

#  =================
#  = User Settings =
#  =================

# Name of the test
test_name = 'Test_1'

data_file = '../Experimental_Data/test_data.csv'

# Common quantities for y-axis labelling
heat_flux_quantities = ['HF_', 'RAD_']
gas_quantities = ['CO_', 'CO2_', 'O2_']

#  ============
#  = Plotting =
#  ============

data = np.genfromtxt(data_file, delimiter=',', names=True)

# Generate a plot for each quantity
for channel in data.dtype.names[2:]:
    figure()
    plot(data['Time'], data[channel], lw=2, label=channel)
    xlabel('Time', fontsize=20)
    
    # Set y-axis label depending on quantity
    if 'TC_' in channel:
        ylabel('Temperature ($^\circ$C)', fontsize=20)
    if 'BDP_' in channel:
        ylabel('Velocity (m/s)', fontsize=20)
    if any([substring in channel for substring in heat_flux_quantities]):
        ylabel('Heat Flux (kW/m$^2$)', fontsize=20)
    if any([substring in channel for substring in gas_quantities]):
        ylabel('Concentration (%)', fontsize=20)
    
    xticks(fontsize=16)
    yticks(fontsize=16)
    ylim(ymin=0)
    legend(loc='lower right')
    grid(True)
    savefig('../Figures/' + test_name + '_' + channel + '.png')
    close('all')
