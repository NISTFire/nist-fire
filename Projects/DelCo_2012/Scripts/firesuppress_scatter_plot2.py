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

data_dir = '../Experimental_Data/'
save_dir = '../Figures/Script_Figures/'

# Location of scaling conversion files
scaling_file_west = '../Experimental_Data/West_DelCo_DAQ_Channel_List.csv'
scaling_file_west_2013 = '../Experimental_Data/West_DelCo_DAQ_Channel_List_2013.csv'
scaling_file_east = '../Experimental_Data/East_DelCo_DAQ_Channel_List.csv'
scaling_file_east_2013 = '../Experimental_Data/East_DelCo_DAQ_Channel_List_2013.csv'

# Location of test description file
info_file = '../Experimental_Data/Description_of_Experiments.csv'
info_file2 = '../Experimental_Data/Fire_Suppress_Test_Matrix.csv'

info = pd.read_csv(info_file, index_col=3)
info2 = pd.read_csv(info_file2, index_col=0)

data_time_averaging_window = 1

# Location of figures
plot_dir = '../Figures/Gas_Cooling/'
# List of sensor groups for each plot

# Skip files
skip_files = ['_times','_reduced','description_','zero','bb','es_','cafs','_attic','sc','gas_cooling_','west_','east_','gcs','fire_suppress']

del_TC_2_h2o_hall = np.zeros((8,6))
del_TC_2_cafs_hall = np.zeros((8,6))
del_TC_2_h2o_door= np.zeros((8,6))
del_TC_2_cafs_door = np.zeros((8,6))

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
        if 'FSW' in test_name:
            if '13' in test_name[-2:]:
                channel_list_file = scaling_file_west_2013
            else:
                channel_list_file = scaling_file_west
        elif 'FSE' in test_name:
            if '13' in test_name[-2:]:
                channel_list_file = scaling_file_east_2013
            else:
                channel_list_file = scaling_file_east

        channel_list = pd.read_csv(channel_list_file)
        channel_list = channel_list.set_index('Channel Name')
        channel_groups = [['FSE2_'],['FSW2_']]
        
        # Read in test times to offset plots
        start_of_test = info['Start of Test'][test_name]
        end_of_test = info['End of Test'][test_name]

        # Load exp. data file
        data = pd.read_csv(data_dir + f)
        data = data.set_index('Timestamp (s)')

        # Offset data time to start of test
        data['X_Value'] = data['X_Value'].values - start_of_test
        # Smooth all data channels with specified data_time_averaging_window
        data_copy = data.drop('X_Value', axis=1)
        data_copy = data_copy.rolling(window=data_time_averaging_window, center=True).mean()
        data_copy.insert(0, 'X_Value', data['X_Value'])
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
        				if 'FSE2_' in channel or 'FSW2_' in channel:
        					if 'HF_' in channel:
        						continue
        					if 'RAD_' in channel:
        						continue
	        				water_data_interval = current_channel_data[info2['Hallway_Start_Time_Water'][reps]:info2['Hallway_Stop_Time_Water'][reps]]
        					water_data_interval2 = current_channel_data[info2['Door_Start_Time_Water'][reps]:info2['Door_Stop_Time_Water'][reps]]
        					del_TC_2_h2o_hall[ii,reps-1] =  max(water_data_interval) - max(min(water_data_interval),0)
        					del_TC_2_h2o_door[ii,reps-1] =  max(water_data_interval2) - max(min(water_data_interval2),0)
        					ii=ii+1

        	if test_name in info2['Test_Series_CAFS'][reps]:
	        	for group in channel_groups:
        			ii=0
        			for channel in data.columns[1:]:
        				if any([substring in channel for substring in info['Excluded Channels'][test_name].split('|')]):
        					continue
        				current_channel_data = data[channel]
        				if 'FSE2_' in channel or 'FSW2_' in channel:
        					if 'HF_' in channel:
        						continue
        					if 'RAD_' in channel:
        						continue
	        				cafs_data_interval = current_channel_data[info2['Hallway_Start_Time_CAFS'][reps]:info2['Hallway_Stop_Time_CAFS'][reps]]
	        				cafs_data_interval2 = current_channel_data[info2['Door_Start_Time_CAFS'][reps]:info2['Door_Stop_Time_CAFS'][reps]]
        					del_TC_2_cafs_hall[ii,reps-1] =  max(max(cafs_data_interval),0) - max(min(cafs_data_interval),0.)
        					del_TC_2_cafs_door[ii,reps-1] =  max(max(cafs_data_interval2),0) - max(min(cafs_data_interval2),0.)
        					# print(max(cafs_data_interval2))
        					ii=ii+1

del_water = del_TC_2_h2o_hall
del_cafs = del_TC_2_cafs_hall
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
savefig(save_dir + 'TCA2_hallnozzle_scatter.pdf',format='pdf')

# print(del_TC_1_h2o_door)
# print(del_TC_1_cafs_door[:,4])

del_water = del_TC_2_h2o_door
del_cafs = del_TC_2_cafs_door
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
savefig(save_dir + 'TCA2_doornozzle_scatter.pdf',format='pdf')