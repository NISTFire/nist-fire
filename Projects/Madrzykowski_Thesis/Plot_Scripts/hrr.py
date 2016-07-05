from __future__ import division
import numpy as np
import numpy.ma as ma
import pandas as pd
import itertools
from pylab import *
from matplotlib import rcParams
# rcParams.update({'figure.autolayout': True})

data_dir = '../Experimental_Data/STHRR/'
plot_dir = '../Figures/'
test_name = 'ST_Gas_HRR'
data = pd.read_csv(data_dir + test_name + '.csv', header=0)
data2 = pd.read_csv(data_dir + test_name + '.csv', header=0,index_col=0)

fuel = test_name[3:-3]
if 'Gas' in str(fuel):
	col = 2
else:
	col = 1
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
# print (2*data2.std(axis=1)[100:200])

fig = figure()
for i in range(data.shape[1]-1):
	y = data[fuel+str(i+1)]
	plot(data['Time (s)'],y,color=colors[i],marker=markers[i],markevery=50,ms=8,label=fuel.replace('_',' ')+str(i+1))
plot(data['Time (s)'],data2.mean(axis=1),'k',label=fuel.replace('_',' ')+'AVG',linewidth=3)
plt.fill_between(data['Time (s)'],data2.mean(axis=1)+2*data2.std(axis=1), data2.mean(axis=1)-2*data2.std(axis=1), facecolor='gray',alpha=0.5, interpolate=True,linewidth=3)
ax1 = gca()
xlabel('Time (s)', fontsize=20)
ylabel('Heat Release Rate (kW)', fontsize=20)
xticks(fontsize=16)
yticks(fontsize=16)
legend(numpoints=1,loc=1,ncol=col,fontsize=16)
axis([0, 300, 0, 120])
box = ax1.get_position()
ax1.set_position([box.x0, box.y0, box.width * 0.85, box.height])
ax1.legend(loc='center left', bbox_to_anchor=(1, 0.5))
grid(True)
savefig(plot_dir + test_name + '.pdf',format='pdf')
close()

fig = figure()
for i in range(data.shape[1]-1):
	y = data[fuel+str(i+1)]
	plot(data['Time (s)'],y,color=colors[i],marker=markers[i],markevery=50,ms=8,label=fuel.replace('_',' ')+str(i+1))
plot(data['Time (s)'],data2.mean(axis=1),'k',label=fuel.replace('_',' ')+'AVG',linewidth=3)
ax1 = gca()
xlabel('Time (s)')
ylabel('Heat Release Rate (kW)')
xticks(fontsize=16)
yticks(fontsize=16)
legend(numpoints=1,loc=1,ncol=col,fontsize=16)
axis([0, 300, 0, 120])
box = ax1.get_position()
ax1.set_position([box.x0, box.y0, box.width * 0.85, box.height])
ax1.legend(loc='center left', bbox_to_anchor=(1, 0.5))
grid(True)
savefig(plot_dir + test_name + '_nosigma.pdf',format='pdf')
close()