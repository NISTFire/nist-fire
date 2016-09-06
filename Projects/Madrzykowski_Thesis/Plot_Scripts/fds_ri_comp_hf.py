from __future__ import division

import os
import numpy as np
import numpy.ma as ma
import pandas as pd
from pylab import *
import math
import string

from matplotlib import rcParams
# rcParams.update({'figure.autolayout': True})

# Location of files
data_dir = '../FDS_Output_Files/'
plot_dir = '../Figures/'

# List of sensor groups for each plot
hf_channels = ['GHF1_Wall_CL','GHF2_Wall_CL','GHF3_Wall_CL','GHF4_Wall_CL','GHF5_Wall_CL','GHF6_Wall_CL']
hf_channels2 = ['GHF1_Wall_R','GHF2_Wall_R','GHF3_Wall_R','GHF4_Wall_R','GHF5_Wall_R','GHF6_Wall_R']
hf_labels = ['0.5 m','0.7 m','0.9 m','1.1 m','1.3 m','1.5 m']


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

data05 = pd.read_csv(data_dir + 'NG_80kW_GBWall_0D_RI=05_devc.csv',header=1)
# data10 = pd.read_csv(data_dir + 'NG_80kW_GBWall_0D_RI=10_devc.csv',header=1)
data20 = pd.read_csv(data_dir + 'NG_80kW_GBWall_0D_RI=20_devc.csv',header=1)


fig = figure()
for i in range(0,len(hf_channels)):
	y05 = data05[hf_channels[i]]
	print(hf_channels[i],np.mean(y05[50:300]))
	# y10 = data10[hf_channels[i]]
	# print(hf_channels[i],np.mean(y10[50:300]))
	y20 = data20[hf_channels[i]]
	print(hf_channels[i],np.mean(y20[50:300]))
	plot(data05['Time'],y05,color=colors[i],marker=markers[i],markevery=25,ms=8,linewidth=2,label='RI=05 '+hf_labels[i])
	# plot(data10['Time'],y10,color=colors[i],marker=markers[i+1],markevery=25,ms=8,linewidth=2,ls='--',label='RI=10 '+hf_labels[i])
	plot(data20['Time'],y20,color=colors[i],marker=markers[i+2],markevery=25,ms=8,linewidth=2,ls='-.',label='RI=20 '+hf_labels[i])
ax1 = gca()
xlabel('Time (s)', fontsize=20)
ylabel('Heat Flux (kW/m$^2$)', fontsize=20)
xticks(fontsize=16)
yticks(fontsize=16)
box = ax1.get_position()
ax1.set_position([box.x0, box.y0, box.width * 0.78, box.height])
ax1.legend(bbox_to_anchor=(1.44, 1.04))
axis([0, 300, 0, 25])
grid(True)
savefig(plot_dir + 'FDS_HF_Centerline_RIComp_p5D.pdf',format='pdf')
close()