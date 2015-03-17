#Weinschenk
#2-15

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

# Skip files
skip_files = ['_reduced', 'description_','zero','gcs','fse','cafs','fsw','_attic','sc']

for f in os.listdir(data_dir):
	if f.endswith('.csv'):

		# Skip files with time information or reduced data files
		if any([substring in f.lower() for substring in skip_files]):
			continue

		# Strip test name from file name
		test_name = f[:-4]
		print 'Test ' + test_name

		# Load exp. data file
		data = pd.read_csv(data_dir + f, header=0, index_col=0)

		if test_name[:2] == 'BB':
			row_num = 7
			col_num = 10
			dx = 0.5
			dy = 0.5
			zlim,zspace = 15,1
			xlabel,ylabel = 'Depth (m)','Width (m)'
			ticksx,ticksy = np.arange(0, col_num, 1),np.arange(0, row_num, 1)
			column_names = ['5.5','5.0','4.4','3.9','3.3','2.8','2.2','1.7','1.1','0.6']
			row_names = ['0.6','1.1','1.7','2.2','2.8','3.3','3.9']
			water_mass = np.reshape(data['Mass of Water Collected (kg)'],(col_num,-1))
			water_mass = fliplr(water_mass).T
			for i in enumerate(range(col_num)):
				for j in enumerate(range(row_num)):
					water_mass[j,i] +=  abs(np.random.normal(scale=1e-6))
		else:
			row_num = 11
			col_num = 8
			dx = 0.5
			dy = 0.5
			zlim,zspace = 40,2
			xlabel,ylabel = 'Width (m)','Depth (m)'
			ticksx,ticksy = np.arange(0, row_num, 1),np.arange(0, col_num, 1)
			column_names = ['6.1','5.5','5.0','4.4','3.9','3.3','2.8','2.2','1.7','1.1','0.6']
			row_names = ['0.6','1.1','1.7','2.2','2.8','3.3','3.9','4.4']
			water_mass = np.reshape(data['Mass of Water Collected (kg)'],(col_num,-1))[::-1]
			for i in enumerate(range(col_num)):
				for j in enumerate(range(row_num)):
					water_mass[i,j] +=  abs(np.random.normal(scale=1e-6))

		fig = plt.figure()
		ax = fig.add_subplot(111, projection='3d')
		plt.xticks(ticksx, column_names)
		ax.set_xlabel(xlabel)
		plt.yticks(ticksy, row_names)
		ax.set_ylabel(ylabel)
		ax.set_zlabel('Mass of Water Collected (kg)')
		ticksz = np.arange(0, zlim, zspace)
		ax.set_zticks(ticksz)
		ax.set_zlim(0,zlim)
		x_data, y_data = np.meshgrid(np.arange(water_mass.shape[1]),np.arange(water_mass.shape[0]))
		x_data = x_data.flatten()
		y_data = y_data.flatten()
		z_data = np.nan_to_num(water_mass.flatten())
		ax.bar3d(x_data, y_data, np.zeros(len(z_data)), dx, dy, z_data,zsort='max')
		savefig('../Figures/Bars/' + test_name + '.pdf')
		close('all')