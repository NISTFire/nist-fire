# -*- coding: utf-8 -*-
from __future__ import unicode_literals
#Weinschenk
#3-15
from __future__ import division
import os
import numpy as np
import pandas as pd
import itertools
from pylab import *
import statsmodels.api as sm

from matplotlib import rcParams
rcParams.update({'figure.autolayout': True})

# Location of file with timing information
all_times_file = '../Experimental_Data/All_Times.csv'

data_dir = '../../DelCo_2014_2015/Experimental_Data/'
save_dir = '../Figures/Script_Figures/'

# Location of scaling conversion files
scaling_file = '../../DelCo_2014_2015/DAQ_Files/DAQ_Files_2015/West_DelCo_DAQ_Channel_List.csv'

# Location of test description file
info_file = '../../DelCo_2014_2015/Experimental_Data/Description_of_Experiments.csv'
info_file2 = '../Experimental_Data/Fire_Suppress_Test_Matrix_2.csv'

info = pd.read_csv(info_file, index_col=3)
info2 = pd.read_csv(info_file2, index_col=0)

data_time_averaging_window = 1

# Location of figures
plot_dir = '../Figures/Script_Figures/'
# List of sensor groups for each plot

# Skip files
skip_files = ['_times', '_reduced', 'description_','zero_','_rh','burn','helmet','ppv_','fire','hose']

del_TC_h2o = np.zeros((8,2))
del_TC_caf = np.zeros((8,2))


#  ===============================
#  = Loop through all data files =
#  ===============================
for f in os.listdir(data_dir):
	if f.endswith('.csv'):

		# Skip files with time information or reduced data files
		if any([substring in f.lower() for substring in skip_files]):
			continue

		# Strip test name from file name
		test_name = f[:-4]
		print ('Test ' + test_name)

		# Load exp. scaling file
		channel_list_file = scaling_file

		channel_list = pd.read_csv(channel_list_file)
		channel_list = channel_list.set_index('Channel Name')
		channel_groups = [['TC_A9']]
		
		# Read in test times to offset plots
		start_of_test = info['Start of Test'][test_name]
		end_of_test = info['End of Test'][test_name]

		# Load exp. data file
		data = pd.read_csv(data_dir + f)
		data = data.set_index('TimeStamp(s)')

		data['Time'] = data['Time'].values - start_of_test

		data_copy = data.drop('Time', axis=1)
		data_copy = pd.rolling_mean(data_copy, data_time_averaging_window, center=True)
		data_copy.insert(0, 'Time', data['Time'])
		data_copy = data_copy.dropna()
		data = data_copy

		for reps in range(1,len(info2)+1):
			if test_name in info2['Test_Series_Water'][reps]:
				for group in channel_groups:
					ii=0
					for channel in data.columns[1:]:
						if any([substring in channel for substring in info['Excluded Channels'][test_name].split('|')]):
							continue
						current_channel_data = data[channel]
						if 'TC_A10' in channel:
							water_data_interval = current_channel_data[info2['Water_On'][reps]:info2['Water_Off'][reps]]
							del_TC_h2o[ii,reps-1] =  max(water_data_interval) - max(min(water_data_interval),0)
							ii=ii+1

			if test_name in info2['Test_Series_CAFS'][reps]:
				for group in channel_groups:
					ii=0
					for channel in data.columns[1:]:
						if any([substring in channel for substring in info['Excluded Channels'][test_name].split('|')]):
							continue
						current_channel_data = data[channel]
						if 'TC_A10' in channel:
							cafs_data_interval = current_channel_data[info2['CAF_On'][reps]:info2['CAF_Off'][reps]]
							del_TC_caf[ii,reps-1] =  max(max(cafs_data_interval),0) - max(min(cafs_data_interval),0.)
							ii=ii+1

print (del_TC_h2o)
print (del_TC_caf)

del_water = del_TC_h2o
del_cafs = del_TC_caf
del_water = del_water.reshape(-1)
del_cafs  = del_cafs.reshape(-1)
dif_data  = []
for i in range (0,len(del_water)):
	dif_data.append({'del_water' : del_water[i], 'del_cafs' : del_cafs[i]})
del_temp = pd.DataFrame(dif_data,columns=['del_water','del_cafs'])
y = del_water.ravel()
X = del_cafs.ravel()
est = sm.OLS(y, X)
est = est.fit()
max_axis = max(X.max(),y.max())
X_prime = np.linspace(0,X.max())
y_hat = est.predict(X_prime)
avg_rel_diff = sum((y-X)/((y+X)/2.))/len(X)

fig = figure()
plt.scatter(X,y,alpha=0.5)
plt.plot(X_prime, y_hat, 'r--', alpha=0.9,linewidth=3)  # Add the regression line, colored in red
plt.plot(X_prime,X_prime,'k')
plt.fill_between(X_prime,0.85*X_prime,1.15*X_prime, facecolor='gray',alpha=0.5, interpolate=True,linewidth=3)
axis([0, max_axis, 0, max_axis])
plt.text(0.1*max_axis , 0.95*max_axis, 'R$^2$ = ' + str(around(est.rsquared,decimals=3)),
	horizontalalignment='center',
	verticalalignment='center', bbox=dict(facecolor='none', edgecolor='black'))
xlabel('$\Delta$T ($^{\circ}$C) CAFS')
ylabel('$\Delta$T ($^{\circ}$C) WATER')
savefig(save_dir + 'TC_A10_scatter.pdf',format='pdf')
