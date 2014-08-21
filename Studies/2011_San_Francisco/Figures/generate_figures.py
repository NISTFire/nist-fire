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

FDS_baseline_file = '../FDS_Output_Files/133_berkeley_fire_baseline_hrr.csv'
FDS_alternative_file = '../FDS_Output_Files/133_berkeley_fire_baseline_hrr.csv'

FDS_baseline = pd.read_csv(FDS_baseline_file, header=1)
HRR_baseline = FDS_baseline['HRR'] / 1000
HRR_baseline_avg = movingaverage(HRR_baseline, 2)

FDS_alternative = pd.read_csv(FDS_alternative_file, header=1)
HRR_alternative = FDS_alternative['HRR'] / 1000
HRR_alternative_avg = movingaverage(HRR_alternative, 2)

prescribed_time = np.array([0, 17, 23, 25, 35, 46, 53, 65, 80, 98, 112, 125, 133, 142, 144, 147, 157, 161, 167, 177, 184, 188, 195, 197, 201, 204, 205, 208, 215, 222, 230, 235, 241, 244, 246, 247, 250, 251, 253, 257, 260, 269, 273, 279, 282, 285, 288, 292, 295, 296, 297, 299, 300, 540])

prescribed_HRR = np.array([0, 5, 5, 16, 12, 12, 16, 20, 49, 98, 147, 199, 225, 236, 259, 266, 334, 338, 367, 420, 431, 424, 487, 543, 622, 637, 685, 715, 749, 786, 839, 869, 914, 996, 1037, 1041, 1074, 1078, 1149, 1213, 1303, 1580, 1733, 1793, 1883, 2006, 2118, 2350, 2560, 2687, 2952, 3110, 20000, 20000]) / 1000

figure()
plot(prescribed_time, prescribed_HRR, 'k-', lw=2, label='Prescribed HRR')
plot(FDS_baseline['Time'], HRR_baseline_avg, 'r--', lw=2, label='FDS Model HRR (Baseline Simulation)')
plot(FDS_alternative['Time'], HRR_alternative_avg, 'g-.', lw=2, label='FDS Model HRR (Alternative Simulation)')
plt.text(342+20, 2, 'Rear Window Failures Begin')
axvline(342, color='k', ls='--', lw=2)
ylim([0, 30])
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
