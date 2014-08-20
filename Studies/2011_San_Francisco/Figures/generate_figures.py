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

couch_time = np.array([0, 17, 23, 25, 35, 46, 53, 65, 80, 98, 112, 125, 133, 142, 144, 147, 157, 161, 167, 177, 184, 188, 195, 197, 201, 204, 205, 208, 215, 222, 230, 235, 241, 244, 246, 247, 250, 251, 253, 257, 260, 269, 273, 279, 282, 285, 288, 292, 295, 296, 297, 299, 302, 304, 306, 308, 310, 312, 314, 317, 319, 321, 322, 323, 326, 327, 332, 334, 336, 338, 339, 341, 342, 343, 345, 346, 347, 349, 352, 353, 355, 356, 358, 359, 360, 362, 363, 365, 366, 367, 369, 371, 372, 373, 375, 377, 378, 379, 380, 381, 382, 384, 385, 387, 388, 389, 390, 391, 392, 393, 394, 395, 396, 397, 398, 399, 400, 401, 402, 404, 405, 406, 407, 409, 410, 411, 414, 416, 418, 419, 420, 421, 422, 423, 425, 426, 427, 428, 429, 431, 432, 433, 434, 436, 437, 438, 439, 440, 442, 443, 444, 445, 446, 447, 448, 450, 451, 452, 453, 454, 455, 456, 457, 458, 459, 460, 462, 463, 464, 465, 466, 467, 469, 470, 471, 472, 473, 476, 478, 479, 480, 482, 485, 488, 490, 494, 497, 499, 500, 503, 504, 506, 507, 509, 511, 513, 515, 517, 519, 525, 526, 528, 530, 532, 534, 537, 539, 546, 550, 554, 557, 561, 564, 569, 578, 584, 588, 592, 597, 604, 613, 621, 625, 631, 637, 642, 644, 649, 653, 663, 671, 677, 687, 700, 718, 737, 751, 765, 780, 792, 803, 813, 821, 829, 837, 846, 855, 868, 877, 887, 900, 920, 933, 950, 969])

couch_HRR = np.array([0, 5, 5, 16, 12, 12, 16, 20, 49, 98, 147, 199, 225, 236, 259, 266, 334, 338, 367, 420, 431, 424, 487, 543, 622, 637, 685, 715, 749, 786, 839, 869, 914, 996, 1037, 1041, 1074, 1078, 1149, 1213, 1303, 1580, 1733, 1793, 1883, 2006, 2118, 2350, 2560, 2687, 2952, 3110, 3495, 3686, 3862, 3963, 4127, 4262, 4314, 4468, 4580, 4688, 4715, 4812, 4946, 5119, 5148, 4935, 5152, 5328, 5317, 5261, 5231, 5122, 5051, 4905, 4849, 4898, 4917, 5047, 4905, 5010, 5242, 5343, 5261, 5197, 5055, 5070, 4849, 4905, 4976, 5010, 5077, 5104, 5205, 4999, 5089, 5006, 5208, 5392, 5306, 5324, 5444, 5339, 5317, 5264, 4995, 4707, 4587, 4546, 4584, 4494, 4524, 4481, 4347, 4388, 4365, 4186, 4163, 4107, 4036, 3871, 3920, 3804, 3681, 3673, 3299, 3312, 3140, 3211, 3106, 3143, 3147, 3046, 3009, 2941, 2848, 2810, 2750, 2732, 2683, 2664, 2679, 2661, 2601, 2548, 2519, 2421, 2343, 2369, 2339, 2320, 2279, 2305, 2197, 2193, 2152, 2141, 2028, 2043, 2006, 1950, 1920, 1879, 1890, 1755, 1696, 1669, 1699, 1594, 1580, 1531, 1505, 1523, 1482, 1493, 1505, 1512, 1512, 1445, 1456, 1400, 1344, 1273, 1190, 1161, 1190, 1247, 1194, 1172, 1190, 1123, 1022, 959, 940, 880, 854, 887, 846, 854, 839, 839, 801, 775, 727, 712, 700, 719, 689, 655, 596, 536, 491, 468, 480, 480, 442, 424, 375, 356, 326, 319, 274, 259, 300, 308, 308, 259, 218, 222, 233, 233, 203, 184, 165, 150, 143, 121, 128, 117, 117, 106, 121, 113, 98, 106, 98, 98, 98, 91, 83, 83, 83, 83, 76]) / 1000

nominal_time = couch_time
nominal_HRR = couch_HRR

nominal_time
nominal_HRR[52:] += 15

print couch_time[52:]

print nominal_time
print nominal_HRR

figure()
plot(nominal_time, nominal_HRR, 'k-', lw=2, label='Nominal HRR')
plot(FDS_baseline['Time'], HRR_baseline_avg, 'r--', lw=2, label='FDS Model HRR (Baseline Simulation)')
plot(FDS_alternative['Time'], HRR_alternative_avg, 'g-.', lw=2, label='FDS Model HRR (Alternative Simulation)')
plt.text(342+20, 2, 'Rear Window Failures Begin')
axvline(342, color='k', ls='--', lw=2)
xlabel('Time(s)', fontsize=20)
ylabel('HRR (MW)', fontsize=20)
grid(True)
ax = gca()
for xlabel_i in ax.get_xticklabels():
    xlabel_i.set_fontsize(16)
for ylabel_i in ax.get_yticklabels():
    ylabel_i.set_fontsize(16)
savefig('Fire_HRR.pdf')
