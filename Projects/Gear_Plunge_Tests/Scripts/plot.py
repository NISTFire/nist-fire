#!/usr/bin/env python

from __future__ import division

import itertools
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

#  =================
#  = User settings =
#  =================

data_dir = '../Experimental_Data/'

#  ========================
#  = Plot slug only tests =
#  ========================

conditions = ['50_C_40_Hz', '50_C_60_Hz', '100_C_40_Hz', '100_C_60_Hz', '150_C_40_Hz', '150_C_60_Hz']

for condition in conditions:
    data = pd.read_csv(data_dir + 'Slug_Only/' + condition + '.csv')

    fig = figure()
    plot(data['Time (s)'], data['Outside TC (C)'], lw=1.5, ls='-', color='r', label='Outside TC')
    plot(data['Time (s)'], data['Surface TC (C)'], lw=1.5, ls='--', color='g', label='Surface TC')
    plot(data['Time (s)'], data['Slug TC (C)'], lw=1.5, ls='-.', color='b', label='Slug TC')
    grid(True)
    xlabel('Time', fontsize=20)
    ylabel('Temperature ($^\circ$C)', fontsize=20)
    xticks(fontsize=16)
    yticks(fontsize=16)
    ylim([0, 160])
    legend(loc='upper right')
    savefig('../Figures/Slug_Only_Temperature_' + condition + '.pdf')

    close('all')

#  ================================
#  = Plot gear tests without slug =
#  ================================

conditions = ['50_C_40_Hz', '50_C_60_Hz', '100_C_40_Hz', '100_C_60_Hz', '150_C_40_Hz', '150_C_60_Hz']
data = {}

for condition in conditions:
    data[condition + '_Test_1'] = pd.read_csv(data_dir + 'Gear_No_Slug/' + condition + '_Test_1.csv')
    data[condition + '_Test_2'] = pd.read_csv(data_dir + 'Gear_No_Slug/' + condition + '_Test_2.csv')
    data[condition + '_Test_3'] = pd.read_csv(data_dir + 'Gear_No_Slug/' + condition + '_Test_3.csv')

    fig = figure()
    plot(np.arange(301), data[condition + '_Test_1']['Gear Outside TC (C)'], lw=1.5, ls='-', color='r', label='Test 1')
    plot(np.arange(301), data[condition + '_Test_2']['Gear Outside TC (C)'], lw=1.5, ls='-', color='g', label='Test 2')
    plot(np.arange(301), data[condition + '_Test_3']['Gear Outside TC (C)'], lw=1.5, ls='-', color='b', label='Test 3')
    plot(np.arange(301), data[condition + '_Test_1']['Gear Inside TC (C)'], lw=1.5, ls='--', color='r', label='Test 1')
    plot(np.arange(301), data[condition + '_Test_2']['Gear Inside TC (C)'], lw=1.5, ls='--', color='g', label='Test 2')
    plot(np.arange(301), data[condition + '_Test_3']['Gear Inside TC (C)'], lw=1.5, ls='--', color='b', label='Test 3')
    grid(True)
    xlabel('Time', fontsize=20)
    ylabel('Temperature ($^\circ$C)', fontsize=20)
    xticks(fontsize=16)
    yticks(fontsize=16)
    ylim([0, 200])
    legend(loc='upper right')
    savefig('../Figures/Gear_No_Slug_Temperature_' + condition + '_All.pdf')

    data[condition + '_Outside_Average'] = np.mean([data[condition + '_Test_1']['Gear Outside TC (C)'],
                                                   data[condition + '_Test_2']['Gear Outside TC (C)'],
                                                   data[condition + '_Test_3']['Gear Outside TC (C)']], axis=0)
    
    data[condition + '_Outside_Std'] = np.std([data[condition + '_Test_1']['Gear Outside TC (C)'],
                                              data[condition + '_Test_2']['Gear Outside TC (C)'],
                                              data[condition + '_Test_3']['Gear Outside TC (C)']], axis=0)
    
    data[condition + '_Inside_Average'] = np.mean([data[condition + '_Test_1']['Gear Inside TC (C)'],
                                                  data[condition + '_Test_2']['Gear Inside TC (C)'],
                                                  data[condition + '_Test_3']['Gear Inside TC (C)']], axis=0)
    
    data[condition + '_Inside_Std'] = np.std([data[condition + '_Test_1']['Gear Inside TC (C)'],
                                             data[condition + '_Test_2']['Gear Inside TC (C)'],
                                             data[condition + '_Test_3']['Gear Inside TC (C)']], axis=0)

    fig = figure()
    errorbar(np.arange(301), data[condition + '_Outside_Average'], yerr=data[condition + '_Outside_Std'],
             errorevery=10, ecolor='0.8', lw=1.5, ls='-', color='r', label='Gear Outside')
    errorbar(np.arange(301), data[condition + '_Inside_Average'], yerr=data[condition + '_Inside_Std'],
             errorevery=10, ecolor='0.8', lw=1.5, ls='--', color='r', label='Gear Inside')
    grid(True)
    xlabel('Time', fontsize=20)
    ylabel('Temperature ($^\circ$C)', fontsize=20)
    xticks(fontsize=16)
    yticks(fontsize=16)
    ylim([0, 200])
    legend(loc='upper right')
    savefig('../Figures/Gear_No_Slug_Temperature_' + condition + '_Average.pdf')

    data[condition + '_Outside_Average_Diff'] = np.diff(smooth(data[condition + '_Outside_Average'], 10))
    data[condition + '_Inside_Average_Diff'] = np.diff(smooth(data[condition + '_Inside_Average'], 10))

    fig = figure()
    plot(np.arange(309), data[condition + '_Inside_Average_Diff'], lw=1.5, ls='--', color='r', label='Gear Inside')
    grid(True)
    xlabel('Time', fontsize=20)
    ylabel('Temperature ($^\circ$C)', fontsize=20)
    xticks(fontsize=16)
    yticks(fontsize=16)
    ylim([0, 1.2])
    legend(loc='upper right')
    savefig('../Figures/Gear_No_Slug_Temperature_' + condition + '_Diff.pdf')

    close('all')

# Heat transfer model
t = np.arange(300)
A = 0.01 # m^2
m = 0.05 # kg
c = 1 # kJ/kg-K
### q = h * A * (T_gas - T) = m * c * dT/dt
# h = 11 # W/m^2-K
# h = 13 # W/m^2-K
# tau = m*c/h*A

T_i_1 = 25; tau_1 = 65; T_gas_1 = 40.5; offset_1 = 10
T_i_2 = 26; tau_2 = 60; T_gas_2 = 41; offset_2 = 7
T_i_3 = 27; tau_3 = 70; T_gas_3 = 74; offset_3 = 10
T_i_4 = 27; tau_4 = 65; T_gas_4 = 70; offset_4 = 10
T_i_5 = 30; tau_5 = 68; T_gas_5 = 115; offset_5 = 10
T_i_6 = 30; tau_6 = 55; T_gas_6 = 113; offset_6 = 10

T_1 = T_gas_1 - (T_gas_1 - T_i_1) * np.exp(-t/tau_1)
T_2 = T_gas_2 - (T_gas_2 - T_i_2) * np.exp(-t/tau_2)
T_3 = T_gas_3 - (T_gas_3 - T_i_3) * np.exp(-t/tau_3)
T_4 = T_gas_4 - (T_gas_4 - T_i_4) * np.exp(-t/tau_4)
T_5 = T_gas_5 - (T_gas_5 - T_i_5) * np.exp(-t/tau_5)
T_6 = T_gas_6 - (T_gas_6 - T_i_6) * np.exp(-t/tau_6)

fig = figure()
plot(t+offset_1, T_1, lw=1.5, ls='--', color='r')
plot(t+offset_2, T_2, lw=1.5, ls='--', color='g')
plot(t+offset_3, T_3, lw=1.5, ls='--', color='b')
plot(t+offset_4, T_4, lw=1.5, ls='--', color='c')
plot(t+offset_5, T_5, lw=1.5, ls='--', color='m')
plot(t+offset_6, T_6, lw=1.5, ls='--', color='k')
plot(np.arange(301), data['50_C_40_Hz_Inside_Average'], lw=1.5, ls='-', color='r', label='50 $^\circ$C at 2 m/s')
plot(np.arange(301), data['50_C_60_Hz_Inside_Average'], lw=1.5, ls='-', color='g', label='50 $^\circ$C at 3 m/s')
plot(np.arange(301), data['100_C_40_Hz_Inside_Average'], lw=1.5, ls='-', color='b', label='100 $^\circ$C at 2 m/s')
plot(np.arange(301), data['100_C_60_Hz_Inside_Average'], lw=1.5, ls='-', color='c', label='100 $^\circ$C at 3 m/s')
plot(np.arange(301), data['150_C_40_Hz_Inside_Average'], lw=1.5, ls='-', color='m', label='150 $^\circ$C at 2 m/s')
plot(np.arange(301), data['150_C_60_Hz_Inside_Average'], lw=1.5, ls='-', color='k', label='150 $^\circ$C at 3 m/s')
grid(True)
xlabel('Time', fontsize=20)
ylabel('Temperature ($^\circ$C)', fontsize=20)
xticks(fontsize=16)
yticks(fontsize=16)
xlim([0, 300])
ylim([0, 200])
legend(loc='upper left')
savefig('../Figures/Gear_No_Slug_Inside_Temperature_Average_Comparison.pdf')

fig = figure()
plot(np.arange(309), data['50_C_40_Hz_Inside_Average_Diff'], lw=1.5, ls='-', color='r', label='50 $^\circ$C at 2 m/s')
plot(np.arange(309), data['50_C_60_Hz_Inside_Average_Diff'], lw=1.5, ls='-', color='g', label='50 $^\circ$C at 3 m/s')
plot(np.arange(309), data['100_C_40_Hz_Inside_Average_Diff'], lw=1.5, ls='-', color='b', label='100 $^\circ$C at 2 m/s')
plot(np.arange(309), data['100_C_60_Hz_Inside_Average_Diff'], lw=1.5, ls='-', color='c', label='100 $^\circ$C at 3 m/s')
plot(np.arange(309), data['150_C_40_Hz_Inside_Average_Diff'], lw=1.5, ls='-', color='m', label='150 $^\circ$C at 2 m/s')
plot(np.arange(309), data['150_C_60_Hz_Inside_Average_Diff'], lw=1.5, ls='-', color='k', label='150 $^\circ$C at 3 m/s')
grid(True)
xlabel('Time', fontsize=20)
ylabel('Temperature ($^\circ$C)', fontsize=20)
xticks(fontsize=16)
yticks(fontsize=16)
ylim([0, 1.2])
legend(loc='upper right')
savefig('../Figures/Gear_No_Slug_Inside_Temperature_Diff_Comparison.pdf')

#  =============================
#  = Plot gear tests with slug =
#  =============================

conditions = ['50_C_40_Hz', '50_C_60_Hz', '100_C_40_Hz', '100_C_60_Hz', '150_C_40_Hz', '150_C_60_Hz']

for condition in conditions:
    data1 = pd.read_csv(data_dir + 'Gear_With_Slug/' + condition + '_Test_1.csv')
    data2 = pd.read_csv(data_dir + 'Gear_With_Slug/' + condition + '_Test_2.csv')
    data3 = pd.read_csv(data_dir + 'Gear_With_Slug/' + condition + '_Test_3.csv')

    fig = figure()
    plot(data1['Time (s)'], data1['Gear Outside TC (C)'], lw=1.5, ls='-', color='r', label='Test 1')
    plot(data2['Time (s)'], data2['Gear Outside TC (C)'], lw=1.5, ls='-', color='g', label='Test 2')
    plot(data3['Time (s)'], data3['Gear Outside TC (C)'], lw=1.5, ls='-', color='b', label='Test 3')
    plot(data1['Time (s)'], data1['Gear Inside TC (C)'], lw=1.5, ls='--', color='r', label='Test 1')
    plot(data2['Time (s)'], data2['Gear Inside TC (C)'], lw=1.5, ls='--', color='g', label='Test 2')
    plot(data3['Time (s)'], data3['Gear Inside TC (C)'], lw=1.5, ls='--', color='b', label='Test 3')
    plot(data1['Time (s)'], data1['Gear Slug TC (C)'], lw=1.5, ls='-.', color='r', label='Test 1')
    plot(data2['Time (s)'], data2['Gear Slug TC (C)'], lw=1.5, ls='-.', color='g', label='Test 2')
    plot(data3['Time (s)'], data3['Gear Slug TC (C)'], lw=1.5, ls='-.', color='b', label='Test 3')
    grid(True)
    xlabel('Time', fontsize=20)
    ylabel('Temperature ($^\circ$C)', fontsize=20)
    xticks(fontsize=16)
    yticks(fontsize=16)
    ylim([0, 160])
    legend(loc='upper right')
    savefig('../Figures/Gear_With_Slug_Temperature_' + condition + '.pdf')

    close('all')
