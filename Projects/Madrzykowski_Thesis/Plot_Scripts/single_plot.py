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
data = pd.read_csv('../Experimental_Data/TWGas/Reduced/HF_Center_Avg.csv', header=0)
#fds = pd.read_csv('../FDS_Output_Data/testname.csv', header=1)

#plotting
fig = figure()
#here data['Position'] is calling for the column named Position in data file which is x data
#data[0,2 m] is the y data
plot(data['Position'],data['0.2 m'],'k-s', label='0.2 m Above Burner',ms=8)
plot(data['Position'],data['0.4 m'],'r-*', label='0.4 m Above Burner',ms=8)
plot(data['Position'],data['0.6 m'],'b-^', label='0.6 m Above Burner',ms=8)
plot(data['Position'],data['0.8 m'],'g-o', label='0.8 m Above Burner',ms=8)
plot(data['Position'],data['1.0 m'],'c-<', label='1.0 m Above Burner',ms=8)
plot(data['Position'],data['1.2 m'],'m->', label='1.2 m Above Burner',ms=8)
ax1 = gca()
xlabel('Distance from Wall (m)', fontsize=20)
ylabel('Heat Flux (kW/m$^2$)', fontsize=20)
xticks(fontsize=16)
yticks(fontsize=16)
grid(True)
ax = gca()
axis([0, 0.7, 0, 75])
legend(numpoints=1,loc='upper right',fontsize=16 )
#point figures to be written in Figures directory and desired file name
savefig('../Figures/nctw_gas_heatflux.pdf',format='pdf')
close()