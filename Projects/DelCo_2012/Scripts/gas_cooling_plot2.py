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
data = pd.read_csv(data_dir + 'GCSeries1.csv')
test_name = 'GCSeries1'

y = [1,2,3,4,5,6,7,8,9,10,11]

del_TC_1_h2o = np.zeros((11,3))
del_TC_3_h2o = np.zeros((11,3))
del_TC_1_cafs = np.zeros((11,3))
del_TC_3_cafs = np.zeros((11,3))


for group in sensor_groups:
	for channel in data.columns[1:]:
		if 'TC_A1_' in channel:
			del_TC_1_h2o[int(channel[6:])-1,0] = max(data[channel][1290:1350]) - min(data[channel][1290:1350])
			del_TC_1_h2o[int(channel[6:])-1,1] = max(data[channel][1600:1700]) - min(data[channel][1600:1700])
			del_TC_1_h2o[int(channel[6:])-1,2] = max(data[channel][2170:2250]) - min(data[channel][2170:2250])
			del_TC_1_cafs[int(channel[6:])-1,0] = max(data[channel][2450:2550]) - min(data[channel][2450:2550])
			del_TC_1_cafs[int(channel[6:])-1,1] = max(data[channel][2950:3000]) - min(data[channel][2950:3000])
			del_TC_1_cafs[int(channel[6:])-1,2] = max(data[channel][3100:3150]) - min(data[channel][3100:3150])
		if 'TC_A3_' in channel:
			del_TC_3_h2o[int(channel[6:])-1,0] = max(data[channel][1290:1350]) - min(data[channel][1290:1350])
			del_TC_3_h2o[int(channel[6:])-1,1] = max(data[channel][1600:1700]) - min(data[channel][1600:1700])
			del_TC_3_h2o[int(channel[6:])-1,2] = max(data[channel][2170:2250]) - min(data[channel][2170:2250])
			del_TC_3_cafs[int(channel[6:])-1,0] = max(data[channel][2450:2550]) - min(data[channel][2450:2550])
			del_TC_3_cafs[int(channel[6:])-1,1] = max(data[channel][2950:3000]) - min(data[channel][2950:3000])
			del_TC_3_cafs[int(channel[6:])-1,2] = max(data[channel][3100:3150]) - min(data[channel][3100:3150])
del_water = concatenate([del_TC_1_h2o, del_TC_3_h2o], axis=1)
del_cafs  = concatenate([del_TC_1_cafs, del_TC_3_cafs], axis=1)


fig = figure()
plot(del_water.mean(axis=1),y,'k',label='7/8 H$_2$O',linewidth=3)
plt.fill_betweenx(y,del_water.mean(axis=1)+del_water.std(axis=1),del_water.mean(axis=1)-del_water.std(axis=1), facecolor='black',alpha=0.5,linewidth=3)
plot(del_cafs.mean(axis=1),y,'r-',label='7/8 CAFS',linewidth=3)
plt.fill_betweenx(y,del_cafs.mean(axis=1)+del_cafs.std(axis=1),del_cafs.mean(axis=1)-del_cafs.std(axis=1), facecolor='red',alpha=0.25,linewidth=3)
ax1 = gca()
xlabel('$\Delta$T ($^{\circ}$C)')
ylabel('Height')
xticks(fontsize=16)
yticks(fontsize=16)
legend(numpoints=1,loc=1,fontsize=16)
axis([0, 85, 0, 12])
grid(True)
savefig(plot_dir + test_name + '_delta_T.pdf',format='pdf')


y = del_water.ravel()
X = del_cafs.ravel()
est = sm.OLS(y, X)
est = est.fit()
print est.summary()
X_prime = np.linspace(X.min(), X.max(), 100)[:, np.newaxis]
#X_prime = sm.add_constant(X_prime)  # add constant
y_hat = est.predict(X_prime)

fig = figure()
plt.scatter(X,y,alpha=0.5)
plt.plot(X_prime, y_hat, 'r', alpha=0.9)  # Add the regression line, colored in red
axis([0, 100, 0, 100])
xlabel('$\Delta$T ($^{\circ}$C) CAFS')
ylabel('$\Delta$T ($^{\circ}$C) H$_2$O')
savefig(plot_dir + test_name + '_scatter.pdf',format='pdf')

