from __future__ import division

import os
import numpy as np
import numpy.ma as ma
import pandas as pd
from pylab import *
import math
import string

from matplotlib import rcParams
rcParams.update({'figure.autolayout': True})

# Location of files
data_dir = '../FDS_Output_Files/'
plot_dir = '../Figures/'

# List of sensor groups for each plot
plume_channels = ['TC01','TC02','TC03','TC04','TC05','TC06','TC07','TC08','TC09','TC10','TC11','TC12']
plume_labels = ['0.2 m','0.4 m','0.6 m','0.8 m','1.0 m','1.2 m','1.4 m','1.6 m','1.8 m','2.0 m','2.2 m','2.4 m']


#number of TCs in array
num_array = 12

markers = ['s', '*', '^', 'o', '<', '>', '8', 'h','d','x','p','v','H', 'D', '1', '2', '3', '4', '|']
colors = [(31, 119, 180), (174, 199, 232), (255, 127, 14), (255, 187, 120),
             (44, 160, 44), (152, 223, 138), (214, 39, 40), (255, 152, 150),
             (148, 103, 189), (197, 176, 213), (140, 86, 75), (196, 156, 148),
             (227, 119, 194), (247, 182, 210), (127, 127, 127), (199, 199, 199),
             (188, 189, 34), (219, 219, 141), (23, 190, 207), (158, 218, 229)]

# Scale the RGB values to the [0, 1] range, which is the format matplotlib accepts.
for i in range(len(colors)):
    r, g, b = colors[i]
    colors[i] = (r / 255., g / 255., b / 255.)

#  =========================
#  = Reading in Data Files =
#  =========================

data05 = pd.read_csv(data_dir + 'NG_80kW_GBWall_2D_RI=05_devc.csv',header=1)
data10 = pd.read_csv(data_dir + 'NG_80kW_GBWall_2D_RI=10_devc.csv',header=1)
data20 = pd.read_csv(data_dir + 'NG_80kW_GBWall_2D_RI=20_devc.csv',header=1)


fig = figure()
for i in range(2,3):
	y05 = data05[plume_channels[i]]
	y10 = data10[plume_channels[i]]
	y20 = data20[plume_channels[i]]
	plot(data05['Time'],y05,color=colors[i],marker=markers[i],markevery=25,ms=8,linewidth=2,label='FDS RI=05 '+plume_labels[i])
	plot(data10['Time'],y10,color=colors[i],marker=markers[i+1],markevery=25,ms=8,linewidth=2,ls='--',label='FDS RI=10 '+plume_labels[i])
	plot(data20['Time'],y20,color=colors[i],marker=markers[i+2],markevery=25,ms=8,linewidth=2,ls='-.',label='FDS RI=20 '+plume_labels[i])

ax1 = gca()
xlabel('Time (s)', fontsize=20)
ylabel('Temperature ($^{\circ}$C)', fontsize=20)
xticks(fontsize=16)
yticks(fontsize=16)
legend(numpoints=1,loc=1,ncol=1,fontsize=16)
legend(bbox_to_anchor=(1.03,1.04))
axis([0, 300, 0, 1000])
grid(True)
savefig(plot_dir + 'FDS_TC_Plume_RIComp.pdf',format='pdf')
close()