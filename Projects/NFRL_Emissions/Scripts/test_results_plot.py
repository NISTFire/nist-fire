#Weinschenk
#10-14

from __future__ import division
import numpy as np
import pandas as pd
from pylab import *
from matplotlib import rcParams
rcParams.update({'figure.autolayout': True})


PVC_T3 = pd.read_csv('../Experimental_Data/9-26-2014-NFRL-PVCWoodCribTrain3-Post.csv', header=0)
PVC_T4 = pd.read_csv('../Experimental_Data/9-26-2014-NFRL-PVCWoodCribTrain4-Post.csv', header=0)
NG_Cal = pd.read_csv('../Experimental_Data/10-3-2014-NFRL-NGCal9m-Post.csv', header=0)

fig = figure()
plot(PVC_T3['Time (s)'],1.044*PVC_T3['67: HRR (kW)'],'k-',mfc='none',label='Wood Crib w/ PVC - Train 3 ',linewidth=2)
plot(PVC_T4['Time (s)'],1.044*PVC_T4['67: HRR (kW)'],'r--',mfc='none',label='Wood Crib w/ PVC - Train 4 ',linewidth=2)
xlabel('Time (s)')
ylabel('HRR (kW)')
legend(numpoints=1,loc=1)
axis([0, 5000, 0, 1300])
savefig('../Figures/HRR_PVC_2Train.pdf',format='pdf')
close()

fig = figure()
plot(NG_Cal['Time (s)'],NG_Cal['66: HRRburner (kW)'],'k-',mfc='none',label='Burner Calculated HRR',linewidth=2)
plot(NG_Cal['Time (s)'],NG_Cal['67: HRR (kW)'],'r--',mfc='none',label='Calorimetry Calculated HRR',linewidth=2)
xlabel('Time (s)')
ylabel('HRR (kW)')
legend(numpoints=1,loc=2)
axis([0, 2500, 0, 3000])
savefig('../Figures/HRR_Calibration.pdf',format='pdf')
close()