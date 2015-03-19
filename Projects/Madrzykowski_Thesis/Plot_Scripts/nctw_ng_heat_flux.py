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
data = pd.read_csv('../Experimental_Data/nctw_ng_heatflux.csv')

#plotting
fig = figure()
plot(data['Position'],data['0.2 m'],'k-+', label='0.2 m Above Burner')
plot(data['Position'],data['0.4 m'],'r-*', label='0.4 m Above Burner')
plot(data['Position'],data['0.6 m'],'b-^', label='0.6 m Above Burner')
plot(data['Position'],data['0.8 m'],'g-o', label='0.8 m Above Burner')
plot(data['Position'],data['1.0 m'],'c-<', label='1.0 m Above Burner')
plot(data['Position'],data['1.2 m'],'m->', label='1.2 m Above Burner')
ax1 = gca()
markersize=20
xlabel('Distance from Wall (m)')
ylabel('Heat Flux (kW/m$^2$)')
grid(True)
ax = gca()
axis([0, 0.7, 0, 50])
legend(numpoints=1,loc='upper right' )
savefig('../Figures/nctw_ng_heatflux.pdf',format='pdf')
close()