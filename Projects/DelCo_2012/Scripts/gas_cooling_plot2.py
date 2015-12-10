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

#from ggplot import *
#from patsy import ModelDesc

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
skip_channels = ['_9','_10','_11']

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
	if info['Replicates'][entry] == 0:
		continue
	else:
		print (info['Nozzle'][entry]+ ' ' + info['Position'][entry])
		num_rep = info['Replicates'][entry]
		del_TC_1_h2o = np.zeros((8,num_rep))
		del_TC_2_h2o = np.zeros((8,num_rep))
		del_TC_3_h2o = np.zeros((8,num_rep))
		del_TC_1_cafs = np.zeros((8,num_rep))
		del_TC_2_cafs = np.zeros((8,num_rep))
		del_TC_3_cafs = np.zeros((8,num_rep))


		for reps in range(0,num_rep):
			for channel in data1.columns[1:]:
                # Skip excluded channels
				if any([substring in channel for substring in skip_channels]):
					continue
				elif 'TC_A1_' in channel:
					water_test = 'data'+str(info['Test_Series_Water'][entry+reps])
					water_test = locals().get(water_test)
					water_data_interval = water_test[channel][info['Start_Time_Water'][entry+reps]:info['Stop_Time_Water'][entry+reps]]
					del_TC_1_h2o[int(channel[6:])-1,reps] = max(water_data_interval) - min(water_data_interval)
					#del_TC_1_h2o[int(channel[6:])-1,reps] = (max(water_data_interval) - min(water_data_interval))/max(water_data_interval)

					cafs_test = 'data'+str(info['Test_Series_CAFS'][entry+reps])
					cafs_test = locals().get(cafs_test)
					cafs_data_interval = cafs_test[channel][info['Start_Time_CAFS'][entry+reps]:info['Stop_Time_CAFS'][entry+reps]]
					del_TC_1_cafs[int(channel[6:])-1,reps] = max(cafs_data_interval) - min(cafs_data_interval)
					#del_TC_1_cafs[int(channel[6:])-1,reps] = (max(cafs_data_interval) - min(cafs_data_interval))/max(cafs_data_interval)
				elif 'TC_A3_' in channel:
					water_test = 'data'+str(info['Test_Series_Water'][entry+reps])
					water_test = locals().get(water_test)
					water_data_interval = water_test[channel][info['Start_Time_Water'][entry+reps]:info['Stop_Time_Water'][entry+reps]]
					#del_TC_3_h2o[int(channel[6:])-1,reps] = max(water_data_interval) - min(water_data_interval)
					del_TC_3_h2o[int(channel[6:])-1,reps] = (max(water_data_interval) - min(water_data_interval))/max(water_data_interval)
					# print (max(water_data_interval) , min(water_data_interval), max(water_data_interval) - min(water_data_interval), channel,reps,'water')
					cafs_test = 'data'+str(info['Test_Series_CAFS'][entry+reps])
					cafs_test = locals().get(cafs_test)
					cafs_data_interval = cafs_test[channel][info['Start_Time_CAFS'][entry+reps]:info['Stop_Time_CAFS'][entry+reps]]
					#del_TC_3_cafs[int(channel[6:])-1,reps] = max(cafs_data_interval) - min(cafs_data_interval)
					del_TC_3_cafs[int(channel[6:])-1,reps] = (max(cafs_data_interval) - min(cafs_data_interval))/max(cafs_data_interval)
					# print (max(cafs_data_interval) , min(cafs_data_interval),max(cafs_data_interval) - min(cafs_data_interval),channel,reps,'cafs')
					# print()
				if 'TC_A2_' in channel:
					water_test = 'data'+str(info['Test_Series_Water'][entry+reps])
					water_test = locals().get(water_test)
					water_data_interval = water_test[channel][info['Start_Time_Water'][entry+reps]:info['Stop_Time_Water'][entry+reps]]
					del_TC_2_h2o[int(channel[6:])-1,reps] = (max(water_data_interval) - min(water_data_interval))/max(water_data_interval)

					cafs_test = 'data'+str(info['Test_Series_CAFS'][entry+reps])
					cafs_test = locals().get(cafs_test)
					cafs_data_interval = cafs_test[channel][info['Start_Time_CAFS'][entry+reps]:info['Stop_Time_CAFS'][entry+reps]]
					del_TC_2_cafs[int(channel[6:])-1,reps] = (max(cafs_data_interval) - min(cafs_data_interval))/max(cafs_data_interval)
		#del_water = concatenate([del_TC_1_h2o, del_TC_3_h2o], axis=1)
		del_water = del_TC_3_h2o
		del_water = del_water.reshape(-1)
		# del_cafs  = concatenate([del_TC_1_cafs, del_TC_3_cafs], axis=1)
		del_cafs = del_TC_3_cafs
		del_cafs  = del_cafs.reshape(-1)
		dif_data  = []
		for i in range (0,len(del_water)):
			dif_data.append({'del_water' : del_water[i], 'del_cafs' : del_cafs[i]})
		del_temp = pd.DataFrame(dif_data,columns=['del_water','del_cafs'])

		#-----------------------
		# Stats Analysis OLS
		#-----------------------

		y = del_water.ravel()
		X = del_cafs.ravel()
		est = sm.OLS(y, X)
		est = est.fit()
		max_axis = max(X.max(),y.max())
		X_prime = np.linspace(0,X.max())
		y_hat = est.predict(X_prime)
		avg_rel_diff = sum((y-X)/((y+X)/2.))/len(X)

		# p = ggplot(aes('del_cafs', 'del_water'),data = del_temp) + geom_point() + stat_smooth(method='lm', color='blue',se=True) + \
		# geom_abline(intercept=0,slope=1,colour="black") + scale_x_continuous("$\Delta$T (deg C) CAFS", limits=(0,max_axis)) + \
		# scale_y_continuous("$\Delta$T (deg C) H$_2$O",limits=(0,max_axis))
		# ggsave(p,plot_dir + info['Nozzle'][entry] + '_' + info['Position'][entry] + '_scatter_ggplot.pdf',format='pdf' )

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
		savefig(plot_dir + info['Nozzle'][entry] + '_' + info['Position'][entry] + '_A3_scatter.pdf',format='pdf')

		# fig = figure()
		# plt.scatter(del_TC_2_h2o,del_TC_2_cafs,alpha=0.5)
		# plt.plot(X_prime,X_prime,'k')
		# axis([0, max_axis, 0, max_axis])
		# xlabel('$\Delta$T ($^{\circ}$C) CAFS')
		# ylabel('$\Delta$T ($^{\circ}$C) H$_2$O')
		# savefig(plot_dir + info['Nozzle'][entry] + '_' + info['Position'][entry] + '_A2_scatter.pdf',format='pdf')

		# fig=figure()
		# plt.hist(est.norm_resid())
		# plt.ylabel('Count')
		# plt.xlabel('Normalized residuals')
		# savefig(plot_dir + info['Nozzle'][entry] + '_' + info['Position'][entry] + '_residuals.pdf',format='pdf')
