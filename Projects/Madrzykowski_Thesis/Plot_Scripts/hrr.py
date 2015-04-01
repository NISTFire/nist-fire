from __future__ import division
import numpy as np
import numpy.ma as ma
import pandas as pd
import itertools
from pylab import *
from matplotlib import rcParams
rcParams.update({'figure.autolayout': True})

data_dir = '../Experimental_Data/STHRR/'
plot_dir = '../Figures/'
test_name = 'ST_Gas_HRR'
data = pd.read_csv(data_dir + test_name + '.csv', header=0)
data2 = pd.read_csv(data_dir + test_name + '.csv', header=0,index_col=0)

fuel = 'Gas_'
markers = ['s', '*', '^', 'o', '<', '>', '8', 'h','d','x','p','v','H', 'D', '1', '2', '3', '4', '|']
colors=['r', 'b', 'g', 'c', 'm', '0.75', 'y','#cc5500', '#228b22','#f4a460','#4c177d','firebrick', 'mediumblue', 'darkgreen', 'cadetblue', 'indigo', 'crimson', 'gold']

print 2*data2.std(axis=1)[100:200]

fig = figure()
for i in range(data.shape[1]-1):
	y = data[fuel+str(i+1)]
	plot(data['Time (s)'],y,color=colors[i],marker=markers[i],markevery=50,ms=8,label=fuel+str(i+1))
plot(data['Time (s)'],data2.mean(axis=1),'k',label=fuel+'_AVG',linewidth=3)
plt.fill_between(data['Time (s)'],data2.mean(axis=1)+2*data2.std(axis=1), data2.mean(axis=1)-2*data2.std(axis=1), facecolor='gray',alpha=0.5, interpolate=True,linewidth=3)
ax1 = gca()
xlabel('Time (s)')
ylabel('Heat Release Rate (kW)')
legend(numpoints=1,loc=1,ncol=2)
axis([0, 300, 0, 120])
savefig(plot_dir + test_name + '.pdf',format='pdf')
close()

fig = figure()
for i in range(data.shape[1]-1):
	y = data[fuel+str(i+1)]
	plot(data['Time (s)'],y,color=colors[i],marker=markers[i],markevery=50,ms=8,label=fuel+str(i+1))
plot(data['Time (s)'],data2.mean(axis=1),'k',label=fuel+'_AVG',linewidth=3)
ax1 = gca()
xlabel('Time (s)')
ylabel('Heat Release Rate (kW)')
legend(numpoints=1,loc=1,ncol=2)
axis([0, 300, 0, 120])
savefig(plot_dir + test_name + '_nosigma.pdf',format='pdf')
close()