#!/usr/bin/env python

from __future__ import division

import numpy as np
import pandas as pd
from pylab import *

from matplotlib import rcParams
rcParams.update({'figure.autolayout': True})


def movingaverage(interval, window_size):
    window= np.ones(int(window_size))/float(window_size)
    return np.convolve(interval, window, 'same')

FDS_file = '../FDS_Output_Files/133_berkeley_fire_hrr.csv'
FDS = pd.read_csv(FDS_file, header=1)
HRR_FDS = FDS['HRR'] / 1000
HRR_FDS_avg = movingaverage(HRR_FDS, 10)

CALC_file = '../Supplemental_Calculations/FDS_HRR_ramps.csv'
CALC = pd.read_csv(CALC_file)
HRR_CALC = CALC['Total HRR (kW)'] / 1000

figure()
plot(CALC['Time (s)'], HRR_CALC, 'k-', lw=2, label='Prescribed HRR')
plot(FDS['Time'][:-4], HRR_FDS_avg[:-4], 'r--', lw=2, label='FDS Model HRR')
plt.text(342+10, 2, 'Rear Window Failures Begin')
axvline(342, color='k', ls='--', lw=2)
ylim([0, 35])
xlabel('Time(s)', fontsize=20)
ylabel('HRR (MW)', fontsize=20)
grid(True)
legend(loc='upper left')
ax = gca()
for xlabel_i in ax.get_xticklabels():
    xlabel_i.set_fontsize(16)
for ylabel_i in ax.get_yticklabels():
    ylabel_i.set_fontsize(16)
savefig('Fire_HRR.pdf')
