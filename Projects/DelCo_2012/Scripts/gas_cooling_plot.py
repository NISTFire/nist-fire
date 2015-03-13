#Weinschenk
#3-15

from __future__ import division
import os
import numpy as np
import pandas as pd
from pylab import *
import datetime
from mpl_toolkits.mplot3d import Axes3D
from matplotlib import rcParams
rcParams.update({'figure.autolayout': True})

# Location of experimental data files
data_dir = '../Experimental_Data/'

# Location of test description file
info_file = '../Experimental_Data/Description_of_Gas_Cooling_Tests.csv'

# Duration of pre-test time for bi-directional probes and heat flux gauges (s)
pre_test_time = 60

# List of sensor groups for each plot
sensor_groups = [['GC_1_'], ['GC_2_'], ['GC_3_'], ['GC_4_'], ['GC_5_'],
                 ['BDP5_'], ['HF_', 'RAD_']]

radiometer_cal = 9.542
heatflux_cal = 5.5371

# Load exp. timings and description file
info = pd.read_csv(info_file, index_col=0)

# Skip files
skip_files = ['_reduced', 'description_']

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
		print 'Test ' + test_name
		
		# Load exp. data file
		data = pd.read_csv(data_dir + f,header=0)
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

			# Skip excluded groups listed in test description file
			#if any([substring in group for substring in info['Excluded Groups'][test_name].split('|')]):
			#	continue
			
			fig = figure()

			for channel in data.columns[1:]:

				if any([substring in channel for substring in group]):
					
					if 'GC_' in channel:
						plt.rc('axes', color_cycle=['k', 'r', 'g', 'b', '0.75', 'c', 'm', 'y'])
						quantity = data[channel]
						ylabel('Temperature ($^\circ$C)', fontsize=20)
						line_style = '-'

				# Save converted quantity back to exp. dataframe
				data[channel] = quantity
				plot(t, quantity, lw=1.5, ls=line_style)

			# Set axis options, legend, tickmarks, etc.
			ax1 = gca()
			xlim([0, end_of_test - start_of_test])
			ylim([0, 1000])
			ax1.xaxis.set_major_locator(MaxNLocator(8))
			ax1_xlims = ax1.axis()[0:2]
			grid(True)
			xlabel('Time', fontsize=20)
			xticks(fontsize=16)
			yticks(fontsize=16)
			legend(loc='lower right', fontsize=8)
			
			print 'Plotting', group
			savefig('../Figures/Gas_Cooling/' + test_name + '_' + group[0].rstrip('_') + '.pdf')
			close('all')

		close('all')
		data.to_csv(data_dir + test_name + '_Reduced.csv')     