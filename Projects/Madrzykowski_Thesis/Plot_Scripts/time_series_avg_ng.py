from __future__ import division

import os
import numpy as np
import numpy.ma as ma
import pandas as pd
from pylab import *
import math
import string

from matplotlib import rcParams
rcParams.update({'figure.autolayout': True})

# Location of files
data_dir = '../Experimental_Data/TWNG/'
plot_dir = '../Figures/'
info_file = '../Experimental_Data/TWNG/Description_of_NG_Tests.csv'

# List of sensor groups for each plot
sensor_groups = [['TC Plume'],['TC Surface Center'],['TC Surface Offset'],['TC Back Center'],['HF Center'],['HF Offset']]


# Load exp. timings and description file
info = pd.read_csv(info_file,header=0, index_col=0)
# Skip files
skip_files = ['description_','nctw_']

#  =========================
#  = Reading in Data Files =
#  =========================

markers = ['s', '*', '^', 'o', '<', '>', '8', 'h','d','x','p','v','H', 'D', '1', '2', '3', '4', '|']
colors=['r', 'b', 'g', 'c', 'm', 'grey', 'y','#cc5500', '#228b22','#f4a460','#4c177d','firebrick', 'mediumblue', 'darkgreen', 'cadetblue', 'indigo', 'crimson', 'gold']
label_plume = ['TC Plume 0.4m','TC Plume 0.6m','TC Plume 0.8m','TC Plume 1.0m','TC Plume 1.2m','TC Plume 1.4m',
			'TC Plume 1.6m','TC Plume 1.8m','TC Plume 2.0m','TC Plume 2.2m','TC Plume 2.4m']
label_surf_cen = ['TC Front Center 0.2m','TC Front Center 0.4m','TC Front Center 0.6m','TC Front Center 0.8m','TC Front Center 1.0m',
					'TC Front Center 1.2m','TC Front Center 1.4m','TC Front Center 1.6m','TC Front Center 1.8m','TC Front Center 2.0m','TC Front Center 2.2m']
label_surf_off = ['TC Front Edge 0.2m','TC Front Edge 0.4m','TC Front Edge 0.6m','TC Front Edge 0.8m','TC Front Edge 1.0m',
					'TC Front Edge 1.2m','TC Front Edge 1.4m','TC Front Edge 1.6m','TC Front Edge 1.8m','TC Front Edge 2.0m','TC Front Edge 2.2m']
label_back_cen = ['TC Back Center 0.2m','TC Back Center 0.4m','TC Back Center 0.6m','TC Back Center 0.8m','TC Back Center 1.0m',
					'TC Back Center 1.2m','TC Back Center 1.4m','TC Back Center 1.6m','TC Back Center 1.8m','TC Back Center 2.0m','TC Back Center 2.2m']
label_hf_cen = ['HF Center 0.2m','HF Center 0.4m','HF Center 0.6m','HF Center 0.8m','HF Center 1.0m','HF Center 1.2m']
label_hf_off = ['HF Edge 0.2m','HF Edge 0.4m','HF Edge 0.6m','HF Edge 0.8m','HF Edge 1.0m','HF Edge 1.2m']

for f in os.listdir(data_dir):
	if f.endswith('.csv'):
		print
		# Skip files with time information or reduced data files
		if any([substring in f.lower() for substring in skip_files]):
			continue

		# Strip test name from file name
		test_name = f[:-4]
		print 'Test ' + test_name

		# Skip replicate files
		if info['Skip'][test_name] == 'Yes':
			print 'Replicate test skipped'
			continue
		# Time sample rate
		time_sample = 1

		# Load first replicate of exp. data files
		if info['Replicate_Of'][test_name] == test_name:
			data = pd.read_csv(data_dir + test_name + '.csv')
			data_len = int(int(min(info['End_Time']))/time_sample)
			data_sub=np.zeros(shape=(data_len, int(info['Replicate_Num'][test_name])))
			time = np.arange(0,int(min(info['End_Time'])),time_sample)


		# Generate subsets for each setup
		for group in sensor_groups:
			k=0
			if 'TC Plume' in group:
				labels = label_plume
				array = '_TC_Plume_Avg'
				num_array = 12
				shape_offset = 1
				ymax,xmax = 1000,500
				ylabel('Temperature ($^{\circ}$C)', fontsize=20)
			elif 'TC Surface Center' in group:
				labels = label_surf_cen
				array = '_TC_Surface_Center_Avg'
				num_array = 11
				shape_offset = 0
				ymax,xmax = 500,600
				ylabel('Temperature ($^{\circ}$C)', fontsize=20)
			elif 'TC Surface Offset' in group:
				labels = label_surf_off
				array = '_TC_Surface_Offset_Avg'
				num_array = 10
				shape_offset = 0
				ymax,xmax = 300,600
				ylabel('Temperature ($^{\circ}$C)', fontsize=20)
			elif 'TC Back Center' in group:
				labels = label_back_cen
				array = '_TC_Back_Center_Avg'
				num_array = 11
				shape_offset = 0
				ymax,xmax = 120,600
				ylabel('Temperature ($^{\circ}$C)', fontsize=20)
			elif 'HF Center' in group:
				labels = label_hf_cen
				array = '_HF_Center_Avg'
				num_array = 6
				shape_offset = 0
				ymax,xmax = 60,300
				ylabel('Heat Flux (kW/m$^2$)', fontsize=20)
			elif 'HF Offset' in group:
				labels = label_hf_off
				array = '_HF_Offset_Avg'
				num_array = 6
				shape_offset = 0
				ymax,xmax = 50,300
				ylabel('Heat Flux (kW/m$^2$)', fontsize=20)
			data_average = np.zeros(shape=(data_len, num_array))
			for channel in data.columns[1:]:
				if any([substring in channel for substring in group]):
					if 'TC ' or 'HF ' in channel:
						if info['Replicate_Of'][test_name] == test_name:
							for i in range(0,int(info['Replicate_Num'][test_name])):
								Num = int(test_name[-2:])+i-1
								data2 = pd.read_csv(data_dir + info['Rep_Name'][Num] + '.csv')
								data_sub[:,i] = data2[channel][:int(min(info['End_Time']))]
						data_average[:,k] = ma.masked_outside(data_sub,-3000,3000).mean(axis=1)
						k=k+1

			fig = figure()
			for i in range(data_average.shape[1]-shape_offset):
				y = data_average[:,i+shape_offset]
				plot(time,y,color=colors[i],marker=markers[i],markevery=50,ms=8,label=labels[i])
			ax1 = gca()
			xlabel('Time (s)', fontsize=20)
			xticks(fontsize=16)
			yticks(fontsize=16)
			legend(numpoints=1,loc=1,ncol=1,fontsize=16)
			axis([0, xmax, 0, ymax])
			grid(True)
			savefig(plot_dir + test_name[9:] + array + '.pdf',format='pdf')
			close()

