from __future__ import division
import numpy as np
import pandas as pd
import itertools
from pylab import *
from matplotlib import rcParams
from itertools import cycle
rcParams.update({'figure.autolayout': True})

data_dir = '../Experimental_Data/FHNG/'
fds_dir = '../FDS_Output_Files/'
plot_dir = '../Figures/'

y_data = [0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8,0.9,1.0,1.1,1.2]
y_fds = [0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8,0.9,1.0,1.1,1.2]

test_name = 'FHNG01'
fds_name_05 = 'FHNG_80kW_FreeBurn_RI=05_devc'
fds_name_05_022 = 'FHNG_80kW_FreeBurn_022_RI=05_devc'
fds_name_05_025 = 'FHNG_80kW_FreeBurn_025_RI=05_devc'
fds_name_05_030 = 'FHNG_80kW_FreeBurn_030_RI=05_devc'

fds_name_10 = 'FHNG_80kW_FreeBurn_RI=10_devc'
fds_name_10_022 = 'FHNG_80kW_FreeBurn_022_RI=10_devc'

fds_name_20 = 'FHNG_80kW_FreeBurn_RI=20_devc'
fds_name_20_022 = 'FHNG_80kW_FreeBurn_022_RI=20_devc'



data = pd.read_csv(data_dir+test_name+'.csv', header=0)
fds_05  = pd.read_csv(fds_dir+fds_name_05+'.csv', header=1)
fds_05_022  = pd.read_csv(fds_dir+fds_name_05_022+'.csv', header=1)
fds_05_025  = pd.read_csv(fds_dir+fds_name_05_025+'.csv', header=1)
fds_05_030  = pd.read_csv(fds_dir+fds_name_05_030+'.csv', header=1)

fds_10 = pd.read_csv(fds_dir+fds_name_10+'.csv', header=1)
fds_10_022 = pd.read_csv(fds_dir+fds_name_10_022+'.csv', header=1)

fds_20 = pd.read_csv(fds_dir+fds_name_20+'.csv', header=1)
fds_20_022 = pd.read_csv(fds_dir+fds_name_20_022+'.csv', header=1)


#change from 1:13 to 13:25 for TC sensors versus gas temperature
data_slice = data.iloc[:,1:13].mean()
fds_slice_05 = fds_05.iloc[:,1:13].mean()
fds_slice_05_022 = fds_05_022.iloc[:,1:13].mean()
fds_slice_05_025 = fds_05_025.iloc[:,1:13].mean()
fds_slice_05_030 = fds_05_030.iloc[:,1:13].mean()

fds_slice_10 = fds_10.iloc[:,1:13].mean()
fds_slice_10_022 = fds_10_022.iloc[:,1:13].mean()

fds_slice_20 = fds_20.iloc[:,1:13].mean()
fds_slice_20_022 = fds_20_022.iloc[:,1:13].mean()

fig = figure()
errorbar(data_slice,y_data,xerr=0.15*data_slice,linestyle='None',marker='o',ms=8,color='k',label='Experiment')
plot(fds_slice_05,y_fds,color ='purple', marker = 'd',label = 'FDS RF = 0.20 (Default)')
plot(fds_slice_05_022,y_fds,'rx-',label = 'FDS 05 RF = 0.22')
plot(fds_slice_05_025,y_fds,'bo-',label = 'FDS 05 RF = 0.25')
plot(fds_slice_05_030,y_fds,'gs-',label = 'FDS 05 RF = 0.30')
xlabel('Temperature ($^{\circ}$C)', fontsize=20)
ylabel('Distance above Burner (m)', fontsize=20)
xticks(fontsize=16)
yticks(fontsize=16)
grid(True)
axis([150, 1000, 0, 1.3 ])
legend(numpoints=1,loc='upper right',fontsize=16 )
savefig(plot_dir + test_name + '_RF_RI5.pdf',format='pdf')
close()

fig = figure()
plot(fds_05['Time'],fds_05['GHF1'],color='purple',linestyle='-.',marker = 'd',markevery=25,label = 'FDS RF = 0.20 (Default)')
plot(fds_05_022['Time'],fds_05_022['GHF1'],color='red',linestyle='-.',marker='x',markevery=25,label = 'FDS RF = 0.22')
plot(fds_05_025['Time'],fds_05_025['GHF1'],color='blue',linestyle='-.',marker='o',markevery=25,label = 'FDS RF = 0.25')
plot(fds_05_030['Time'],fds_05_030['GHF1'],color='green',linestyle='-.',marker='^',markevery=25,label = 'FDS RF = 0.30')
plot(data['Time (s)'], data['Average HF'], 'k', marker='s', markevery=25, linewidth=3, label='Experiment')
xlabel('Time (s)', fontsize=20)
ylabel('Heat Flux (kW/m$^2$)', fontsize=20)
xticks(fontsize=16)
yticks(fontsize=16)
grid(True)
axis([0, 225, 0, 3 ])
legend(numpoints=1,loc='lower right',fontsize=16 )
savefig(plot_dir + test_name + '_HF_RI5.pdf',format='pdf')
close()

fig = figure()
errorbar(data_slice,y_data,xerr=0.15*data_slice,linestyle='None',marker='o',ms=8,color='k',label='Experiment')
plot(fds_slice_05,y_fds,'rx-',label = 'FDS 05')
plot(fds_slice_10,y_fds,'bo-',label = 'FDS 10')
plot(fds_slice_20,y_fds,'gs-',label = 'FDS 20')
xlabel('Temperature ($^{\circ}$C)', fontsize=20)
ylabel('Distance above Burner (m)', fontsize=20)
xticks(fontsize=16)
yticks(fontsize=16)
grid(True)
axis([150, 1000, 0, 1.3 ])
legend(numpoints=1,loc='upper right',fontsize=16 )
savefig(plot_dir + test_name + '_RI.pdf',format='pdf')
close()

fig = figure()
plot(fds_05['Time'],fds_05['GHF1'],color='red',linestyle='-.',marker='x',markevery=25,label = 'FDS 05')
plot(fds_10['Time'],fds_10['GHF1'],color='blue',linestyle='-.',marker='o',markevery=25,label = 'FDS 10')
plot(fds_20['Time'],fds_20['GHF1'],color='green',linestyle='-.',marker='^',markevery=25,label = 'FDS 20')
plot(data['Time (s)'], data['Average HF'], 'k', marker='s', markevery=25, linewidth=3,label='Experiment')
xlabel('Time (s)', fontsize=20)
ylabel('Heat Flux (kW/m$^2$)', fontsize=20)
xticks(fontsize=16)
yticks(fontsize=16)
grid(True)
axis([0, 225, 0, 3 ])
legend(numpoints=1,loc='lower right',fontsize=16 )
savefig(plot_dir + test_name + '_HF_RI.pdf',format='pdf')
close()


fig = figure()
errorbar(data_slice,y_data,xerr=0.15*data_slice,linestyle='None',marker='o',ms=8,color='k',label='Experiment')
plot(fds_slice_05_022,y_fds,'rx-',label = 'FDS 05')
plot(fds_slice_10_022,y_fds,'bo-',label = 'FDS 10')
plot(fds_slice_20_022,y_fds,'gs-',label = 'FDS 20')
xlabel('Temperature ($^{\circ}$C)', fontsize=20)
ylabel('Distance above Burner (m)', fontsize=20)
xticks(fontsize=16)
yticks(fontsize=16)
grid(True)
axis([150, 1000, 0, 1.3 ])
legend(numpoints=1,loc='upper right',fontsize=16 )
savefig(plot_dir + test_name + '_RF22_RI.pdf',format='pdf')
close()

fig = figure()
plot(fds_05_022['Time'],fds_05_022['GHF1'],color='red',marker='x',markevery=25,label = 'FDS 05')
plot(fds_10_022['Time'],fds_10_022['GHF1'],color='blue',marker='o',markevery=25,label = 'FDS 10')
plot(fds_20_022['Time'],fds_20_022['GHF1'],color='green',marker='^',markevery=25,label = 'FDS 20')
plot(data['Time (s)'], data['Average HF'], 'k', marker='s', markevery=25, label='Experiment')
xlabel('Time (s)', fontsize=20)
ylabel('Heat Flux (kW/m$^2$)', fontsize=20)
xticks(fontsize=16)
yticks(fontsize=16)
grid(True)
axis([0, 225, 0, 3 ])
legend(numpoints=1,loc='lower right',fontsize=16 )
savefig(plot_dir + test_name + '_HF_RF22_RI.pdf',format='pdf')
close()


