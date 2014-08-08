#Weinschenk
#7-14

import os
import numpy as np
import pandas as pd
from pylab import *

from matplotlib import rcParams
rcParams.update({'figure.autolayout': True})

def movingaverage(interval, window_size):
    window= np.ones(int(window_size))/float(window_size)
    return np.convolve(interval, window, 'same')

FDS_4MW_20 = np.genfromtxt('../FDS_Output_Files/pg_county_20mph_4MW_hrr.csv', delimiter=',', skip_header=1, dtype=None, names=True)
HRR_4MW_20 = FDS_4MW_20['HRR']/1000
HRR_4MW_20_avg = movingaverage(HRR_4MW_20,10)

FDS_9MW_20 = np.genfromtxt('../FDS_Output_Files/pg_county_20mph_9MW_hrr.csv', delimiter=',', skip_header=1, dtype=None, names=True)
HRR_9MW_20 = FDS_9MW_20['HRR']/1000
HRR_9MW_20_avg = movingaverage(HRR_9MW_20,10)

FDSdevc_9MW_20 = np.genfromtxt('../FDS_Output_Files/pg_county_20mph_9MW_devc.csv', delimiter=',', skip_header=1, dtype=None, names=True)
HRR_B_9MW_20 = FDSdevc_9MW_20['Basement_HRR']/1000
HRR_1_9MW_20 = FDSdevc_9MW_20['First_Floor_HRR']/1000
HRR_B_9MW_20_avg = movingaverage(HRR_B_9MW_20,10)
HRR_1_9MW_20_avg = movingaverage(HRR_1_9MW_20,10)
HRR_T_9MW_20_avg = HRR_B_9MW_20_avg + HRR_1_9MW_20_avg

FDS_9MW_10 = np.genfromtxt('../FDS_Output_Files/pg_county_10mph_9MW_hrr.csv', delimiter=',', skip_header=1, dtype=None, names=True)
HRR_9MW_10 = FDS_9MW_10['HRR']/1000
HRR_9MW_10_avg = movingaverage(HRR_9MW_10,10)

FDSdevc_9MW_10 = np.genfromtxt('../FDS_Output_Files/pg_county_10mph_9MW_devc.csv', delimiter=',', skip_header=1, dtype=None, names=True)
HRR_B_9MW_10 = FDSdevc_9MW_10['Basement_HRR']/1000
HRR_1_9MW_10 = FDSdevc_9MW_10['First_Floor_HRR']/1000
HRR_B_9MW_10_avg = movingaverage(HRR_B_9MW_10,10)
HRR_1_9MW_10_avg = movingaverage(HRR_1_9MW_10,10)

FDS_9MW_00 = np.genfromtxt('../FDS_Output_Files/pg_county_10mph_9MW_hrr.csv', delimiter=',', skip_header=1, dtype=None, names=True)
HRR_9MW_00 = FDS_9MW_00['HRR']/1000
HRR_9MW_00_avg = movingaverage(HRR_9MW_00,10)

FDSdevc_9MW_00 = np.genfromtxt('../FDS_Output_Files/pg_county_0mph_9MW_devc.csv', delimiter=',', skip_header=1, dtype=None, names=True)
HRR_B_9MW_00 = FDSdevc_9MW_00['Basement_HRR']/1000
HRR_1_9MW_00 = FDSdevc_9MW_00['First_Floor_HRR']/1000
HRR_B_9MW_00_avg = movingaverage(HRR_B_9MW_00,10)
HRR_1_9MW_00_avg = movingaverage(HRR_1_9MW_00,10)

# plt.figure
# plt.plot(FDS_4MW_20['Time'],HRR_4MW_20_avg,'r-',mfc='none',label='FDS Model HRR (4 MW)',linewidth=2)
# plt.plot(FDS_9MW_20['Time'],HRR_9MW_20_avg,'g--',mfc='none',label='FDS Model HRR (9 MW)',linewidth=2)
# plt.axvline(x=100, ymin=0, ymax=10./15,linestyle='-',linewidth=2,color = '#000000')
# plt.axvline(x=160, ymin=0, ymax=10./15,linestyle='-',linewidth=2,color = '#000000')
# plt.axvline(x=170, ymin=0, ymax=10./15,linestyle='-',linewidth=2,color = '#000000')
# plt.axvline(x=180, ymin=0, ymax=10./15,linestyle='-',linewidth=2,color = '#000000')
# plt.axis([0, 250, 0, 15])
# plt.xlabel('Time (s)')
# plt.ylabel('HRR (MW)')
# plt.legend(numpoints=1,frameon=False,loc=2)
# plt.savefig('../Figures/PG_CO_20mph_HRR.pdf',format='pdf')
# plt.close()

# plt.figure
# plt.plot(FDS_9MW_00['Time'],HRR_9MW_00_avg,'b.-',mfc='none',label='FDS Model HRR (0 mph)',linewidth=2)
# plt.plot(FDS_9MW_10['Time'],HRR_9MW_10_avg,'r-',mfc='none',label='FDS Model HRR (10 mph)',linewidth=2)
# plt.plot(FDS_9MW_20['Time'],HRR_9MW_20_avg,'g--',mfc='none',label='FDS Model HRR (20 mph)',linewidth=2)
# plt.axvline(x=100, ymin=0, ymax=10./15,linestyle='-',linewidth=2,color = '#000000')
# plt.axvline(x=160, ymin=0, ymax=10./15,linestyle='-',linewidth=2,color = '#000000')
# plt.axvline(x=170, ymin=0, ymax=10./15,linestyle='-',linewidth=2,color = '#000000')
# plt.axvline(x=180, ymin=0, ymax=10./15,linestyle='-',linewidth=2,color = '#000000')
# plt.axis([0, 250, 0, 15])
# plt.xlabel('Time (s)')
# plt.ylabel('HRR (MW)')
# plt.legend(numpoints=1,frameon=False,loc=2)
# plt.savefig('../Figures/PG_CO_9MW_HRR.pdf',format='pdf')
# plt.close()

fig = figure()
plot(FDSdevc_9MW_00['Time'],HRR_B_9MW_00_avg,'b.-',mfc='none',label='FDS Model HRR (0 mph)',linewidth=2)
plot(FDSdevc_9MW_10['Time'],HRR_B_9MW_10_avg,'r-',mfc='none',label='FDS Model HRR (10 mph)',linewidth=2)
plot(FDSdevc_9MW_20['Time'],HRR_B_9MW_20_avg,'g--',mfc='none',label='FDS Model HRR (20 mph)',linewidth=2)
axvline(x=100,linestyle='-',linewidth=2,color = '#000000')
axvline(x=160,linestyle='-',linewidth=2,color = '#000000')
axvline(x=170,linestyle='-',linewidth=2,color = '#000000')
axvline(x=180,linestyle='-',linewidth=2,color = '#000000')
ax1 = gca()
xlim([0, 250])
ax1.xaxis.set_major_locator(MaxNLocator(8))
ax1_xlims = ax1.axis()[0:2]
xlabel('Time (s)')
ylabel('HRR (MW)')
legend(numpoints=1,loc=2)
ax2 = ax1.twiny()
ax2.set_xlim(ax1_xlims)
ax2.set_xticks([100,160,170,180])
setp(xticks()[1], rotation=60)
labels = ['Front Door Open', 'Front Door Closed','Bay Window Open', 'Front Door Open']
ax2.set_xticklabels(labels, fontsize=8, ha='left')
xlim([0, 250])
axis([0, 250, 0, 10])
savefig('../Figures/PG_B_9MW_HRR.pdf',format='pdf')
close()

fig = figure()
plot(FDSdevc_9MW_00['Time'],HRR_1_9MW_00_avg,'b.-',mfc='none',label='FDS Model HRR (0 mph)',linewidth=2)
plot(FDSdevc_9MW_10['Time'],HRR_1_9MW_10_avg,'r-',mfc='none',label='FDS Model HRR (10 mph)',linewidth=2)
plot(FDSdevc_9MW_20['Time'],HRR_1_9MW_20_avg,'g--',mfc='none',label='FDS Model HRR (20 mph)',linewidth=2)
axvline(x=100,linestyle='-',linewidth=2,color = '#000000')
axvline(x=160,linestyle='-',linewidth=2,color = '#000000')
axvline(x=170,linestyle='-',linewidth=2,color = '#000000')
axvline(x=180,linestyle='-',linewidth=2,color = '#000000')
ax1 = gca()
xlim([0, 250])
ax1.xaxis.set_major_locator(MaxNLocator(8))
ax1_xlims = ax1.axis()[0:2]
xlabel('Time (s)')
ylabel('HRR (MW)')
legend(numpoints=1,loc=2)
ax2 = ax1.twiny()
ax2.set_xlim(ax1_xlims)
ax2.set_xticks([100,160,170,180])
setp(xticks()[1], rotation=60)
labels = ['Front Door Open', 'Front Door Closed','Bay Window Open', 'Front Door Open']
ax2.set_xticklabels(labels, fontsize=8, ha='left')
xlim([0, 250])
axis([0, 250, 0, 2])
savefig('../Figures/PG_1_9MW_HRR.pdf',format='pdf')
close()


