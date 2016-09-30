# to run - ctrl + b
#these first lines are standard calls for including desired packages for data and plotting
from __future__ import division
import numpy as np
import pandas as pd
from pylab import *
import matplotlib.pyplot as plt
from itertools import cycle

#read in data file(s) -- point to relative path in repository
#if more than one line of headers at top of document add header=n-1
#typically one header line, header = 1-1 -> header=0 which is default
data = pd.read_csv('../Experimental_Data/TWGas/NCTW_GAS_HF_Center_Avg.csv', header=0)
#fds = pd.read_csv('../FDS_Output_Data/testname.csv', header=1)

marker_style =['s', '*', '^', 'o', '<', '>', '8', 'h','d','x','p','v','H', 'D', '1', '2', '3', '4', '|','s']
tableau20 = [(31, 119, 180), (174, 199, 232), (255, 127, 14), (255, 187, 120),
             (44, 160, 44), (152, 223, 138), (214, 39, 40), (255, 152, 150),
             (148, 103, 189), (197, 176, 213), (140, 86, 75), (196, 156, 148),
             (227, 119, 194), (247, 182, 210), (127, 127, 127), (199, 199, 199),
             (188, 189, 34), (219, 219, 141), (23, 190, 207), (158, 218, 229)]
for i in range(len(tableau20)):
    r, g, b = tableau20[i]
    tableau20[i] = (r / 255., g / 255., b / 255.)

#plotting
fig = figure()
#here data['Position'] is calling for the column named Position in data file which is x data
#data[0,2 m] is the y data
plt.rcParams['axes.prop_cycle'] = (cycler('color',tableau20)+cycler('marker',marker_style))
plt.plot(data['Position'],data['0.2 m'], label='0.2 m Above Burner',ms=8)
plt.plot(data['Position'],data['0.4 m'], label='0.4 m Above Burner',ms=8)
plt.plot(data['Position'],data['0.6 m'], label='0.6 m Above Burner',ms=8)
plt.plot(data['Position'],data['0.8 m'], label='0.8 m Above Burner',ms=8)
plt.plot(data['Position'],data['1.0 m'], label='1.0 m Above Burner',ms=8)
plt.plot(data['Position'],data['1.2 m'], label='1.2 m Above Burner',ms=8)
ax1 = gca()
xlabel('Distance from Wall (m)', fontsize=20)
ylabel('Heat Flux (kW/m$^2$)', fontsize=20)
xticks(fontsize=16)
yticks(fontsize=16)
grid(True)
ax = gca()
axis([0, 0.7, 0, 75])
legend(numpoints=1,loc='upper right',fontsize=16 )
#point figures to be written in Figures directory and desired file name
savefig('../Figures/test_heatflux.pdf',format='pdf')
close()