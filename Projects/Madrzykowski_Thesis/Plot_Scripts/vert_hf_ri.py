from __future__ import division
import numpy as np
import pandas as pd
import itertools
from pylab import *
from matplotlib import rcParams
from itertools import cycle
rcParams.update({'figure.autolayout': True})

data_dir = '../Experimental_Data/Vertical_Comp/'
fds_dir = '../FDS_Output_Files/'
plot_dir = '../Figures/'

y_data = [0.2,0.4,0.6,0.8,1.0,1.2]
y_fds = [0.2,0.4,0.6,0.8,1.0,1.2]

test_name = 'IWGB_NG_HF_Offset_Avg'
fds_name = 'hfwalledge_avg_2D'
distance = ['_0D','_0pD','_1D','_2D']

data = pd.read_csv(data_dir+test_name+'.csv', header=0)
fds  = pd.read_csv(fds_dir+fds_name+'.csv', header=0)


data_slice = np.squeeze(np.asarray(data.iloc[[3],1:]))
fds_slice_05 = np.squeeze(np.asarray(fds.iloc[[0],1:]))
fds_slice_10 = np.squeeze(np.asarray(fds.iloc[[1],1:]))
# fds_slice_20 = np.squeeze(np.asarray(fds.iloc[[2],1:]))

fig = figure()
errorbar(data_slice,y_data,xerr=0.15*data_slice,linestyle='None',marker='o',ms=8,color='k',label='Experiment')
plot(fds_slice_05,y_fds,'k',label = 'FDS 05')
plot(fds_slice_10,y_fds,'r',label = 'FDS 10')
# plot(fds_slice_20,y_fds,'b',label = 'FDS 20')	
xlabel('Heat flux (kW/m$^{2}$)', fontsize=20)
ylabel('Distance above Burner (m)', fontsize=20)
xticks(fontsize=16)
yticks(fontsize=16)
grid(True)
# axis([0, 850, 0, 2.4 ])
legend(numpoints=1,loc='upper right',fontsize=16 )
savefig(plot_dir + test_name + distance[3] + '_RI.pdf',format='pdf')
close()

