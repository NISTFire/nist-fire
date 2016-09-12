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
plume_channels = ['TC01','TC02','TC03','TC04','TC05','TC06','TC07','TC08','TC09','TC10','TC11']
plume_labels = ['0.2 m','0.4 m','0.6 m','0.8 m','1.0 m','1.2 m','1.4 m','1.6 m','1.8 m','2.0 m','2.2 m']

wall_channels = ['T01_Wall','T02_Wall','T03_Wall','T04_Wall','T05_Wall','T06_Wall','T07_Wall','T08_Wall','T09_Wall','T10_Wall','T11_Wall']
wall_labels = ['0.2 m','0.4 m','0.6 m','0.8 m','1.0 m','1.2 m','1.4 m','1.6 m','1.8 m','2.0 m','2.2 m']

hf_channels = ['GHF1_Wall_CL','GHF2_Wall_CL','GHF3_Wall_CL','GHF4_Wall_CL','GHF5_Wall_CL','GHF6_Wall_CL']
hf_labels = ['0.5 m','0.7 m','0.9 m','1.1 m','1.3 m','1.5 m']

hf_edge_channels = ['GHF1_Wall_R','GHF2_Wall_R','GHF3_Wall_R','GHF4_Wall_R','GHF5_Wall_R','GHF6_Wall_R']
hf_edge_labels = ['0.5 m','0.7 m','0.9 m','1.1 m','1.3 m','1.5 m']

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

distance = ['0D','p5D','1D','2D']

for j in range(0,len(distance)):
	data05 = pd.read_csv(data_dir + 'NG_80kW_GBWall_'+distance[j]+'_RI=05_devc.csv',header=1)
	data10 = pd.read_csv(data_dir + 'NG_80kW_GBWall_'+distance[j]+'_RI=10_devc.csv',header=1)
	data20 = pd.read_csv(data_dir + 'NG_80kW_GBWall_'+distance[j]+'_RI=20_devc.csv',header=1)

	temp_plume = [['RI=05'],['RI=10'],['RI=20']]
	for i in range(0,len(plume_channels)):
		y05 = np.mean(data05[plume_channels[i]][50:300])
		temp_plume[0].append(y05)
		y10 = np.mean(data10[plume_channels[i]][50:300])
		temp_plume[1].append(y10)
		y20 = np.mean(data20[plume_channels[i]][50:300])
		temp_plume[2].append(y20)
	temp_plume = pd.DataFrame(temp_plume)
	temp_plume = temp_plume.drop(temp_plume.columns[[0]],axis=1)
	temp_plume.columns = plume_labels
	temp_plume.to_csv('../FDS_Output_Files/plumetemp_avg_'+distance[j]+'.csv')

	temp_wall = [['RI=05'],['RI=10'],['RI=20']]
	for i in range(0,len(wall_channels)):
		y05 = np.mean(data05[wall_channels[i]][50:300])
		temp_wall[0].append(y05)
		y10 = np.mean(data10[wall_channels[i]][50:300])
		temp_wall[1].append(y10)
		y20 = np.mean(data20[wall_channels[i]][50:300])
		temp_wall[2].append(y20)
	temp_wall = pd.DataFrame(temp_wall)
	temp_wall = temp_wall.drop(temp_wall.columns[[0]],axis=1)
	temp_wall.columns = plume_labels
	temp_wall.to_csv('../FDS_Output_Files/walltemp_avg_'+distance[j]+'.csv')

	temp_hf_wall = [['RI=05'],['RI=10'],['RI=20']]
	for i in range(0,len(hf_channels)):
		y05 = np.mean(data05[hf_channels[i]][50:300])
		temp_hf_wall[0].append(y05)
		y10 = np.mean(data10[hf_channels[i]][50:300])
		temp_hf_wall[1].append(y10)
		y20 = np.mean(data20[hf_channels[i]][50:300])
		temp_hf_wall[2].append(y20)
	temp_hf_wall = pd.DataFrame(temp_hf_wall)
	temp_hf_wall = temp_hf_wall.drop(temp_hf_wall.columns[[0]],axis=1)
	temp_hf_wall.columns = hf_labels
	temp_hf_wall.to_csv('../FDS_Output_Files/hfwallcl_avg_'+distance[j]+'.csv')

	temp_hf_wall_edge = [['RI=05'],['RI=10'],['RI=20']]
	for i in range(0,len(hf_edge_channels)):
		y05 = np.mean(data05[hf_edge_channels[i]][50:300])
		temp_hf_wall_edge[0].append(y05)
		y10 = np.mean(data10[hf_edge_channels[i]][50:300])
		temp_hf_wall_edge[1].append(y10)
		y20 = np.mean(data20[hf_edge_channels[i]][50:300])
		temp_hf_wall_edge[2].append(y20)
	temp_hf_wall_edge = pd.DataFrame(temp_hf_wall_edge)
	temp_hf_wall_edge = temp_hf_wall_edge.drop(temp_hf_wall_edge.columns[[0]],axis=1)
	temp_hf_wall_edge.columns = hf_edge_labels
	temp_hf_wall_edge.to_csv('../FDS_Output_Files/hfwalledge_avg_'+distance[j]+'.csv')