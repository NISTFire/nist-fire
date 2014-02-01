#Weinschenk
#8-7-13

import numpy as np
import matplotlib.pyplot as plt
from matplotlib import rc
rc('font',**{'family':'serif','serif':['Times New Roman'],'size':16})

def movingaverage(interval, window_size):
    window= np.ones(int(window_size))/float(window_size)
    return np.convolve(interval, window, 'same')


C_FDS = np.genfromtxt('../FDS_Output_Files/west_50th_fire_hrr.csv', delimiter=',', skip_header=1, dtype=None, names=True)
HRR = C_FDS['HRR']/1000
HRR_avg = movingaverage(HRR,10)

HRR_theo = [None]*1000
HRR_time = list(xrange(1000))

for i in range (0, 999):
	if i <= 8:
		HRR_theo[i] = (9/8)*i
	elif i > 8 and i <= 40:
		HRR_theo[i] = 9
	elif i > 40 and i <= 48:
		HRR_theo[i] = 9 + (3.3/8)*(i-40)
	else:
		HRR_theo[i] = 12.3

print HRR_avg[129],HRR_avg[160]

plt.figure
plt.plot(C_FDS['Time'],HRR_avg,'k-',mfc='none',label='West 50th Fire Model HRR',linewidth=2)
plt.plot(HRR_time,HRR_theo,'b',mfc='none',label='West 50th Fire Theory HRR',linewidth=2)
plt.axvline(x=130, ymin=0, ymax=0.615,label='Back Door Open',linestyle=':',linewidth=3,color = '#CC5500')
plt.axvline(x=160, ymin=0, ymax=0.615,label='Door Fail (Top)',linestyle='-.',linewidth=3,color = '#347235')
plt.axis([0, 250, 0, 20])
plt.xlabel('Time (s)')
plt.ylabel('HRR (MW)')
plt.legend(numpoints=1,frameon=False,loc=2)
plt.savefig('../Figures/Chicago_Fire_HRR.pdf',format='pdf')
plt.close()