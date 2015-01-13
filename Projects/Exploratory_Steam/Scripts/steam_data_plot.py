#Weinschenk
#9-14

from __future__ import division
import numpy as np
import pandas as pd
from pylab import *

from matplotlib import rcParams
rcParams.update({'figure.autolayout': True})

def DP_sub (b,c,temp,RH):
	DP_func = (c*(log(RH/100)+ (b*temp)/(c+temp)))/(b-(log(RH/100)+ (b*temp)/(c+temp)))
	return DP_func;
b = 17.67
c = 243.5

sample_rate = 6.

T80_RH97_FC = pd.read_csv('../Experimental_Data/80degC_97RH_Full_Chamber.csv', header=5)
TDP_T80_RH97_FC = np.zeros(len(T80_RH97_FC['Temperature (C)']))
T80_RH97_FC_Time = np.zeros(len(T80_RH97_FC['Temperature (C)']))

T80_RH97_FS = pd.read_csv('../Experimental_Data/80degC_97RH_Full_Sample.csv', header=5)
TDP_T80_RH97_FS = np.zeros(len(T80_RH97_FS['Temperature (C)']))
T80_RH97_FS_Time = np.zeros(len(T80_RH97_FS['Temperature (C)']))

for i in range(len(T80_RH97_FC)):
	T80_RH97_FC_Time[i] = -4476 + i*sample_rate
	TDP_T80_RH97_FC[i] = DP_sub(b,c,T80_RH97_FC['Temperature (C)'][i],T80_RH97_FC['Humidity (RH)'][i])

k=1		
for i in range(len(T80_RH97_FS)):
	T80_RH97_FS_Time[i] = -4398 + i*sample_rate
	TDP_T80_RH97_FS[i] = DP_sub(b,c,T80_RH97_FS['Temperature (C)'][i],T80_RH97_FS['Humidity (RH)'][i])
	if TDP_T80_RH97_FS[i] > 37 and k == 1:
		j = T80_RH97_FS_Time[i]
		k = -1

fig = figure()
plt.plot(T80_RH97_FC_Time,TDP_T80_RH97_FC,'rs',linewidth=2, label='Test Chamber Conditions')
plt.plot(T80_RH97_FS_Time,TDP_T80_RH97_FS,'bo',linewidth=2, label='Sample Penetration Conditions')
axvline(x=j,linestyle='-',linewidth=2,color = '#000000')
plt.text(j+5., 22, 'Temperature for skin burn reached at '+str(j)+' s', 
	 horizontalalignment='left',
     verticalalignment='center')
ax1 = gca()
xlabel('Time (s)')
ylabel('Dew Point Temperature ($^{\circ}$C)')
grid(True)
ax = gca()
legend(numpoints=1,loc=4)
axis([0, 1200, 0, 90])
savefig('../Figures/DewTemp_T80_RH97.pdf',format='pdf')
close()


