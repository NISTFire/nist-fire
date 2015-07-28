#!/usr/bin/env python

import os
import collections
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from itertools import cycle

from matplotlib import rcParams
rcParams.update({'figure.autolayout': True})

#  =================
#  = User Settings =
#  =================

# Location of experimental data files
data_dir = '../Experimental_Data/'

# Location of file with timing information
all_times_file = '../Experimental_Data/All_Times.csv'

# Location of scaling conversion files
scaling_file_west = '../DAQ_Files/West_DelCo_DAQ_Channel_List.csv'
scaling_file_east = '../DAQ_Files/East_DelCo_DAQ_Channel_List.csv'

# Location of test description file
info_file = '../Experimental_Data/Description_of_Experiments.csv'

# Location to save/output figures
save_dir = '../Figures/Script_Figures/'

# Time averaging window for data smoothing
data_time_averaging_window = 10

# Duration of pre-test time for bi-directional probes and heat flux gauges (s)
pre_test_time = 60

# Load exp. timings and description file
all_times = pd.read_csv(all_times_file)
all_times = all_times.set_index('Time')
info = pd.read_csv(info_file, index_col=3)

# List of sensor groups for each plot
sensor_groups = [['TC_A5_'],['TC_A6_'],['TC_A6_'],['BDP_A5_'],['BDP_A6_'],['BDP_A10_']]

#  =============================
#  = Property Lookup Functions =
#  =============================

def density (T):

	density_temp = [10,15,20,25,30,40,50,60,70,80,90,100,200,300,400,500,1000]
	density_value = [1.247,1.225,1.204,1.184,1.165,1.127,1.109,1.060,
				1.029,.9996,.9721,.9461,.7461,.6159,.5243,.4565,.2772]

	for i in range(0,len(density_temp)):
		if T < density_temp[i] and T > density_temp[i-1]:
			rho = density_value[i] - (density_value[i]-density_value[i-1])*(density_temp[i]-T)/(density_temp[i]-density_temp[i-1])
		else:
			continue
		i += 1

	return rho;

def heatCapacity (T):

	T_Kelvin = T + 274.15

	cp_temp = [250,300,350,400,450,500,550,600,650,700,750,800,900,1000,1100,1200,1300,1400,1500]
	cp_value = [1.003,1.005,1.008,1.013,1.020,1.029,1.040,1.051,1.063,
				1.075,1.087,1.099,1.121,1.142,1.155,1.173,1.190,1.204,1.216]


	for i in range(0,len(cp_temp)):
		if T_Kelvin < cp_temp[i] and T_Kelvin > cp_temp[i-1]:
			cp = cp_value[i] - (cp_value[i]-cp_value[i-1])*(cp_temp[i]-T_Kelvin)/(cp_temp[i]-cp_temp[i-1])
		else:
			continue
		i += 1

	return cp;

#  ===================
#  = HRR Calculation =
#  ===================

time = 490

data = pd.read_csv(data_dir + 'Test_46_West_71015_Reduced.csv')

groups2 = ['TC 5 ']

for group in groups2:
	

TC_A5_1 = data['TC 5 0.08 m BS West']
rho_A5_1 = np.zeros(len(TC_A5_1))
for i in range(0,len(TC_A5_1)):
	rho_A5_1[i] = density(TC_A5_1[i])


TC_A5 = [331.4311939,326.0074702,336.83139,317.6481487,300.2922252,274.4683349,201.8816151,124.7623352]
TC_A6 = [314.2820229,329.4394212,286.9078352,241.185635,207.0832675,173.6605126,136.6284685,101.0759911]
TC_A10 = [281.3507691,304.6334154,262.1768415,296.8416945,294.4427193,288.5982813,190.1521199,101.5997678]

rho_A5 = np.zeros(8)
rho_A6 = np.zeros(8)
rho_A10 = np.zeros(8)
cp_A5 = np.zeros(8)
cp_A6 = np.zeros(8)
cp_A10 = np.zeros(8)

groups = ['TC_A5','TC_A6','TC_A10']

for group in groups:
	for n in range(0,8):
		if 'TC_A5' in group:
			rho_A5[n] = density(TC_A5[n])
			cp_A5[n] = heatCapacity(TC_A5[n])
		elif 'TC_A6' in group:
			rho_A6[n] = density(TC_A6[n])
			cp_A6[n] = heatCapacity(TC_A6[n])
		else:
			rho_A10[n] = density(TC_A10[n])
			cp_A10[n] = heatCapacity(TC_A10[n])



print np.mean(rho_A10)
print np.mean(cp_A10)

