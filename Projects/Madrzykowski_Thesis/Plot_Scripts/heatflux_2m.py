from __future__ import division
import numpy as np
import numpy.ma as ma
import pandas as pd
import itertools
from pylab import *
from matplotlib import rcParams
rcParams.update({'figure.autolayout': True})

data_dir = '../Experimental_Data/STData/'
plot_dir = '../Figures/'
test_name = 'HF_Gas_2m'
data = pd.read_csv(data_dir + test_name + '.csv',header=0)
data2 = pd.read_csv(data_dir + test_name + '.csv',header=0,index_col=0)

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

fig = figure()
for i in range(data.shape[1]-1):
	y = data.iloc[:,i+1]
	plot(data['Time (s)'],y,color=colors[i],marker=markers[i],markevery=50,ms=8,label=data.columns[i+1].replace('_', ' '))
plot(data['Time (s)'],data2.mean(axis=1),'k',label=test_name.replace('_', ' ')+'_AVG'.replace('_', ' '),linewidth=3)
ax1 = gca()
xlabel('Time (s)', fontsize=20)
ylabel('Heat Flux (kW/m$^2$)', fontsize=20)
xticks(fontsize=16)
yticks(fontsize=16)
legend(numpoints=1,loc=1,ncol=1,fontsize=16)
legend(bbox_to_anchor=(1.04,1.0))
axis([0, 300, 0, 4])
grid(True)
savefig(plot_dir + test_name + '.pdf',format='pdf')
close()