#Weinschenk
#3-15

import os
import numpy as np
import pandas as pd
from pylab import *
import statsmodels.api as sm
from matplotlib import rcParams
rcParams.update({'figure.autolayout': True})

# Location of experimental data files
data_dir = '../Experimental_Data/'

# Location of test description file
info_file = '../Experimental_Data/Gas_Cooling_Test_Matrix.csv'

# Location of figures
plot_dir = '../Figures/Gas_Cooling/'
# List of sensor groups for each plot
sensor_groups = [['TC_A1_'],['TC_A3_']]

# Load exp. timings and description file
info = pd.read_csv(info_file, index_col=0)

# Skip files
skip_files = ['_reduced', 'description_','zero','bb','es_','fse','cafs','fsw','_attic','sc','gas_cooling','west_','east_','all_']

#  ===============================
#  = Loop through all data files =
#  ===============================

# Load exp. data file
data1 = pd.read_csv(data_dir + 'GCSeries1.csv')
data2 = pd.read_csv(data_dir + 'GCSeries2.csv')
data3 = pd.read_csv(data_dir + 'GCSeries3.csv')
data4 = pd.read_csv(data_dir + 'GCSeries4.csv')
data5 = pd.read_csv(data_dir + 'GCSeries5.csv')

for entry in range(0,len(info)):
	print entry
	if info['Replicates'][entry] == 0:
		continue
	else:
		num_rep = info['Replicates'][entry]
		del_TC_1_h2o = np.zeros((11,num_rep))
		del_TC_3_h2o = np.zeros((11,num_rep))
		del_TC_1_cafs = np.zeros((11,num_rep))
		del_TC_3_cafs = np.zeros((11,num_rep))

		for group in sensor_groups:
			for channel in data1.columns[1:]:
				for reps in range(0,num_rep):
					if 'TC_A1_' in channel:
						water_test = 'data'+str(info['Test_Series_Water'][entry])
						water_test = locals().get(water_test)
						water_data_interval = water_test[channel][info['Start_Time_Water'][entry]:info['Stop_Time_Water'][entry]]
						del_TC_1_h2o[int(channel[6:])-1,reps] = max(water_data_interval) - min(water_data_interval)
						
						cafs_test = 'data'+str(info['Test_Series_CAFS'][entry])
						cafs_test = locals().get(cafs_test)
						cafs_data_interval = cafs_test[channel][info['Start_Time_CAFS'][entry]:info['Stop_Time_CAFS'][entry]]
						del_TC_1_cafs[int(channel[6:])-1,reps] = max(cafs_data_interval) - min(cafs_data_interval)
					if 'TC_A3_' in channel:
						water_test = 'data'+str(info['Test_Series_Water'][entry])
						water_test = locals().get(water_test)
						water_data_interval = water_test[channel][info['Start_Time_Water'][entry]:info['Stop_Time_Water'][entry]]
						del_TC_3_h2o[int(channel[6:])-1,reps] = max(water_data_interval) - min(water_data_interval)
						
						cafs_test = 'data'+str(info['Test_Series_CAFS'][entry])
						cafs_test = locals().get(cafs_test)
						cafs_data_interval = cafs_test[channel][info['Start_Time_CAFS'][entry]:info['Stop_Time_CAFS'][entry]]
						del_TC_3_cafs[int(channel[6:])-1,reps] = max(cafs_data_interval) - min(cafs_data_interval)
		del_water = concatenate([del_TC_1_h2o, del_TC_3_h2o], axis=1)
		print del_water
		del_cafs  = concatenate([del_TC_1_cafs, del_TC_3_cafs], axis=1)




		#-----------------------
		# Stats Analysis OLS
		#-----------------------

		y = del_water.ravel()
		X = del_cafs.ravel()
		est = sm.OLS(y, X)
		est = est.fit()
		max_axis = max(X.max(),y.max())
		X_prime = np.linspace(X.min(), X.max(), 100)[:, np.newaxis]
		y_hat = est.predict(X_prime)
		avg_rel_diff = sum((y-X)/((y+X)/2.))/len(X)

		fig = figure()
		plt.scatter(X,y,alpha=0.5)
		plt.plot(X_prime, y_hat, 'r', alpha=0.9)  # Add the regression line, colored in red
		axis([0, max_axis, 0, max_axis])
		plt.text(8, max_axis-5, 'R$^2$ = ' + str(around(est.rsquared,decimals=3)),
			 horizontalalignment='center',
		     verticalalignment='center', bbox=dict(facecolor='none', edgecolor='black'))
		xlabel('$\Delta$T ($^{\circ}$C) CAFS')
		ylabel('$\Delta$T ($^{\circ}$C) H$_2$O')
		savefig(plot_dir + info['Nozzle'][entry] + '_' + info['Position'][entry] + '_scatter.pdf',format='pdf')

