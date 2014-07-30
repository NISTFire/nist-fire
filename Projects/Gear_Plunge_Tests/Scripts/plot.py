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

data_50_C_40_Hz = pd.read_csv(data_dir + 'test1.csv')
data_50_C_40_Hz_w_Slug = pd.read_csv(data_dir + 'test2.csv')

#  ============
#  = Plotting =
#  ============

fig = figure()

plot(data_50_C_40_Hz['Time'], data_50_C_40_Hz['Temp1'], lw=1.5, label='Test 1')
plot(data_50_C_40_Hz_w_Slug['Time'], data_50_C_40_Hz_w_Slug['Temp2'], lw=1.5, label='Test 2')

grid(True)
xlabel('Time', fontsize=20)
ylabel('Temperature ($^\circ$C)', fontsize=20)
xticks(fontsize=16)
yticks(fontsize=16)
legend(loc='lower right')
savefig('../Figures/Temperature_50_C_40_Hz.pdf')
