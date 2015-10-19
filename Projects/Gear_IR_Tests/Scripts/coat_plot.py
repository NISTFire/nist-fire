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
data_dir = '../Experimental_Data/Coats/'
plot_dir = '../Figures/Coats/'

#  =========================
#  = Reading in Data Files =
#  =========================

for f in os.listdir(data_dir):
	if f.endswith('.csv'):
		print()

		# Strip test name from file name
		test_name = f[:-4]
		print ('Test ' + test_name)

		# Load first exp. data files
		data = pd.read_csv(data_dir + test_name + '.csv')
		time = np.arange(len(data['TC_3']))
		time_offset = 60

		fig = figure()
		plot(time,data['TC_3'],'b*-',markevery=50,ms=8,label='Inside Coat Temperature')
		ax1 = gca()
		xlabel('Time (s)', fontsize=20)
		ylabel('Temperature ($^{\circ}$C)', fontsize=20)
		xticks(fontsize=16)
		yticks(fontsize=16)
		legend(numpoints=1,loc=2,ncol=1,fontsize=16)
		axis([time_offset, len(data['TC_3']), 0, max(data['TC_3'])+25])
		grid(True)
		savefig(plot_dir + test_name + '.pdf',format='pdf')
		close()

