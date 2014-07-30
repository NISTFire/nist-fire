#!/usr/bin/env python

import numpy as np
import pandas as pd
from pylab import *

from matplotlib import rcParams
rcParams.update({'figure.autolayout': True})


def smooth(x, window_len=5, window='flat'):
    """smooth the data using a window with requested size.
    
    This method is based on the convolution of a scaled window with the signal.
    The signal is prepared by introducing reflected copies of the signal 
    (with the window size) in both ends so that transient parts are minimized
    in the begining and end part of the output signal.
    
    input:
        x: the input signal 
        window_len: the dimension of the smoothing window; should be an odd integer
        window: the type of window from 'flat', 'hanning', 'hamming', 'bartlett', 'blackman'
            flat window will produce a moving average smoothing.

    output:
        the smoothed signal
        
    example:

    t=linspace(-2,2,0.1)
    x=sin(t)+randn(len(t))*0.1
    y=smooth(x)
    
    see also: 
    
    np.hanning, np.hamming, np.bartlett, np.blackman, np.convolve
    scipy.signal.lfilter
 
    TODO: the window parameter could be the window itself if an array instead of a string
    NOTE: length(output) != length(input), to correct this: return y[(window_len/2-1):-(window_len/2)] instead of just y.
    """

    if x.ndim != 1:
        raise ValueError, "smooth only accepts 1 dimension arrays."

    if x.size < window_len:
        raise ValueError, "Input vector needs to be bigger than window size."

    if window_len<3:
        return x

    if not window in ['flat', 'hanning', 'hamming', 'bartlett', 'blackman']:
        raise ValueError, "Window options are 'flat', 'hanning', 'hamming', 'bartlett', 'blackman'"

    s=np.r_[x[window_len-1:0:-1],x,x[-1:-window_len:-1]]

    if window == 'flat':
        w=np.ones(window_len,'d')
    else:
        w=eval('np.'+window+'(window_len)')

    y=np.convolve(w/w.sum(),s,mode='valid')
    return y

#  =====================
#  = Read in exp. data =
#  =====================

data_dir = '../Experimental_Data/'

Slug_Only_50_C_40_Hz = pd.read_csv(data_dir + 'Slug_Only/' + '50_C_40_Hz.csv')
Slug_Only_50_C_60_Hz = pd.read_csv(data_dir + 'Slug_Only/' + '50_C_60_Hz.csv')
Slug_Only_100_C_40_Hz = pd.read_csv(data_dir + 'Slug_Only/' + '100_C_40_Hz.csv')
Slug_Only_100_C_60_Hz = pd.read_csv(data_dir + 'Slug_Only/' + '100_C_60_Hz.csv')
Slug_Only_150_C_40_Hz = pd.read_csv(data_dir + 'Slug_Only/' + '150_C_40_Hz.csv')
Slug_Only_150_C_60_Hz = pd.read_csv(data_dir + 'Slug_Only/' + '150_C_60_Hz.csv')

Gear_No_Slug_50_C_40_Hz_Test_1 = pd.read_csv(data_dir + 'Gear_No_Slug/' + '50_C_40_Hz_Test_1.csv')
Gear_No_Slug_50_C_40_Hz_Test_2 = pd.read_csv(data_dir + 'Gear_No_Slug/' + '50_C_40_Hz_Test_2.csv')
Gear_No_Slug_50_C_40_Hz_Test_3 = pd.read_csv(data_dir + 'Gear_No_Slug/' + '50_C_40_Hz_Test_3.csv')
Gear_No_Slug_50_C_60_Hz_Test_1 = pd.read_csv(data_dir + 'Gear_No_Slug/' + '50_C_60_Hz_Test_1.csv')
Gear_No_Slug_50_C_60_Hz_Test_2 = pd.read_csv(data_dir + 'Gear_No_Slug/' + '50_C_60_Hz_Test_2.csv')
Gear_No_Slug_50_C_60_Hz_Test_3 = pd.read_csv(data_dir + 'Gear_No_Slug/' + '50_C_60_Hz_Test_3.csv')
Gear_No_Slug_100_C_40_Hz_Test_1 = pd.read_csv(data_dir + 'Gear_No_Slug/' + '100_C_40_Hz_Test_1.csv')
Gear_No_Slug_100_C_40_Hz_Test_2 = pd.read_csv(data_dir + 'Gear_No_Slug/' + '100_C_40_Hz_Test_2.csv')
Gear_No_Slug_100_C_40_Hz_Test_3 = pd.read_csv(data_dir + 'Gear_No_Slug/' + '100_C_40_Hz_Test_3.csv')
Gear_No_Slug_100_C_60_Hz_Test_1 = pd.read_csv(data_dir + 'Gear_No_Slug/' + '100_C_60_Hz_Test_1.csv')
Gear_No_Slug_100_C_60_Hz_Test_2 = pd.read_csv(data_dir + 'Gear_No_Slug/' + '100_C_60_Hz_Test_2.csv')
Gear_No_Slug_100_C_60_Hz_Test_3 = pd.read_csv(data_dir + 'Gear_No_Slug/' + '100_C_60_Hz_Test_3.csv')
Gear_No_Slug_150_C_40_Hz_Test_1 = pd.read_csv(data_dir + 'Gear_No_Slug/' + '150_C_40_Hz_Test_1.csv')
Gear_No_Slug_150_C_40_Hz_Test_2 = pd.read_csv(data_dir + 'Gear_No_Slug/' + '150_C_40_Hz_Test_2.csv')
Gear_No_Slug_150_C_40_Hz_Test_3 = pd.read_csv(data_dir + 'Gear_No_Slug/' + '150_C_40_Hz_Test_3.csv')
Gear_No_Slug_150_C_60_Hz_Test_1 = pd.read_csv(data_dir + 'Gear_No_Slug/' + '150_C_60_Hz_Test_1.csv')
Gear_No_Slug_150_C_60_Hz_Test_2 = pd.read_csv(data_dir + 'Gear_No_Slug/' + '150_C_60_Hz_Test_2.csv')
Gear_No_Slug_150_C_60_Hz_Test_3 = pd.read_csv(data_dir + 'Gear_No_Slug/' + '150_C_60_Hz_Test_3.csv')

Gear_With_Slug_50_C_40_Hz_Test_1 = pd.read_csv(data_dir + 'Gear_With_Slug/' + '50_C_40_Hz_Test_1.csv')
Gear_With_Slug_50_C_40_Hz_Test_2 = pd.read_csv(data_dir + 'Gear_With_Slug/' + '50_C_40_Hz_Test_2.csv')
Gear_With_Slug_50_C_40_Hz_Test_3 = pd.read_csv(data_dir + 'Gear_With_Slug/' + '50_C_40_Hz_Test_3.csv')
Gear_With_Slug_50_C_60_Hz_Test_1 = pd.read_csv(data_dir + 'Gear_With_Slug/' + '50_C_60_Hz_Test_1.csv')
Gear_With_Slug_50_C_60_Hz_Test_2 = pd.read_csv(data_dir + 'Gear_With_Slug/' + '50_C_60_Hz_Test_2.csv')
Gear_With_Slug_50_C_60_Hz_Test_3 = pd.read_csv(data_dir + 'Gear_With_Slug/' + '50_C_60_Hz_Test_3.csv')
Gear_With_Slug_100_C_40_Hz_Test_1 = pd.read_csv(data_dir + 'Gear_With_Slug/' + '100_C_40_Hz_Test_1.csv')
Gear_With_Slug_100_C_40_Hz_Test_2 = pd.read_csv(data_dir + 'Gear_With_Slug/' + '100_C_40_Hz_Test_2.csv')
Gear_With_Slug_100_C_40_Hz_Test_3 = pd.read_csv(data_dir + 'Gear_With_Slug/' + '100_C_40_Hz_Test_3.csv')
Gear_With_Slug_100_C_60_Hz_Test_1 = pd.read_csv(data_dir + 'Gear_With_Slug/' + '100_C_60_Hz_Test_1.csv')
Gear_With_Slug_100_C_60_Hz_Test_2 = pd.read_csv(data_dir + 'Gear_With_Slug/' + '100_C_60_Hz_Test_2.csv')
Gear_With_Slug_100_C_60_Hz_Test_3 = pd.read_csv(data_dir + 'Gear_With_Slug/' + '100_C_60_Hz_Test_3.csv')
Gear_With_Slug_150_C_40_Hz_Test_1 = pd.read_csv(data_dir + 'Gear_With_Slug/' + '150_C_40_Hz_Test_1.csv')
Gear_With_Slug_150_C_40_Hz_Test_2 = pd.read_csv(data_dir + 'Gear_With_Slug/' + '150_C_40_Hz_Test_2.csv')
Gear_With_Slug_150_C_40_Hz_Test_3 = pd.read_csv(data_dir + 'Gear_With_Slug/' + '150_C_40_Hz_Test_3.csv')
Gear_With_Slug_150_C_60_Hz_Test_1 = pd.read_csv(data_dir + 'Gear_With_Slug/' + '150_C_60_Hz_Test_1.csv')
Gear_With_Slug_150_C_60_Hz_Test_2 = pd.read_csv(data_dir + 'Gear_With_Slug/' + '150_C_60_Hz_Test_2.csv')
Gear_With_Slug_150_C_60_Hz_Test_3 = pd.read_csv(data_dir + 'Gear_With_Slug/' + '150_C_60_Hz_Test_3.csv')

#  ============
#  = Plotting =
#  ============

fig = figure()
plot(Slug_Only_50_C_40_Hz['Time (s)'], Slug_Only_50_C_40_Hz['Outside TC (C)'], lw=1.5, ls='--', color='r', label='Outside TC')
plot(Slug_Only_50_C_40_Hz['Time (s)'], Slug_Only_50_C_40_Hz['Surface TC (C)'], lw=1.5, ls='-.', color='g', label='Surface TC')
plot(Slug_Only_50_C_40_Hz['Time (s)'], Slug_Only_50_C_40_Hz['Slug TC (C)'], lw=1.5, ls='-', color='b', label='Slug TC')
grid(True)
xlabel('Time', fontsize=20)
ylabel('Temperature ($^\circ$C)', fontsize=20)
xticks(fontsize=16)
yticks(fontsize=16)
ylim([0, 160])
legend(loc='upper right')
savefig('../Figures/Slug_Only_Temperature_50_C_40_Hz.pdf')

fig = figure()
plot(Slug_Only_50_C_60_Hz['Time (s)'], Slug_Only_50_C_60_Hz['Outside TC (C)'], lw=1.5, ls='--', color='r', label='Outside TC')
plot(Slug_Only_50_C_60_Hz['Time (s)'], Slug_Only_50_C_60_Hz['Surface TC (C)'], lw=1.5, ls='-.', color='g', label='Surface TC')
plot(Slug_Only_50_C_60_Hz['Time (s)'], Slug_Only_50_C_60_Hz['Slug TC (C)'], lw=1.5, ls='-', color='b', label='Slug TC')
grid(True)
xlabel('Time', fontsize=20)
ylabel('Temperature ($^\circ$C)', fontsize=20)
xticks(fontsize=16)
yticks(fontsize=16)
ylim([0, 160])
legend(loc='upper right')
savefig('../Figures/Slug_Only_Temperature_50_C_60_Hz.pdf')

fig = figure()
plot(Slug_Only_100_C_40_Hz['Time (s)'], Slug_Only_100_C_40_Hz['Outside TC (C)'], lw=1.5, ls='--', color='r', label='Outside TC')
plot(Slug_Only_100_C_40_Hz['Time (s)'], Slug_Only_100_C_40_Hz['Surface TC (C)'], lw=1.5, ls='-.', color='g', label='Surface TC')
plot(Slug_Only_100_C_40_Hz['Time (s)'], Slug_Only_100_C_40_Hz['Slug TC (C)'], lw=1.5, ls='-', color='b', label='Slug TC')
grid(True)
xlabel('Time', fontsize=20)
ylabel('Temperature ($^\circ$C)', fontsize=20)
xticks(fontsize=16)
yticks(fontsize=16)
ylim([0, 160])
legend(loc='upper right')
savefig('../Figures/Slug_Only_Temperature_100_C_40_Hz.pdf')

fig = figure()
plot(Slug_Only_100_C_60_Hz['Time (s)'], Slug_Only_100_C_60_Hz['Outside TC (C)'], lw=1.5, ls='--', color='r', label='Outside TC')
plot(Slug_Only_100_C_60_Hz['Time (s)'], Slug_Only_100_C_60_Hz['Surface TC (C)'], lw=1.5, ls='-.', color='g', label='Surface TC')
plot(Slug_Only_100_C_60_Hz['Time (s)'], Slug_Only_100_C_60_Hz['Slug TC (C)'], lw=1.5, ls='-', color='b', label='Slug TC')
grid(True)
xlabel('Time', fontsize=20)
ylabel('Temperature ($^\circ$C)', fontsize=20)
xticks(fontsize=16)
yticks(fontsize=16)
ylim([0, 160])
legend(loc='upper right')
savefig('../Figures/Slug_Only_Temperature_100_C_60_Hz.pdf')

fig = figure()
plot(Slug_Only_150_C_40_Hz['Time (s)'], Slug_Only_150_C_40_Hz['Outside TC (C)'], lw=1.5, ls='--', color='r', label='Outside TC')
plot(Slug_Only_150_C_40_Hz['Time (s)'], Slug_Only_150_C_40_Hz['Surface TC (C)'], lw=1.5, ls='-.', color='g', label='Surface TC')
plot(Slug_Only_150_C_40_Hz['Time (s)'], Slug_Only_150_C_40_Hz['Slug TC (C)'], lw=1.5, ls='-', color='b', label='Slug TC')
grid(True)
xlabel('Time', fontsize=20)
ylabel('Temperature ($^\circ$C)', fontsize=20)
xticks(fontsize=16)
yticks(fontsize=16)
ylim([0, 160])
legend(loc='upper right')
savefig('../Figures/Slug_Only_Temperature_150_C_40_Hz.pdf')

fig = figure()
plot(Slug_Only_150_C_60_Hz['Time (s)'], Slug_Only_150_C_60_Hz['Outside TC (C)'], lw=1.5, ls='--', color='r', label='Outside TC')
plot(Slug_Only_150_C_60_Hz['Time (s)'], Slug_Only_150_C_60_Hz['Surface TC (C)'], lw=1.5, ls='-.', color='g', label='Surface TC')
plot(Slug_Only_150_C_60_Hz['Time (s)'], Slug_Only_150_C_60_Hz['Slug TC (C)'], lw=1.5, ls='-', color='b', label='Slug TC')
grid(True)
xlabel('Time', fontsize=20)
ylabel('Temperature ($^\circ$C)', fontsize=20)
xticks(fontsize=16)
yticks(fontsize=16)
ylim([0, 160])
legend(loc='upper right')
savefig('../Figures/Slug_Only_Temperature_150_C_60_Hz.pdf')

####################################################################################################################################
####################################################################################################################################
####################################################################################################################################

fig = figure()
plot(Gear_No_Slug_50_C_40_Hz_Test_1['Time (s)'], Gear_No_Slug_50_C_40_Hz_Test_1['Gear Outside TC (C)'], lw=1.5, ls='-', color='r', label='Test 1')
plot(Gear_No_Slug_50_C_40_Hz_Test_2['Time (s)'], Gear_No_Slug_50_C_40_Hz_Test_2['Gear Outside TC (C)'], lw=1.5, ls='-', color='g', label='Test 2')
plot(Gear_No_Slug_50_C_40_Hz_Test_3['Time (s)'], Gear_No_Slug_50_C_40_Hz_Test_3['Gear Outside TC (C)'], lw=1.5, ls='-', color='b', label='Test 3')
plot(Gear_No_Slug_50_C_40_Hz_Test_1['Time (s)'], Gear_No_Slug_50_C_40_Hz_Test_1['Gear Inside TC (C)'], lw=1.5, ls='--', color='r', label='Test 1')
plot(Gear_No_Slug_50_C_40_Hz_Test_2['Time (s)'], Gear_No_Slug_50_C_40_Hz_Test_2['Gear Inside TC (C)'], lw=1.5, ls='--', color='g', label='Test 2')
plot(Gear_No_Slug_50_C_40_Hz_Test_3['Time (s)'], Gear_No_Slug_50_C_40_Hz_Test_3['Gear Inside TC (C)'], lw=1.5, ls='--', color='b', label='Test 3')
grid(True)
xlabel('Time', fontsize=20)
ylabel('Temperature ($^\circ$C)', fontsize=20)
xticks(fontsize=16)
yticks(fontsize=16)
ylim([0, 160])
legend(loc='upper right')
savefig('../Figures/Gear_No_Slug_Temperature_50_C_40_Hz.pdf')

fig = figure()
plot(Gear_No_Slug_50_C_60_Hz_Test_1['Time (s)'], Gear_No_Slug_50_C_60_Hz_Test_1['Gear Outside TC (C)'], lw=1.5, ls='-', color='r', label='Test 1')
plot(Gear_No_Slug_50_C_60_Hz_Test_2['Time (s)'], Gear_No_Slug_50_C_60_Hz_Test_2['Gear Outside TC (C)'], lw=1.5, ls='-', color='g', label='Test 2')
plot(Gear_No_Slug_50_C_60_Hz_Test_3['Time (s)'], Gear_No_Slug_50_C_60_Hz_Test_3['Gear Outside TC (C)'], lw=1.5, ls='-', color='b', label='Test 3')
plot(Gear_No_Slug_50_C_60_Hz_Test_1['Time (s)'], Gear_No_Slug_50_C_60_Hz_Test_1['Gear Inside TC (C)'], lw=1.5, ls='--', color='r', label='Test 1')
plot(Gear_No_Slug_50_C_60_Hz_Test_2['Time (s)'], Gear_No_Slug_50_C_60_Hz_Test_2['Gear Inside TC (C)'], lw=1.5, ls='--', color='g', label='Test 2')
plot(Gear_No_Slug_50_C_60_Hz_Test_3['Time (s)'], Gear_No_Slug_50_C_60_Hz_Test_3['Gear Inside TC (C)'], lw=1.5, ls='--', color='b', label='Test 3')
grid(True)
xlabel('Time', fontsize=20)
ylabel('Temperature ($^\circ$C)', fontsize=20)
xticks(fontsize=16)
yticks(fontsize=16)
ylim([0, 160])
legend(loc='upper right')
savefig('../Figures/Gear_No_Slug_Temperature_50_C_60_Hz.pdf')

fig = figure()
plot(Gear_No_Slug_100_C_40_Hz_Test_1['Time (s)'], Gear_No_Slug_100_C_40_Hz_Test_1['Gear Outside TC (C)'], lw=1.5, ls='-', color='r', label='Test 1')
plot(Gear_No_Slug_100_C_40_Hz_Test_2['Time (s)'], Gear_No_Slug_100_C_40_Hz_Test_2['Gear Outside TC (C)'], lw=1.5, ls='-', color='g', label='Test 2')
plot(Gear_No_Slug_100_C_40_Hz_Test_3['Time (s)'], Gear_No_Slug_100_C_40_Hz_Test_3['Gear Outside TC (C)'], lw=1.5, ls='-', color='b', label='Test 3')
plot(Gear_No_Slug_100_C_40_Hz_Test_1['Time (s)'], Gear_No_Slug_100_C_40_Hz_Test_1['Gear Inside TC (C)'], lw=1.5, ls='--', color='r', label='Test 1')
plot(Gear_No_Slug_100_C_40_Hz_Test_2['Time (s)'], Gear_No_Slug_100_C_40_Hz_Test_2['Gear Inside TC (C)'], lw=1.5, ls='--', color='g', label='Test 2')
plot(Gear_No_Slug_100_C_40_Hz_Test_3['Time (s)'], Gear_No_Slug_100_C_40_Hz_Test_3['Gear Inside TC (C)'], lw=1.5, ls='--', color='b', label='Test 3')
grid(True)
xlabel('Time', fontsize=20)
ylabel('Temperature ($^\circ$C)', fontsize=20)
xticks(fontsize=16)
yticks(fontsize=16)
ylim([0, 160])
legend(loc='upper right')
savefig('../Figures/Gear_No_Slug_Temperature_100_C_40_Hz.pdf')

fig = figure()
plot(Gear_No_Slug_100_C_60_Hz_Test_1['Time (s)'], Gear_No_Slug_100_C_60_Hz_Test_1['Gear Outside TC (C)'], lw=1.5, ls='-', color='r', label='Test 1')
plot(Gear_No_Slug_100_C_60_Hz_Test_2['Time (s)'], Gear_No_Slug_100_C_60_Hz_Test_2['Gear Outside TC (C)'], lw=1.5, ls='-', color='g', label='Test 2')
plot(Gear_No_Slug_100_C_60_Hz_Test_3['Time (s)'], Gear_No_Slug_100_C_60_Hz_Test_3['Gear Outside TC (C)'], lw=1.5, ls='-', color='b', label='Test 3')
plot(Gear_No_Slug_100_C_60_Hz_Test_1['Time (s)'], Gear_No_Slug_100_C_60_Hz_Test_1['Gear Inside TC (C)'], lw=1.5, ls='--', color='r', label='Test 1')
plot(Gear_No_Slug_100_C_60_Hz_Test_2['Time (s)'], Gear_No_Slug_100_C_60_Hz_Test_2['Gear Inside TC (C)'], lw=1.5, ls='--', color='g', label='Test 2')
plot(Gear_No_Slug_100_C_60_Hz_Test_3['Time (s)'], Gear_No_Slug_100_C_60_Hz_Test_3['Gear Inside TC (C)'], lw=1.5, ls='--', color='b', label='Test 3')
grid(True)
xlabel('Time', fontsize=20)
ylabel('Temperature ($^\circ$C)', fontsize=20)
xticks(fontsize=16)
yticks(fontsize=16)
ylim([0, 160])
legend(loc='upper right')
savefig('../Figures/Gear_No_Slug_Temperature_100_C_60_Hz.pdf')

fig = figure()
plot(Gear_No_Slug_150_C_40_Hz_Test_1['Time (s)'], Gear_No_Slug_150_C_40_Hz_Test_1['Gear Outside TC (C)'], lw=1.5, ls='-', color='r', label='Test 1')
plot(Gear_No_Slug_150_C_40_Hz_Test_2['Time (s)'], Gear_No_Slug_150_C_40_Hz_Test_2['Gear Outside TC (C)'], lw=1.5, ls='-', color='g', label='Test 2')
plot(Gear_No_Slug_150_C_40_Hz_Test_3['Time (s)'], Gear_No_Slug_150_C_40_Hz_Test_3['Gear Outside TC (C)'], lw=1.5, ls='-', color='b', label='Test 3')
plot(Gear_No_Slug_150_C_40_Hz_Test_1['Time (s)'], Gear_No_Slug_150_C_40_Hz_Test_1['Gear Inside TC (C)'], lw=1.5, ls='--', color='r', label='Test 1')
plot(Gear_No_Slug_150_C_40_Hz_Test_2['Time (s)'], Gear_No_Slug_150_C_40_Hz_Test_2['Gear Inside TC (C)'], lw=1.5, ls='--', color='g', label='Test 2')
plot(Gear_No_Slug_150_C_40_Hz_Test_3['Time (s)'], Gear_No_Slug_150_C_40_Hz_Test_3['Gear Inside TC (C)'], lw=1.5, ls='--', color='b', label='Test 3')
grid(True)
xlabel('Time', fontsize=20)
ylabel('Temperature ($^\circ$C)', fontsize=20)
xticks(fontsize=16)
yticks(fontsize=16)
ylim([0, 160])
legend(loc='upper right')
savefig('../Figures/Gear_No_Slug_Temperature_150_C_40_Hz.pdf')

fig = figure()
plot(Gear_No_Slug_150_C_60_Hz_Test_1['Time (s)'], Gear_No_Slug_150_C_60_Hz_Test_1['Gear Outside TC (C)'], lw=1.5, ls='-', color='r', label='Test 1')
plot(Gear_No_Slug_150_C_60_Hz_Test_2['Time (s)'], Gear_No_Slug_150_C_60_Hz_Test_2['Gear Outside TC (C)'], lw=1.5, ls='-', color='g', label='Test 2')
plot(Gear_No_Slug_150_C_60_Hz_Test_3['Time (s)'], Gear_No_Slug_150_C_60_Hz_Test_3['Gear Outside TC (C)'], lw=1.5, ls='-', color='b', label='Test 3')
plot(Gear_No_Slug_150_C_60_Hz_Test_1['Time (s)'], Gear_No_Slug_150_C_60_Hz_Test_1['Gear Inside TC (C)'], lw=1.5, ls='--', color='r', label='Test 1')
plot(Gear_No_Slug_150_C_60_Hz_Test_2['Time (s)'], Gear_No_Slug_150_C_60_Hz_Test_2['Gear Inside TC (C)'], lw=1.5, ls='--', color='g', label='Test 2')
plot(Gear_No_Slug_150_C_60_Hz_Test_3['Time (s)'], Gear_No_Slug_150_C_60_Hz_Test_3['Gear Inside TC (C)'], lw=1.5, ls='--', color='b', label='Test 3')
grid(True)
xlabel('Time', fontsize=20)
ylabel('Temperature ($^\circ$C)', fontsize=20)
xticks(fontsize=16)
yticks(fontsize=16)
ylim([0, 160])
legend(loc='upper right')
savefig('../Figures/Gear_No_Slug_Temperature_150_C_60_Hz.pdf')

####################################################################################################################################
####################################################################################################################################
####################################################################################################################################
fig = figure()
plot(Gear_With_Slug_50_C_40_Hz_Test_1['Time (s)'], Gear_With_Slug_50_C_40_Hz_Test_1['Gear Outside TC (C)'], lw=1.5, ls='-', color='r', label='Test 1')
plot(Gear_With_Slug_50_C_40_Hz_Test_2['Time (s)'], Gear_With_Slug_50_C_40_Hz_Test_2['Gear Outside TC (C)'], lw=1.5, ls='-', color='g', label='Test 2')
plot(Gear_With_Slug_50_C_40_Hz_Test_3['Time (s)'], Gear_With_Slug_50_C_40_Hz_Test_3['Gear Outside TC (C)'], lw=1.5, ls='-', color='b', label='Test 3')
plot(Gear_With_Slug_50_C_40_Hz_Test_1['Time (s)'], Gear_With_Slug_50_C_40_Hz_Test_1['Gear Inside TC (C)'], lw=1.5, ls='--', color='r', label='Test 1')
plot(Gear_With_Slug_50_C_40_Hz_Test_2['Time (s)'], Gear_With_Slug_50_C_40_Hz_Test_2['Gear Inside TC (C)'], lw=1.5, ls='--', color='g', label='Test 2')
plot(Gear_With_Slug_50_C_40_Hz_Test_3['Time (s)'], Gear_With_Slug_50_C_40_Hz_Test_3['Gear Inside TC (C)'], lw=1.5, ls='--', color='b', label='Test 3')
grid(True)
xlabel('Time', fontsize=20)
ylabel('Temperature ($^\circ$C)', fontsize=20)
xticks(fontsize=16)
yticks(fontsize=16)
ylim([0, 160])
legend(loc='upper right')
savefig('../Figures/Gear_With_Slug_Temperature_50_C_40_Hz.pdf')

fig = figure()
plot(Gear_With_Slug_50_C_60_Hz_Test_1['Time (s)'], Gear_With_Slug_50_C_60_Hz_Test_1['Gear Outside TC (C)'], lw=1.5, ls='-', color='r', label='Test 1')
plot(Gear_With_Slug_50_C_60_Hz_Test_2['Time (s)'], Gear_With_Slug_50_C_60_Hz_Test_2['Gear Outside TC (C)'], lw=1.5, ls='-', color='g', label='Test 2')
plot(Gear_With_Slug_50_C_60_Hz_Test_3['Time (s)'], Gear_With_Slug_50_C_60_Hz_Test_3['Gear Outside TC (C)'], lw=1.5, ls='-', color='b', label='Test 3')
plot(Gear_With_Slug_50_C_60_Hz_Test_1['Time (s)'], Gear_With_Slug_50_C_60_Hz_Test_1['Gear Inside TC (C)'], lw=1.5, ls='--', color='r', label='Test 1')
plot(Gear_With_Slug_50_C_60_Hz_Test_2['Time (s)'], Gear_With_Slug_50_C_60_Hz_Test_2['Gear Inside TC (C)'], lw=1.5, ls='--', color='g', label='Test 2')
plot(Gear_With_Slug_50_C_60_Hz_Test_3['Time (s)'], Gear_With_Slug_50_C_60_Hz_Test_3['Gear Inside TC (C)'], lw=1.5, ls='--', color='b', label='Test 3')
grid(True)
xlabel('Time', fontsize=20)
ylabel('Temperature ($^\circ$C)', fontsize=20)
xticks(fontsize=16)
yticks(fontsize=16)
ylim([0, 160])
legend(loc='upper right')
savefig('../Figures/Gear_With_Slug_Temperature_50_C_60_Hz.pdf')

fig = figure()
plot(Gear_With_Slug_100_C_40_Hz_Test_1['Time (s)'], Gear_With_Slug_100_C_40_Hz_Test_1['Gear Outside TC (C)'], lw=1.5, ls='-', color='r', label='Test 1')
plot(Gear_With_Slug_100_C_40_Hz_Test_2['Time (s)'], Gear_With_Slug_100_C_40_Hz_Test_2['Gear Outside TC (C)'], lw=1.5, ls='-', color='g', label='Test 2')
plot(Gear_With_Slug_100_C_40_Hz_Test_3['Time (s)'], Gear_With_Slug_100_C_40_Hz_Test_3['Gear Outside TC (C)'], lw=1.5, ls='-', color='b', label='Test 3')
plot(Gear_With_Slug_100_C_40_Hz_Test_1['Time (s)'], Gear_With_Slug_100_C_40_Hz_Test_1['Gear Inside TC (C)'], lw=1.5, ls='--', color='r', label='Test 1')
plot(Gear_With_Slug_100_C_40_Hz_Test_2['Time (s)'], Gear_With_Slug_100_C_40_Hz_Test_2['Gear Inside TC (C)'], lw=1.5, ls='--', color='g', label='Test 2')
plot(Gear_With_Slug_100_C_40_Hz_Test_3['Time (s)'], Gear_With_Slug_100_C_40_Hz_Test_3['Gear Inside TC (C)'], lw=1.5, ls='--', color='b', label='Test 3')
grid(True)
xlabel('Time', fontsize=20)
ylabel('Temperature ($^\circ$C)', fontsize=20)
xticks(fontsize=16)
yticks(fontsize=16)
ylim([0, 160])
legend(loc='upper right')
savefig('../Figures/Gear_With_Slug_Temperature_100_C_40_Hz.pdf')

fig = figure()
plot(Gear_With_Slug_100_C_60_Hz_Test_1['Time (s)'], Gear_With_Slug_100_C_60_Hz_Test_1['Gear Outside TC (C)'], lw=1.5, ls='-', color='r', label='Test 1')
plot(Gear_With_Slug_100_C_60_Hz_Test_2['Time (s)'], Gear_With_Slug_100_C_60_Hz_Test_2['Gear Outside TC (C)'], lw=1.5, ls='-', color='g', label='Test 2')
plot(Gear_With_Slug_100_C_60_Hz_Test_3['Time (s)'], Gear_With_Slug_100_C_60_Hz_Test_3['Gear Outside TC (C)'], lw=1.5, ls='-', color='b', label='Test 3')
plot(Gear_With_Slug_100_C_60_Hz_Test_1['Time (s)'], Gear_With_Slug_100_C_60_Hz_Test_1['Gear Inside TC (C)'], lw=1.5, ls='--', color='r', label='Test 1')
plot(Gear_With_Slug_100_C_60_Hz_Test_2['Time (s)'], Gear_With_Slug_100_C_60_Hz_Test_2['Gear Inside TC (C)'], lw=1.5, ls='--', color='g', label='Test 2')
plot(Gear_With_Slug_100_C_60_Hz_Test_3['Time (s)'], Gear_With_Slug_100_C_60_Hz_Test_3['Gear Inside TC (C)'], lw=1.5, ls='--', color='b', label='Test 3')
grid(True)
xlabel('Time', fontsize=20)
ylabel('Temperature ($^\circ$C)', fontsize=20)
xticks(fontsize=16)
yticks(fontsize=16)
ylim([0, 160])
legend(loc='upper right')
savefig('../Figures/Gear_With_Slug_Temperature_100_C_60_Hz.pdf')

fig = figure()
plot(Gear_With_Slug_150_C_40_Hz_Test_1['Time (s)'], Gear_With_Slug_150_C_40_Hz_Test_1['Gear Outside TC (C)'], lw=1.5, ls='-', color='r', label='Test 1')
plot(Gear_With_Slug_150_C_40_Hz_Test_2['Time (s)'], Gear_With_Slug_150_C_40_Hz_Test_2['Gear Outside TC (C)'], lw=1.5, ls='-', color='g', label='Test 2')
plot(Gear_With_Slug_150_C_40_Hz_Test_3['Time (s)'], Gear_With_Slug_150_C_40_Hz_Test_3['Gear Outside TC (C)'], lw=1.5, ls='-', color='b', label='Test 3')
plot(Gear_With_Slug_150_C_40_Hz_Test_1['Time (s)'], Gear_With_Slug_150_C_40_Hz_Test_1['Gear Inside TC (C)'], lw=1.5, ls='--', color='r', label='Test 1')
plot(Gear_With_Slug_150_C_40_Hz_Test_2['Time (s)'], Gear_With_Slug_150_C_40_Hz_Test_2['Gear Inside TC (C)'], lw=1.5, ls='--', color='g', label='Test 2')
plot(Gear_With_Slug_150_C_40_Hz_Test_3['Time (s)'], Gear_With_Slug_150_C_40_Hz_Test_3['Gear Inside TC (C)'], lw=1.5, ls='--', color='b', label='Test 3')
grid(True)
xlabel('Time', fontsize=20)
ylabel('Temperature ($^\circ$C)', fontsize=20)
xticks(fontsize=16)
yticks(fontsize=16)
ylim([0, 160])
legend(loc='upper right')
savefig('../Figures/Gear_With_Slug_Temperature_150_C_40_Hz.pdf')

fig = figure()
plot(Gear_With_Slug_150_C_60_Hz_Test_1['Time (s)'], Gear_With_Slug_150_C_60_Hz_Test_1['Gear Outside TC (C)'], lw=1.5, ls='-', color='r', label='Test 1')
plot(Gear_With_Slug_150_C_60_Hz_Test_2['Time (s)'], Gear_With_Slug_150_C_60_Hz_Test_2['Gear Outside TC (C)'], lw=1.5, ls='-', color='g', label='Test 2')
plot(Gear_With_Slug_150_C_60_Hz_Test_3['Time (s)'], Gear_With_Slug_150_C_60_Hz_Test_3['Gear Outside TC (C)'], lw=1.5, ls='-', color='b', label='Test 3')
plot(Gear_With_Slug_150_C_60_Hz_Test_1['Time (s)'], Gear_With_Slug_150_C_60_Hz_Test_1['Gear Inside TC (C)'], lw=1.5, ls='--', color='r', label='Test 1')
plot(Gear_With_Slug_150_C_60_Hz_Test_2['Time (s)'], Gear_With_Slug_150_C_60_Hz_Test_2['Gear Inside TC (C)'], lw=1.5, ls='--', color='g', label='Test 2')
plot(Gear_With_Slug_150_C_60_Hz_Test_3['Time (s)'], Gear_With_Slug_150_C_60_Hz_Test_3['Gear Inside TC (C)'], lw=1.5, ls='--', color='b', label='Test 3')
grid(True)
xlabel('Time', fontsize=20)
ylabel('Temperature ($^\circ$C)', fontsize=20)
xticks(fontsize=16)
yticks(fontsize=16)
ylim([0, 160])
legend(loc='upper right')
savefig('../Figures/Gear_With_Slug_Temperature_150_C_60_Hz.pdf')
