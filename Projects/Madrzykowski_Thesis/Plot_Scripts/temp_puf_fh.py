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
data_dir = '../Experimental_Data/FHPUF/'
plot_dir = '../Figures/'
info_file = '../Experimental_Data/FHPUF/Description_of_PUF_Tests.csv'

# List of sensor groups for each plot
sensor_groups = [['Center TC']]


# Load exp. timings and description file
info = pd.read_csv(info_file,header=0, index_col=0)
# Skip files
skip_files = ['description_','hf_','ml_']

#  =========================
#  = Reading in Data Files =
#  =========================

#number of TCs in array
num_array = 12

markers = ['s', '*', '^', 'o', '<', '>', '8', 'h','d','x','p','v','H', 'D', '1', '2', '3', '4', '|']
colors = [(31, 119, 180), (174, 199, 232), (255, 127, 14), (255, 187, 120),
             (44, 160, 44), (152, 223, 138), (214, 39, 40), (255, 152, 150),
             (148, 103, 189), (197, 176, 213), (140, 86, 75), (196, 156, 148),
             (227, 119, 194), (247, 182, 210), (127, 127, 127), (199, 199, 199),
             (188, 189, 34), (219, 219, 141), (23, 190, 207), (158, 218, 229)]

# Scale the RGB values to the [0, 1] range, which is the format matplotlib accepts.
for i in range(len(colors)):
    r, g, b = colors[i]
    colors[i] = (r / 255., g / 255., b / 255.)

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

		# Load first replicate of exp. data files
		if info['Replicate_Of'][test_name] == test_name:
			data = pd.read_csv(data_dir + test_name + '.csv')
			data_sub_TC=np.zeros(shape=(int(min(info['End_Time'])), int(info['Replicate_Num'][test_name])))
			data_average = np.zeros(shape=(int(min(info['End_Time'])), num_array))
			time = np.arange(0,int(min(info['End_Time'])),1)
		# Generate subsets for each setup
		for group in sensor_groups:

			for channel in data.columns[1:]:
				if any([substring in channel for substring in group]):
					if 'TC ' in channel:
						if info['Replicate_Of'][test_name] == test_name:
							for i in range(0,int(info['Replicate_Num'][test_name])):
								Num = int(test_name[-2:])+i-1
								data2 = pd.read_csv(data_dir + info['Rep_Name'][Num] + '.csv')
								data_sub_TC[:,i] = data2[channel][:int(min(info['End_Time']))]
						data_average[:,int(channel[10:])-1] = ma.masked_outside(data_sub_TC,0.001,3000).mean(axis=1)
		fig = figure()
		for i in range(data_average.shape[1]):
			y = data_average[:,i]
			plot(time,y,color=colors[i],marker=markers[i],markevery=50,ms=8,label=data.columns[i+1])
		ax1 = gca()
		xlabel('Time (s)', fontsize=20)
		ylabel('Temperature ($^{\circ}$C)', fontsize=20)
		xticks(fontsize=16)
		yticks(fontsize=16)
		legend(numpoints=1,loc=1,ncol=1,fontsize=16)
		legend(bbox_to_anchor=(1.03,1.04))
		axis([0, 300, 0, 1000])
		grid(True)
		savefig(plot_dir + test_name[:-2] + '_TC_Plume_Avg.pdf',format='pdf')
		close()