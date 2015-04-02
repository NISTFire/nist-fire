from __future__ import division
import numpy as np
import numpy.ma as ma
import pandas as pd
import itertools
from pylab import *
from matplotlib import rcParams
rcParams.update({'figure.autolayout': True})

data_dir = '../Experimental_Data/FHGAS/'
plot_dir = '../Figures/'
test_name = 'HF_GAS'
data = pd.read_csv(data_dir + test_name + '.csv',header=0)
data2 = pd.read_csv(data_dir + test_name + '.csv',header=0,index_col=0)

markers = ['s', '*', '^', 'o', '<', '>', '8', 'h','d','x','p','v','H', 'D', '1', '2', '3', '4', '|']
colors=['r', 'b', 'g', 'c', 'm', '0.75', 'y','#cc5500', '#228b22','#f4a460','#4c177d','firebrick', 'mediumblue', 'darkgreen', 'cadetblue', 'indigo', 'crimson', 'gold']

fig = figure()
for i in range(data.shape[1]-1):
	y = data.iloc[:,i+1]
	plot(data['Time (s)'],y,color=colors[i],marker=markers[i],markevery=50,ms=8,label=data.columns[i+1])
plot(data['Time (s)'],data2.mean(axis=1),'k',label=test_name+'_AVG',linewidth=3)
ax1 = gca()
xlabel('Time (s)', fontsize=20)
ylabel('Heat Flux (kW/m$^2$)', fontsize=20)
xticks(fontsize=16)
yticks(fontsize=16)
legend(numpoints=1,loc=1,ncol=1,fontsize=16)
axis([0, 300, 0, 6])
savefig(plot_dir + test_name + '.pdf',format='pdf')
close()