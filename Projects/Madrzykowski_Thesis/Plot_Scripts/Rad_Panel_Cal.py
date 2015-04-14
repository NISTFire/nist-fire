from __future__ import division

import numpy as np
import pandas as pd
from pylab import *
rc('font',**{'size':14})
params = {'legend.fontsize': 12,
          'legend.linewidth': 4,
          'lines.linewidth': 1.75}
from matplotlib import rcParams
rcParams.update({'figure.autolayout': True})


#read in data file(s)
data = pd.read_csv('../Experimental_Data/Rad_Panel_Cal.csv')

#plotting
fig = figure()
plot(data['Distance'],data['Heatflux'],'k-+', label='Centerline')

ax1 = gca()
markersize=20
xlabel('Distance from Sample Face Closest to Radiant Panel (mm)')
ylabel('Heat Flux (kW/m$^2$)')
grid(True)
ax = gca()
axis([0, 600, 0, 30])
legend(numpoints=1,loc='upper right' )
savefig('../Figures/Rad_Panel_Cal.pdf',format='pdf')
close()