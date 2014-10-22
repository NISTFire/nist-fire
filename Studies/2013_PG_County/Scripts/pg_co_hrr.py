#Weinschenk
#9-14

from __future__ import division

import numpy as np
import pandas as pd
from pylab import *

from matplotlib import rcParams
rcParams.update({'figure.autolayout': True})

def movingaverage(interval, window_size):
    window= np.ones(int(window_size))/float(window_size)
    return np.convolve(interval, window, 'same')

FDS_9MW_20 = pd.read_csv('../FDS_Output_Files/pg_county_20mph_9MW_devc.csv', header=1)
base_hrr_20mph_raw = np.zeros(len(FDS_9MW_20['Time']))
first_hrr_20mph_raw = np.zeros(len(FDS_9MW_20['Time']))
for i in FDS_9MW_20.columns:
    if 'Basement_HRR_' in i:
        base_hrr_20mph_raw += FDS_9MW_20[i]/1000
for i in FDS_9MW_20.columns:
    if 'FirstFloor_HRR_' in i:
        first_hrr_20mph_raw += FDS_9MW_20[i]/1000
base_hrr_20mph = movingaverage(base_hrr_20mph_raw,10)
first_hrr_20mph = movingaverage(first_hrr_20mph_raw,10)

FDS_9MW_10 = pd.read_csv('../FDS_Output_Files/pg_county_10mph_9MW_devc.csv', header=1)
base_hrr_10mph_raw = np.zeros(len(FDS_9MW_10['Time']))
first_hrr_10mph_raw = np.zeros(len(FDS_9MW_10['Time']))
for i in FDS_9MW_10.columns:
    if 'Basement_HRR_' in i:
        base_hrr_10mph_raw += FDS_9MW_10[i]/1000
for i in FDS_9MW_10.columns:
    if 'FirstFloor_HRR_' in i:
        first_hrr_10mph_raw += FDS_9MW_10[i]/1000
base_hrr_10mph = movingaverage(base_hrr_10mph_raw,10)
first_hrr_10mph = movingaverage(first_hrr_10mph_raw,10)

FDS_9MW_00 = pd.read_csv('../FDS_Output_Files/pg_county_0mph_9MW_devc.csv', header=1)
base_hrr_00mph_raw = np.zeros(len(FDS_9MW_00['Time']))
first_hrr_00mph_raw = np.zeros(len(FDS_9MW_00['Time']))
for i in FDS_9MW_00.columns:
    if 'Basement_HRR_' in i:
        base_hrr_00mph_raw += FDS_9MW_00[i]/1000
for i in FDS_9MW_00.columns:
    if 'FirstFloor_HRR_' in i:
        first_hrr_00mph_raw += FDS_9MW_00[i]/1000
base_hrr_00mph = movingaverage(base_hrr_00mph_raw,10)
first_hrr_00mph = movingaverage(first_hrr_00mph_raw,10)


fig = figure()
plot(FDS_9MW_00['Time'],base_hrr_00mph,'b-',mfc='none',label='FDS Model HRR (0 mph)',linewidth=2)
plot(FDS_9MW_10['Time'],base_hrr_10mph,'r:',mfc='none',label='FDS Model HRR (10 mph)',linewidth=2)
plot(FDS_9MW_20['Time'],base_hrr_20mph,'g--',mfc='none',label='FDS Model HRR (20 mph)',linewidth=2)
axvline(x=100,linestyle='-',linewidth=2,color = '#000000')
axvline(x=207,linestyle='-',linewidth=2,color = '#000000')
axvline(x=211,linestyle='-',linewidth=2,color = '#000000')
axvline(x=221,linestyle='-',linewidth=2,color = '#000000')
axvline(x=264,linestyle='-',linewidth=2,color = '#000000')
ax1 = gca()
xlim([0, 275])
ax1.xaxis.set_major_locator(MaxNLocator(8))
ax1_xlims = ax1.axis()[0:2]
xlabel('Time (s)')
ylabel('HRR (MW)')
legend(numpoints=1,loc=4 )
ax2 = ax1.twiny()
ax2.set_xlim(ax1_xlims)
ax2.set_xticks([100,207,211,221,264])
setp(xticks()[1], rotation=60)
labels = ['Front Door Open', 'Front Door Closed','Bottom Bay Window Open', 'Top Bay Window Open','Front Door Open']
ax2.set_xticklabels(labels, fontsize=8, ha='left')
axis([0, 275, 0, 10])
savefig('../Figures/PG_Basement_9MW_HRR.pdf',format='pdf')
close()

fig = figure()
plot(FDS_9MW_00['Time'],first_hrr_00mph,'b-',mfc='none',label='FDS Model HRR (0 mph)',linewidth=2)
plot(FDS_9MW_10['Time'],first_hrr_10mph,'r:',mfc='none',label='FDS Model HRR (10 mph)',linewidth=2)
plot(FDS_9MW_20['Time'],first_hrr_20mph,'g--',mfc='none',label='FDS Model HRR (20 mph)',linewidth=2)
axvline(x=100,linestyle='-',linewidth=2,color = '#000000')
axvline(x=207,linestyle='-',linewidth=2,color = '#000000')
axvline(x=211,linestyle='-',linewidth=2,color = '#000000')
axvline(x=221,linestyle='-',linewidth=2,color = '#000000')
axvline(x=264,linestyle='-',linewidth=2,color = '#000000')
ax1 = gca()
xlim([0, 275])
ax1.xaxis.set_major_locator(MaxNLocator(8))
ax1_xlims = ax1.axis()[0:2]
xlabel('Time (s)')
ylabel('HRR (MW)')
legend(numpoints=1,loc=2)
ax2 = ax1.twiny()
ax2.set_xlim(ax1_xlims)
ax2.set_xticks([100,207,211,221,264])
setp(xticks()[1], rotation=60)
labels = ['Front Door Open', 'Front Door Closed','Bottom Bay Window Open', 'Top Bay Window Open','Front Door Open']
ax2.set_xticklabels(labels, fontsize=8, ha='left')
axis([0, 275, 0, 10])
savefig('../Figures/PG_First_9MW_HRR.pdf',format='pdf')
close()

fig = figure()
plot(FDS_9MW_00['Time'],base_hrr_00mph+first_hrr_00mph,'b-',mfc='none',label='FDS Model HRR (0 mph)',linewidth=2)
plot(FDS_9MW_10['Time'],base_hrr_10mph+first_hrr_10mph,'r:',mfc='none',label='FDS Model HRR (10 mph)',linewidth=2)
plot(FDS_9MW_20['Time'],base_hrr_20mph+first_hrr_20mph,'g--',mfc='none',label='FDS Model HRR (20 mph)',linewidth=2)
axvline(x=100,linestyle='-',linewidth=2,color = '#000000')
axvline(x=207,linestyle='-',linewidth=2,color = '#000000')
axvline(x=211,linestyle='-',linewidth=2,color = '#000000')
axvline(x=221,linestyle='-',linewidth=2,color = '#000000')
axvline(x=264,linestyle='-',linewidth=2,color = '#000000')
ax1 = gca()
xlim([0, 275])
ax1.xaxis.set_major_locator(MaxNLocator(8))
ax1_xlims = ax1.axis()[0:2]
xlabel('Time (s)')
ylabel('HRR (MW)')
legend(numpoints=1,loc=4)
ax2 = ax1.twiny()
ax2.set_xlim(ax1_xlims)
ax2.set_xticks([100,207,211,221,264])
setp(xticks()[1], rotation=60)
labels = ['Front Door Open', 'Front Door Closed','Bottom Bay Window Open', 'Top Bay Window Open','Front Door Open']
ax2.set_xticklabels(labels, fontsize=8, ha='left')
axis([0, 275, 0, 10])
savefig('../Figures/PG_Total_9MW_HRR.pdf',format='pdf')
close()
