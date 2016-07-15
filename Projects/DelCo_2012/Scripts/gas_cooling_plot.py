# -*- coding: utf-8 -*-
from __future__ import unicode_literals
#Weinschenk
#3-15

import os
import numpy as np
import pandas as pd
from pylab import *
from itertools import cycle

from matplotlib import rcParams
rcParams.update({'figure.autolayout': True})

# Location of experimental data files
data_dir = '../Experimental_Data/'

# Location of test description file
info_file = '../Experimental_Data/Description_of_Gas_Cooling_Tests.csv'
zero_file = '../Experimental_Data/zero_data.csv'
# Duration of pre-test time for bi-directional probes and heat flux gauges (s)
pre_test_time = 60

# List of sensor groups for each plot
sensor_groups = [['TC_A1_'], ['TC_A2_'], ['TC_A3_'], ['TC_A4_'], ['TC_A5_'],
                 ['BDP_A5'], ['HF_', 'RAD_']]

heat_flux_quantities = ['HF_', 'RAD_']
radiometer_cal = 9.542
heatflux_cal = 5.5371

# Load exp. timings and description file
info = pd.read_csv(info_file, index_col=0)
zero = pd.read_csv(zero_file, header=0,index_col=0)
# Skip files
skip_files = ['_reduced', 'description_','zero','bb','es_','fse','cafs','fsw','_attic','sc','gas_cooling','west_','east_','all_','fire_suppress']

#  ===============================
#  = Loop through all data files =
#  ===============================

for f in os.listdir(data_dir):
	if f.endswith('.csv'):

		# Skip non gas cooling files
		if any([substring in f.lower() for substring in skip_files]):
			continue

		# Strip test name from file name
		test_name = f[:-4]
		print ('Test ' + test_name)

		# Load exp. data file
		data = pd.read_csv(data_dir + f)
		# Read in test times to offset plots
		start_of_test = info['Start_Time'][test_name]
		end_of_test = info['End_Time'][test_name]

		# Offset data time to start of test
		t = data['Time'].values - start_of_test
		data['Time'] = t

		#  ============
		#  = Plotting =
		#  ============

		# Generate a plot for each quantity group
		for group in sensor_groups:

			fig = figure()

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

			for channel in data.columns[1:]:

				if any([substring in channel for substring in group]):

					if 'TC_' in channel:
						quantity = data[channel]
						ylabel('Temperature ($^\circ$C)', fontsize=20)
						line_style = '-'
						ylim([0,600])
						axhline(250,0,len(t),color = '#000000',ls='--',lw=2)

					if 'BDP_' in channel:
						conv_inch_h2o = 0.4
						conv_pascal = 248.8

                        # Convert voltage to pascals
                        # Get zero voltage from pre-test data
						zero_voltage = zero['Calibration'][channel]
						pressure = conv_inch_h2o * conv_pascal * (data[channel] - zero_voltage)
                        # Calculate velocity
						quantity = pd.rolling_mean(0.0698 * np.sqrt(np.abs(pressure) * (data['TC_'+ channel[4:]] + 273.15)) * np.sign(pressure),20,center=True)
						ylabel('Velocity (m/s)', fontsize=20)
						line_style = '-'
						ylim([-10,10])

					if any([substring in channel for substring in heat_flux_quantities]):
						# Get zero voltage from pre-test data
						zero_voltage = zero['Calibration'][channel]
						if 'HF_' in channel:
							calibration_slope = heatflux_cal*1000.
						elif 'RAD_' in channel:
							calibration_slope = radiometer_cal*1000.
						quantity = pd.rolling_mean((data[channel] - zero_voltage) * calibration_slope,10,center=True)
						ylabel('Heat Flux (kW/m$^2$)', fontsize=20)
						if 'HF' in channel:
							line_style = '-'
						elif 'RAD' in channel:
							line_style = '--'
						ylim([-5,20])

					# Save converted quantity back to exp. dataframe
					data[channel] = quantity
					plot(t, quantity,
							 lw=1.5,
							 ls=line_style,
							 marker=next(plot_markers),
							 markevery=int((end_of_test - start_of_test)/20),
							 mew=1.5,
                             mec='none',
                             ms=7,label=zero['Test Specific Name'][channel])

			# Set axis options, legend, tickmarks, etc.
			ax1 = gca()
			xlim([0, end_of_test - start_of_test])
			ax1.xaxis.set_major_locator(MaxNLocator(8))
			ax1_xlims = ax1.axis()[0:2]
			grid(True)
			xlabel('Time (s)', fontsize=20)
			xticks(fontsize=16)
			yticks(fontsize=16)
			legend(loc='upper left', fontsize=8)

			print ('Plotting', group)
			savefig('../Figures/Gas_Cooling/' + test_name + '_' + group[0].rstrip('_') + '.pdf')
			close('all')

		close('all')
		print
		data.to_csv(data_dir + test_name + '_Reduced.csv')