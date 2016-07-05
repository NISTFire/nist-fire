from __future__ import division

import os
import numpy as np
import numpy.ma as ma
import pandas as pd
from pylab import *
import math
import string

from matplotlib import rcParams
# rcParams.update({'figure.autolayout': True})

# Location of files
data_dir = '../Experimental_Data/IWGBNG/'
plot_dir = '../Figures/'
info_file = '../Experimental_Data/IWGBNG/Description_of_NG_Tests.csv'

# List of sensor groups for each plot
sensor_groups = [['TC Plume'],['TC Surface Center'],['TC Surface Offset'],['TC Back Center'],['HF Center'],['HF Offset']]


# Load exp. timings and description file
info = pd.read_csv(info_file,header=0, index_col=0)
# Skip files
skip_files = ['description_','nctw_','iwgb_']

#  =========================
#  = Reading in Data Files =
#  =========================
colors = [(31, 119, 180), (174, 199, 232), (255, 127, 14), (255, 187, 120),
             (44, 160, 44), (152, 223, 138), (214, 39, 40), (255, 152, 150),
             (148, 103, 189), (197, 176, 213), (140, 86, 75), (196, 156, 148),
             (227, 119, 194), (247, 182, 210), (127, 127, 127), (199, 199, 199),
             (188, 189, 34), (219, 219, 141), (23, 190, 207), (158, 218, 229)]

# Scale the RGB values to the [0, 1] range, which is the format matplotlib accepts.
for i in range(len(colors)):
    r, g, b = colors[i]
    colors[i] = (r / 255., g / 255., b / 255.)

markers = ['s', '*', '^', 'o', '<', '>', '8', 'h','d','x','p','v','H', 'D', '1', '2', '3', '4', '|']
# colors=['r', 'b', 'g', 'c', 'm', 'grey', 'y','#cc5500', '#228b22','#f4a460','#4c177d','firebrick', 'mediumblue', 'darkgreen', 'cadetblue', 'indigo', 'crimson', 'gold']
label_plume = ['Plume 0.4m','Plume 0.6m','Plume 0.8m','Plume 1.0m','Plume 1.2m','Plume 1.4m',
			'Plume 1.6m','Plume 1.8m','Plume 2.0m','Plume 2.2m','Plume 2.4m']
label_surf_cen = ['Front Center 0.2m','Front Center 0.4m','Front Center 0.6m','Front Center 0.8m','Front Center 1.0m',
					'Front Center 1.2m','Front Center 1.4m','Front Center 1.6m','Front Center 1.8m','Front Center 2.0m','Front Center 2.2m']
label_surf_off = ['Front Edge 0.2m','Front Edge 0.4m','Front Edge 0.6m','Front Edge 0.8m','Front Edge 1.0m',
					'Front Edge 1.2m','Front Edge 1.4m','Front Edge 1.6m','Front Edge 1.8m','Front Edge 2.0m','Front Edge 2.2m']
label_back_cen = ['Back Center 0.2m','Back Center 0.4m','Back Center 0.6m','Back Center 0.8m','Back Center 1.0m',
					'Back Center 1.2m','Back Center 1.4m','Back Center 1.6m','Back Center 1.8m','Back Center 2.0m','Back Center 2.2m']
label_hf_cen = ['Center 0.2m','Center 0.4m','Center 0.6m','Center 0.8m','Center 1.0m','Center 1.2m']
label_hf_off = ['Edge 0.2m','Edge 0.4m','Edge 0.6m','Edge 0.8m','Edge 1.0m','Edge 1.2m']

for f in os.listdir(data_dir):
	if f.endswith('.csv'):
		print
		# Skip files with time information or reduced data files
		if any([substring in f.lower() for substring in skip_files]):
			continue

		# Strip test name from file name
		test_name = f[:-4]
		print ('Test ' + test_name)

		# Skip replicate files
		if info['Skip'][test_name] == 'Yes':
			print ('Replicate test skipped')
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
		fig = figure()
		for group in sensor_groups:
			k=0
			if 'TC Plume' in group:
				labels = label_plume
				array = '_TC_Plume_Avg'
				num_array = 12
				shape_offset = 1
				ymax,xmax = 1000,600
				mean_length=1
				ylabel('Temperature ($^{\circ}$C)', fontsize=20)
			elif 'TC Surface Center' in group:
				labels = label_surf_cen
				array = '_TC_Surface_Center_Avg'
				num_array = 11
				shape_offset = 0
				ymax,xmax = 600,600
				mean_length=1
				ylabel('Temperature ($^{\circ}$C)', fontsize=20)
			elif 'TC Surface Offset' in group:
				labels = label_surf_off
				array = '_TC_Surface_Offset_Avg'
				num_array = 10
				shape_offset = 0
				ymax,xmax = 500,600
				mean_length=1
				ylabel('Temperature ($^{\circ}$C)', fontsize=20)
			elif 'TC Back Center' in group:
				labels = label_back_cen
				array = '_TC_Back_Center_Avg'
				num_array = 11
				shape_offset = 0
				ymax,xmax = 120,600
				mean_length=1
				ylabel('Temperature ($^{\circ}$C)', fontsize=20)
			elif 'HF Center' in group:
				labels = label_hf_cen
				array = '_HF_Center_Avg'
				num_array = 6
				shape_offset = 0
				ymax,xmax = 60,600
				mean_length=10
				ylabel('Heat Flux (kW/m$^2$)', fontsize=20)
			elif 'HF Offset' in group:
				labels = label_hf_off
				array = '_HF_Offset_Avg'
				num_array = 6
				shape_offset = 0
				ymax,xmax = 70,600
				mean_length=10
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

			for i in range(data_average.shape[1]-shape_offset):
				y = pd.rolling_mean(data_average[:,i+shape_offset],mean_length,center=True)
				plot(time,y,color=colors[i],marker=markers[i],markevery=50,ms=8,label=labels[i])
			ax1 = gca()
			xlabel('Time (s)', fontsize=20)
			xticks(fontsize=16)
			yticks(fontsize=16)
			axis([0, xmax, 0, ymax])
			box = ax1.get_position()
			ax1.set_position([box.x0, box.y0, box.width * 0.7, box.height])
			ax1.legend(loc='center left', bbox_to_anchor=(1, 0.5))
			# legend(numpoints=1,loc=1,ncol=1,fontsize=16)
			grid(True)
			savefig(plot_dir + test_name[9:] + array + '.pdf',format='pdf')
			close()

