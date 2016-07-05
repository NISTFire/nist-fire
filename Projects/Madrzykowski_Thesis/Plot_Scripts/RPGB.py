# to run - ctrl + b
#these first lines are standard calls for including desired packages for data and plotting
from __future__ import division
import numpy as np
import pandas as pd
from pylab import *
# from matplotlib import rcParams
# rcParams.update({'figure.autolayout': True})
from itertools import cycle

#read in data file(s) -- point to relative path in repository
#if more than one line of headers at top of document add header=n-1
#typically one header line, header = 1-1 -> header=0 which is default
data = pd.read_csv('../Experimental_Data/RPGB/RP_GB.csv', header=0)
#fds = pd.read_csv('../FDS_Output_Data/testname.csv', header=1)

markers = cycle(['s', '*', '^', 'o', '<', '>', '8', 'h','d','x','p','v','H', 'D', '1', '2', '3', '4', '|'])
colors = [(31, 119, 180), (174, 199, 232), (255, 127, 14), (255, 187, 120),
             (44, 160, 44), (152, 223, 138), (214, 39, 40), (255, 152, 150),
             (148, 103, 189), (197, 176, 213), (140, 86, 75), (196, 156, 148),
             (227, 119, 194), (247, 182, 210), (127, 127, 127), (199, 199, 199),
             (188, 189, 34), (219, 219, 141), (23, 190, 207), (158, 218, 229)]

# Scale the RGB values to the [0, 1] range, which is the format matplotlib accepts.
for i in range(len(colors)):
    r, g, b = colors[i]
    colors[i] = (r / 255., g / 255., b / 255.)


#plotting
fig = plt.figure()
#here data['Position'] is calling for the column named Position in data file which is x data
#data[0,2 m] is the y data
rcParams['axes.prop_cycle']=(cycler('color',colors))
plt.plot(data['Time (s)'],data['10F'],label='10 (kW/m$^2$)',markevery=50,ms=8,marker=next(markers))
plt.plot(data['Time (s)'],data['12_5F'],label='12.5 (kW/m$^2$)',markevery=50,ms=8,marker=next(markers))
plt.plot(data['Time (s)'],data['15F'],label='15 (kW/m$^2$)',markevery=50,ms=8,marker=next(markers))
plt.plot(data['Time (s)'],data['17_5F'],label='17.5 (kW/m$^2$)',markevery=50,ms=8,marker=next(markers))
plt.plot(data['Time (s)'],data['20F'],label='20 (kW/m$^2$)',markevery=50,ms=8,marker=next(markers))
plt.plot(data['Time (s)'],data['22_5F'],label='22.5 (kW/m$^2$)',markevery=50,ms=8,marker=next(markers))
plt.plot(data['Time (s)'],data['25F'],label='25 (kW/m$^2$)',markevery=50,ms=8,marker=next(markers))
ax1 = gca()
xlabel('Time (s)', fontsize=20)
ylabel('Temperature ($^{\circ}$C)', fontsize=20)
xticks(fontsize=16)
yticks(fontsize=16)
grid(True)
ax1 = gca()
axis([0, 600, 0, 500])
box = ax1.get_position()
ax1.set_position([box.x0, box.y0, box.width * 0.75, box.height])
ax1.legend(loc='center left', bbox_to_anchor=(1, 0.5))
# legend(numpoints=1,loc='upper right',fontsize=16 )
#point figures to be written in Figures directory and desired file name
savefig('../Figures/RP_GB_Front.pdf',format='pdf')
close()