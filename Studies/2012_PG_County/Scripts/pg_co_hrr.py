# -*- coding: utf-8 -*-
from __future__ import unicode_literals
#Weinschenk
#9-14

from __future__ import division

import numpy as np
import pandas as pd
from pylab import *
rc('font',**{'size':14})
params = {'legend.fontsize': 12,
          'legend.linewidth': 4,
          'lines.linewidth': 1.75,
          'lines.markersize': 6}
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
base_hrr_20mph = pd.rolling_mean(base_hrr_20mph_raw,10,center=True)
first_hrr_20mph = pd.rolling_mean(first_hrr_20mph_raw,10,center=True)

FDS_HRR_20 = pd.rolling_mean(pd.read_csv('../FDS_Output_Files/pg_county_20mph_9MW_hrr.csv', header=1),10,center=True)

HRR_theo = [None]*1000
HRR_time = list(range(1000))

for i in range (0, 999):
    if i <= 10:
        HRR_theo[i] = (8.55/10)*i
    elif i > 10 and i <= 207:
        HRR_theo[i] = 8.55
    elif i > 207 and i <= 267:
        HRR_theo[i] = 8.55 - (0.75*8.55/60)*(i-207)
    else:
        HRR_theo[i] = 0.25*8.55


fig = figure()
plt.plot(HRR_time,HRR_theo,'k-',mfc='none',label='Prescribed HRR')
plot(FDS_HRR_20['Time'],FDS_HRR_20['HRR']/1000.,'r-',mfc='none',label='Total Calculated HRR')
plot(FDS_9MW_20['Time'],base_hrr_20mph,'b--',mfc='none',label='Calculated Basement HRR')
axvline(x=100,linestyle='-',color = '#000000')
axvline(x=207,linestyle='-',color = '#000000')
axvline(x=211,linestyle='-',color = '#000000')
axvline(x=221,linestyle='-',color = '#000000')
axvline(x=267,linestyle='-',color = '#000000')
ax1 = gca()
xlim([100, 221])
ax1.xaxis.set_major_locator(MaxNLocator(8))
ax1_xlims = ax1.axis()[0:2]
xlabel('Time (s)')
ylabel('HRR (MW)')
legend(numpoints=1,loc=3 )
ax2 = ax1.twiny()
ax2.set_xlim(ax1_xlims)
ax2.set_xticks([100,206,211,221,267])
setp(xticks()[1], rotation=60)
labels = ['Front Door Open', 'Front Door Closed','Bottom Bay Window Open', 'Top Bay Window Open','Front Door Open']
ax2.set_xticklabels(labels, fontsize=12, ha='left')
plt.tick_params(\
    axis='x',
    which='both',
    bottom='off',
    top='off',
    labelbottom='off')
axis([100, 221, 6, 10])
savefig('../Figures/PG_Basement_9MW_HRR.pdf',format='pdf')
close()

fig = figure()
plot(FDS_9MW_20['Time'],first_hrr_20mph,'b--',mfc='none',label='Calculated First Floor HRR')
axvline(x=100,linestyle='-',color = '#000000')
axvline(x=207,linestyle='-',color = '#000000')
axvline(x=211,linestyle='-',color = '#000000')
axvline(x=221,linestyle='-',color = '#000000')
axvline(x=267,linestyle='-',color = '#000000')
ax1 = gca()
xlim([100, 221])
ax1.xaxis.set_major_locator(MaxNLocator(8))
ax1_xlims = ax1.axis()[0:2]
xlabel('Time (s)')
ylabel('HRR (MW)')
legend(numpoints=1,loc=2)
ax2 = ax1.twiny()
ax2.set_xlim(ax1_xlims)
ax2.set_xticks([100,206,211,221,267])
setp(xticks()[1], rotation=60)
labels = ['Front Door Open', 'Front Door Closed','Bottom Bay Window Open', 'Top Bay Window Open','Front Door Open']
ax2.set_xticklabels(labels, fontsize=12, ha='left')
plt.tick_params(\
    axis='x',
    which='both',
    bottom='off',
    top='off',
    labelbottom='off')
axis([100, 221, 0, 1])
savefig('../Figures/PG_First_9MW_HRR.pdf',format='pdf')
close()

fig = figure()
plt.plot(HRR_time,HRR_theo,'k-',mfc='none',label='Prescribed HRR')
plot(FDS_9MW_20['Time'],base_hrr_20mph+first_hrr_20mph,'b--',mfc='none',label='Structure Interior Calculated HRR')
axvline(x=100,linestyle='-',color = '#000000')
axvline(x=207,linestyle='-',color = '#000000')
axvline(x=211,linestyle='-',color = '#000000')
axvline(x=221,linestyle='-',color = '#000000')
axvline(x=267,linestyle='-',color = '#000000')
ax1 = gca()
xlim([0, 300])
ax1.xaxis.set_major_locator(MaxNLocator(8))
ax1_xlims = ax1.axis()[0:2]
xlabel('Time (s)')
ylabel('HRR (MW)')
legend(numpoints=1,loc=3)
ax2 = ax1.twiny()
ax2.set_xlim(ax1_xlims)
ax2.set_xticks([100,204,211,221,267])
setp(xticks()[1], rotation=60)
labels = ['Front Door Open', 'Front Door Closed','Bottom Bay Window Open', 'Top Bay Window Open','Front Door Open']
ax2.set_xticklabels(labels, fontsize=12, ha='left')
plt.tick_params(\
    axis='x',
    which='both',
    bottom='off',
    top='off',
    labelbottom='off')
axis([0, 300, 0, 10])
savefig('../Figures/PG_Total_9MW_HRR.pdf',format='pdf')
close()

fig = figure()
plt.plot(HRR_time,HRR_theo,'k-',mfc='none',label='Prescribed HRR')
plot(FDS_HRR_20['Time'],FDS_HRR_20['HRR']/1000.,'b--',mfc='none',label='Total Calculated HRR')
axvline(x=100,linestyle='-',color = '#000000')
axvline(x=207,linestyle='-',color = '#000000')
axvline(x=211,linestyle='-',color = '#000000')
axvline(x=221,linestyle='-',color = '#000000')
axvline(x=267 ,linestyle='-',color = '#000000')
ax1 = gca()
xlim([0, 300])
ax1.xaxis.set_major_locator(MaxNLocator(8))
ax1_xlims = ax1.axis()[0:2]
xlabel('Time (s)')
ylabel('HRR (MW)')
legend(numpoints=1,loc=3)
ax2 = ax1.twiny()
ax2.set_xlim(ax1_xlims)
ax2.set_xticks([100,204,211,221,267])
setp(xticks()[1], rotation=60)
labels = ['Front Door Open', 'Front Door Closed','Bottom Bay Window Open', 'Top Bay Window Open','Front Door Open']
ax2.set_xticklabels(labels, fontsize=12, ha='left')
plt.tick_params(\
    axis='x',
    which='both',
    bottom='off',
    top='off',
    labelbottom='off')
axis([0, 300, 0, 10])
savefig('../Figures/PG_9MW_HRR.pdf',format='pdf')
close()

fig = figure()
plt.plot(HRR_time,HRR_theo,'k-')
ax1 = gca()
plt.text(88, 8.625, 'Steady Burning')
plt.text(237, 5.35, 'Water on Fire')
xlabel('Time (s)')
ylabel('HRR (MW)')
grid(True)
ax = gca()
for xlabel_i in ax.get_xticklabels():
    xlabel_i.set_fontsize(16)
for ylabel_i in ax.get_yticklabels():
    ylabel_i.set_fontsize(16)
axis([0, 300, 0, 10])
savefig('../Figures/Fire_HRR.pdf',format='pdf')
close()

fig = figure()
plot(FDS_HRR_20['Time'], FDS_HRR_20['HRR']/1000. - base_hrr_20mph+first_hrr_20mph,'b--',mfc='none',label='Calculated HRR')
axvline(x=100,linestyle='-',color = '#000000')
axvline(x=207,linestyle='-',color = '#000000')
axvline(x=211,linestyle='-',color = '#000000')
axvline(x=221,linestyle='-',color = '#000000')
axvline(x=267 ,linestyle='-',color = '#000000')
ax1 = gca()
xlim([0, 300])
ax1.xaxis.set_major_locator(MaxNLocator(8))
ax1_xlims = ax1.axis()[0:2]
xlabel('Time (s)')
ylabel('HRR (MW)')
legend(numpoints=1,loc=1)
ax2 = ax1.twiny()
ax2.set_xlim(ax1_xlims)
ax2.set_xticks([100,204,211,221,267])
setp(xticks()[1], rotation=60)
labels = ['Front Door Open', 'Front Door Closed','Bottom Bay Window Open', 'Top Bay Window Open','Front Door Open']
ax2.set_xticklabels(labels, fontsize=12, ha='left')
plt.tick_params(\
    axis='x',
    which='both',
    bottom='off',
    top='off',
    labelbottom='off')
axis([0, 300, 0, 1.5])
savefig('../Figures/PG_HRR_diff.pdf',format='pdf')
close() 

