from __future__ import division

import os
import numpy as np
import numpy.ma as ma
import pandas as pd
from pylab import *
import math
import string
from itertools import cycle
import matplotlib.pyplot as plt

#from matplotlib import rcParams
#rcParams.update({'figure.autolayout': True})

# Location of files
data_dir = '../Experimental_Data/Coats/'
plot_dir = '../Figures/Coats/'

# Location of test description file
info_file = '../Experimental_Data/Coats/Description_of_Experiments.csv'
info = pd.read_csv(info_file)

# Files to skip
skip_files = ['description_']

#  =========================
#  = Reading in Data Files =
#  =========================

coat_number = ['1561','1562','1563','2778']

for i in range(0,4):

	# Load exp. data file
	data1 = pd.read_csv(data_dir + 'tog_' + coat_number[i] + '_01p5.csv')
	data2 = pd.read_csv(data_dir + 'tog_' + coat_number[i] + '_02.csv')
	data3 = pd.read_csv(data_dir + 'tog_' + coat_number[i] + '_03.csv')
	data4 = pd.read_csv(data_dir + 'tog_' + coat_number[i] + '_05.csv')
	data5 = pd.read_csv(data_dir + 'tog_' + coat_number[i] + '_10.csv')

	# set time lengths
	time1 = np.arange(len(data1['TC_3']))
	time2 = np.arange(len(data2['TC_3']))
	time3 = np.arange(len(data3['TC_3']))
	time4 = np.arange(len(data4['TC_3']))
	time5 = np.arange(len(data5['TC_3']))
	time_offset = 60


	# set color scheme
	tableau20 = [(31, 119, 180), (174, 199, 232), (255, 127, 14), (255, 187, 120),
	             (44, 160, 44), (152, 223, 138), (214, 39, 40), (255, 152, 150),
	             (148, 103, 189), (197, 176, 213), (140, 86, 75), (196, 156, 148),
	             (227, 119, 194), (247, 182, 210), (127, 127, 127), (199, 199, 199),
	             (188, 189, 34), (219, 219, 141), (23, 190, 207), (158, 218, 229)]

	for j in range(len(tableau20)):
	    r, g, b = tableau20[j]
	    tableau20[j] = (r / 255., g / 255., b / 255.)
	plt.rc('axes', color_cycle=tableau20)
	plot_markers = cycle(['s', 'o', '^', 'd', 'h', 'p','v','8','D','*','<','>','H'])

	fig = plt.figure()
	ax = plt.subplot(111)
	ax.plot(time1,data1['TC_3'],marker=next(plot_markers),markevery=50,ms=8,label='1.5 kW/m$^2$')
	ax.plot(time2,data2['TC_3'],marker=next(plot_markers),markevery=50,ms=8,label='2 kW/m$^2$')
	ax.plot(time3,data3['TC_3'],marker=next(plot_markers),markevery=50,ms=8,label='3 kW/m$^2$')
	ax.plot(time4,data4['TC_3'],marker=next(plot_markers),markevery=50,ms=8,label='5 kW/m$^2$')
	ax.plot(time5,data5['TC_3'],marker=next(plot_markers),markevery=50,ms=8,label='10 kW/m$^2$')
	ax1 = gca()
	xlabel('Time (s)', fontsize=20)
	ylabel('Temperature ($^{\circ}$C)', fontsize=20)
	xticks(fontsize=16)
	yticks(fontsize=16)
	legend(numpoints=1,loc=2,ncol=1,fontsize=16)
	axis([time_offset, len(data5['TC_3']), 0, max(data5['TC_3'])+25])
	# Shrink current axis by 20%
	box = ax.get_position()
	ax.set_position([box.x0, box.y0, box.width * 0.8, box.height])

	# Put a legend to the right of the current axis
	ax.legend(loc='center left', bbox_to_anchor=(1, 0.5))
	grid(True)
	savefig(plot_dir + 'coat_'+ coat_number[i] + '.pdf',format='pdf')
	close()

