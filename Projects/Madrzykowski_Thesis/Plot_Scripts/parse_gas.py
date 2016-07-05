from __future__ import division

import os
import numpy as np
import pandas as pd
from pylab import *
import math
import string

from matplotlib import rcParams
rcParams.update({'figure.autolayout': True})

# Location of experimental data files
data_dir = '../Experimental_Data/IWGBGAS/'

# Location of test description file
info_file = '../Experimental_Data/TWGas/Description_of_Gas_Tests.csv'

# List of sensor groups for each plot
sensor_groups = [['TC Surface Center'], ['TC Surface Offset'], ['TC Back Center'], ['TC Plume'], ['HF Center'],
                 ['HF Offset']]

wall_TC_array = [0.2,0.4,0.6,0.8,1.0,1.2,1.4,1.6,1.8,2.0,2.2]
gas_TC_array = [2.4,2.2,2.0,1.8,1.6,1.4,1.2,1.0,0.8,0.6,0.4,0.2]
hf_array = [0.2,0.4,0.6,0.8,1.0,1.2]

# Load exp. timings and description file
info = pd.read_csv(info_file,header=0, index_col=0)
# Skip files
skip_files = ['description_','nctw_','iwgb_']

sample_rate = 4.
sample_length = int(math.ceil(15./sample_rate))


#  =========================
#  = Reading in Data Files =
#  =========================

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
			data_sub_TC=np.zeros(shape=(2*sample_length, int(info['Replicate_Num'][test_name])))
			data_sub_HF=np.zeros(shape=(2*sample_length, int(info['Replicate_Num'][test_name])))

		# Generate subsets for each setup
		for group in sensor_groups:
			# fig=figure()
			if 'HF' in str(group):
				x = hf_array
				ylim([0,75])
				xlim([0,1.5])
			elif 'TC Plume' in group:
				x = gas_TC_array
				ylim([0,800])
				xlim([0,2.5])
			elif group == 'TC Surface Center' or 'TC Surface Offset' or 'TC Back Center':
				x = wall_TC_array
				ylim([0,500])
				xlim([0,2.5])
			data_mean = pd.DataFrame(np.zeros(len(x)))
			k=0

			for channel in data.columns[1:]:
				if any([substring in channel for substring in group]):
					if 'TC ' in channel:
						if info['Replicate_Of'][test_name] == test_name:
							for i in range(0,int(info['Replicate_Num'][test_name])):
								Num = int(test_name[-2:])+i-1
								data2 = pd.read_csv(data_dir + info['Rep_Name'][Num] + '.csv')
								max_id = min(data2[channel].idxmax(), len(data2[channel]) - sample_length)
								data_sub_TC[:,i] = data2[channel][max_id-sample_length:max_id+sample_length:1]
						data_mean[k] = data_sub_TC.mean()
						k=k+1

					if 'HF ' in channel:
						if info['Replicate_Of'][test_name] == test_name:
							for i in range(0,int(info['Replicate_Num'][test_name])):
								Num = int(test_name[-2:])+i-1
								data2 = pd.read_csv(data_dir + info['Rep_Name'][Num] + '.csv')
								max_id = min(data2[channel].idxmax(), len(data2[channel]) - sample_length)
								data_sub_HF[:,i] = data2[channel][max_id-sample_length:max_id+sample_length:1]
						data_mean[k] = data_sub_HF.mean()
						k=k+1

			data_mean.to_csv(data_dir + 'Reduced/' + test_name + '_' + group[0].rstrip('_') + '.csv')
			close('all')
		close('all')
