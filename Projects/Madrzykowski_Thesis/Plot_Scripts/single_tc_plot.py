# to run - ctrl + b
#these first lines are standard calls for including desired packages for data and plotting
from __future__ import division
import numpy as np
import pandas as pd
import itertools
from pylab import *
from matplotlib import rcParams
rcParams.update({'figure.autolayout': True})

#read in data file(s) -- point to relative path in repository
#if more than one line of headers at top of document add header=n-1
#typically one header line, header = 1-1 -> header=0 which is default
data_dir = '../Experimental_Data/TWPUF/'
plot_dir = '../Figures/'
test_name = 'NCTW_PUF_TC_Plume_Avg'
data = pd.read_csv(data_dir + test_name + '.csv', header=0)
#fds = pd.read_csv('../FDS_Output_Data/testname.csv', header=1)

markers = ['s', '*', '^', 'o', '<', '>', '8', 'h','d', 'x','p','v']
headers = ['0.2 m','0.4 m','0.6 m','0.8 m','1.0 m','1.2 m','1.4 m','1.6 m','1.8 m','2.0 m','2.2 m']
labels = ['0.2 m Above Burner','0.4 m Above Burner','0.6 m Above Burner','0.8 m Above Burner','1.0 m Above Burner',
		'1.2 m Above Burner','1.4 m Above Burner','1.6 m Above Burner','1.8 m Above Burner','2.0 m Above Burner',
		'2.2 m Above Burner']

fig = figure()
#here data['Position'] is calling for the column named Position in data file which is x data
#data[0,2 m] is the y data
for i in range(len(headers)):
	y = data[headers[i]]
	plt.rc('axes', color_cycle=['k', 'r', 'b', 'g', 'c', 'm', '0.75', 'y','#cc5500', '#228b22','#f4a460','#4c177d'])
	plot(data['Position'],y,marker=markers[i],label=labels[i], ms=8)
ax1 = gca()
xlabel('Distance from Wall (m)', fontsize=20)
ylabel('Temperature ($^{\circ}$C)', fontsize=20)
xticks(fontsize=16)
yticks(fontsize=16)
grid(True)
ax = gca()
axis([0, 0.7, 0, 1500])
legend(numpoints=1,loc='upper right',fontsize=16 )
#point figures to be written in Figures directory and desired file name
savefig(plot_dir + test_name + '.pdf',format='pdf')
close()