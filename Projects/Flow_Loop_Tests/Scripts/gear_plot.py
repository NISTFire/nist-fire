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
data_dir = '../Experimental_Data_Gear/'
plot_dir = '../Figures/Gear/'
info_file = '../Experimental_Data_Gear/Description_of_Experiments.csv'

# Load exp. timings and description file
info = pd.read_csv(info_file, index_col=1)

# Skip files
skip_files = ['description_']

#  =========================
#  = Reading in Data Files =
#  =========================

markers = ['s', '*', '^', 'o', '<', '>', '8', 'h','d','x','p','v','H', 'D', '1', '2', '3', '4', '|']
colors=['r', 'b', 'g', 'c', 'm', '0.75', 'y','#cc5500', '#228b22','#f4a460','#4c177d','firebrick', 'mediumblue', 'darkgreen', 'cadetblue', 'indigo', 'crimson', 'gold']

for f in os.listdir(data_dir):
	if f.endswith('.csv'):
		print
		# Skip files with time information or reduced data files
		if any([substring in f.lower() for substring in skip_files]):
			continue

		# Strip test name from file name
		test_name = f[:-4]
		print 'Test ' + test_name

        # Read in test times to offset plots
		start_of_test = info['Start of Test'][test_name]
		end_of_test = info['End of Test'][test_name]

		# Load first exp. data files
		data = pd.read_csv(data_dir + test_name + '.csv')

        # Offset data time to start of test
		data['Time'] = data['Time'].values - start_of_test

		fig = figure()
		plot(data['Time'],data['TC16'],'b*-',markevery=50,ms=8,label='1')
		plot(data['Time'],data['TC17'],'rs-',markevery=50,ms=8,label='2')
		plot(data['Time'],data['TC18'],'g^-',markevery=50,ms=8,label='3')
		plot(data['Time'],data['TC19'],'co-',markevery=50,ms=8,label='4')
		plot(data['Time'],data['TC20'],'m<-',markevery=50,ms=8,label='5')
		plot(data['Time'],data['TC21'],'k8-',markevery=50,ms=8,label='6')
		ax1 = gca()
		xlabel('Time (s)', fontsize=20)
		ylabel('Temperature ($^{\circ}$C)', fontsize=20)
		xticks(fontsize=16)
		yticks(fontsize=16)
		legend(numpoints=1,loc=2,ncol=1,fontsize=16)
		axis([0, end_of_test - start_of_test, 0, 350])
		grid(True)
		savefig(plot_dir + test_name + '.pdf',format='pdf')
		close()

