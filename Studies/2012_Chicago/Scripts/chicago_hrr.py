#Weinschenk
#8-7-13

import numpy as np
import matplotlib.pyplot as plt
from matplotlib import rc
rc('font',**{'family':'serif','serif':['Times New Roman'],'size':16})

def movingaverage(interval, window_size):
    window= np.ones(int(window_size))/float(window_size)
    return np.convolve(interval, window, 'same')

C_FDS = np.genfromtxt('../FDS_Output_Files/west_50th_baseline_hrr.csv', delimiter=',', skip_header=1, dtype=None, names=True)
HRR = C_FDS['HRR']/1000
HRR_avg = movingaverage(HRR,2)

ND_FDS = np.genfromtxt('../FDS_Output_Files/west_50th_norear_hrr.csv', delimiter=',', skip_header=1, dtype=None, names=True)
HRR_ND = ND_FDS['HRR']/1000
HRR_ND_avg = movingaverage(HRR_ND,2)

HRR_theo = [None]*1000
HRR_time = list(xrange(1000))

for i in range (0, 999):
	if i <= 10:
		HRR_theo[i] = (9./10)*i
	elif i > 10 and i <= 40:
		HRR_theo[i] = 9
	elif i > 40 and i <= 50:
		HRR_theo[i] = 9 + (3.3/10)*(i-40)
	else:
		HRR_theo[i] = 12.3

#print HRR_avg[129],HRR_avg[161],HRR_ND_avg[161]

plt.figure
plt.plot(HRR_time,HRR_theo,'b-.',mfc='none',label='Prescribed HRR',linewidth=2)
plt.plot(C_FDS['Time'],HRR_avg,'r-',mfc='none',label='FDS Model HRR (Baseline Simulation)',linewidth=2)
plt.plot(ND_FDS['Time'],HRR_ND_avg,'g--',mfc='none',label='FDS Model HRR (Alternative Simulation)',linewidth=2)
plt.text(98, 2, 'Rear Door Open', 
	 horizontalalignment='center',
     verticalalignment='center')
plt.text(195, 2, 'Interior Door Fail', 
	 horizontalalignment='center',
     verticalalignment='center')
plt.axvline(x=130, ymin=0, ymax=12.3/20,linestyle='-',linewidth=2,color = '#000000')
plt.axvline(x=160, ymin=0, ymax=12.3/20,linestyle='-',linewidth=2,color = '#000000')
plt.axis([0, 250, 0, 20])
plt.xlabel('Time (s)')
plt.ylabel('HRR (MW)')
plt.legend(numpoints=1,frameon=False,loc=2)
plt.savefig('../Figures/Chicago_Fire_HRR.pdf',format='pdf')
plt.close()