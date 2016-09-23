from __future__ import division
import numpy as np
import pandas as pd
import itertools
from pylab import *
from itertools import cycle

data_dir = '../Experimental_Data/Vertical_Comp/'
plot_dir = '../Figures/'

y = [0.2,0.4,0.6,0.8,1.0,1.2,1.4,1.6,1.8,2.0,2.2]

test_name = 'IWGB_NG_TC_Surface_Center_Avg'
distance = ['_0D','_0p5D','_1D','_2D']

data = pd.read_csv(data_dir+test_name+'.csv', header=0)
fds  = pd.read_csv(data_dir+test_name+'_FDS.csv', header=0)

for i in range(4):
	data_slice = np.squeeze(np.asarray(data.iloc[[i],1:]))
	fds_slice = np.squeeze(np.asarray(fds.iloc[[i],1:]))

	fig = figure()
	plot(data_slice,y,linestyle='None',marker='o',ms=8,color='k',label='Experiment')
	plot(fds_slice,y,'k',label = 'FDS')
	ax1 = gca()
	xlabel('Temperature ($^{\circ}$C)', fontsize=20)
	ylabel('Distance above Burner (m)', fontsize=20)
	xticks(fontsize=16)
	yticks(fontsize=16)
	grid(True)
	ax = gca()
	axis([0, 600, 0, 2.2])
	legend(numpoints=1,loc='upper right',fontsize=16 )
	savefig(plot_dir + test_name + distance[i] + '.pdf',format='pdf')
	close()

