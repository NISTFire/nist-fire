# to run - ctrl + b
#these first lines are standard calls for including desired packages for data and plotting
from __future__ import division
import numpy as np
import pandas as pd
from pylab import *
from matplotlib import rcParams
rcParams.update({'figure.autolayout': True})

#read in data file(s) -- point to relative path in repository
#if more than one line of headers at top of document add header=n-1
#typically one header line, header = 1-1 -> header=0 which is default
data = pd.read_csv('../Experimental_Data/RPGB/RP_GB.csv', header=0)
#fds = pd.read_csv('../FDS_Output_Data/testname.csv', header=1)

#plotting
fig = figure()
#here data['Position'] is calling for the column named Position in data file which is x data
#data[0,2 m] is the y data
plot(data['Time (s)'],data['10F'],'k-s', label='10 (kW/m$^2$)',markevery=50,ms=8)
plot(data['Time (s)'],data['12_5F'],'r-*', label='12.5 (kW/m$^2$)',markevery=50,ms=8)
plot(data['Time (s)'],data['15F'],'b-^', label='15 (kW/m$^2$)',markevery=50,ms=8)
plot(data['Time (s)'],data['17_5F'],'g-o', label='17.5 (kW/m$^2$)',markevery=50,ms=8)
plot(data['Time (s)'],data['20F'],'c-<', label='20 (kW/m$^2$)',markevery=50,ms=8)
plot(data['Time (s)'],data['22_5F'],'m->', label='22.5 (kW/m$^2$)',markevery=50,ms=8)
plot(data['Time (s)'],data['25F'],'b-s', label='25 (kW/m$^2$)',markevery=50,ms=8)
ax1 = gca()
xlabel('Time (s)', fontsize=20)
ylabel('Temperature ($^{\circ}$C)', fontsize=20)
xticks(fontsize=16)
yticks(fontsize=16)
grid(True)
ax = gca()
axis([0, 600, 0, 600])
legend(numpoints=1,loc='upper right',fontsize=16 )
#point figures to be written in Figures directory and desired file name
savefig('../Figures/RP_GB_Front.pdf',format='pdf')
close()