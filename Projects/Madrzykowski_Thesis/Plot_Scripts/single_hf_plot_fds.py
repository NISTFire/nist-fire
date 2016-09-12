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
data_dir = '../FDS_Output_Files/'
plot_dir = '../Figures/'
test_name = ['IWGB_NG_HF_Offset_Avg_FDS','IWGB_NG_HF_Center_Avg_FDS']
#fds = pd.read_csv('../FDS_Output_Data/testname.csv', header=1)

markers =['s', '*', '^', 'o', '<', '>', '8', 'h','d','x','p','v','H', 'D', '1', '2', '3', '4', '|','s']
colors = [(31, 119, 180), (174, 199, 232), (255, 127, 14), (255, 187, 120),
             (44, 160, 44), (152, 223, 138), (214, 39, 40), (255, 152, 150),
             (148, 103, 189), (197, 176, 213), (140, 86, 75), (196, 156, 148),
             (227, 119, 194), (247, 182, 210), (127, 127, 127), (199, 199, 199),
             (188, 189, 34), (219, 219, 141), (23, 190, 207), (158, 218, 229)]

# Scale the RGB values to the [0, 1] range, which is the format matplotlib accepts.
for i in range(len(colors)):
    r, g, b = colors[i]
    colors[i] = (r / 255., g / 255., b / 255.)

for j in range(len(test_name)):
	print(test_name[j])
	try:
		data = pd.read_csv(data_dir + test_name[j] + '.csv', header=0)
	except:
		continue

	#plotting
	fig = figure()
	#here data['Position'] is calling for the column named Position in data file which is x data
	#data[0.2 m] is the y data
	rcParams['axes.prop_cycle']=(cycler('color',colors) + cycler('marker',markers))
	plot(data['Position'],data['0.2 m'], label='0.2 m Above Burner',ms=8)
	plot(data['Position'],data['0.4 m'], label='0.4 m Above Burner',ms=8)
	plot(data['Position'],data['0.6 m'], label='0.6 m Above Burner',ms=8)
	plot(data['Position'],data['0.8 m'], label='0.8 m Above Burner',ms=8)
	plot(data['Position'],data['1.0 m'], label='1.0 m Above Burner',ms=8)
	plot(data['Position'],data['1.2 m'], label='1.2 m Above Burner',ms=8)
	ax1 = gca()
	xlabel('Distance from Wall (m)', fontsize=20)
	ylabel('Heat Flux (kW/m$^2$)', fontsize=20)
	xticks(fontsize=16)
	yticks(fontsize=16)
	grid(True)
	ax = gca()
	axis([0, 0.35, 0, 70])
	legend(numpoints=1,loc='upper right',fontsize=16 )
	#point figures to be written in Figures directory and desired file name
	savefig(plot_dir + test_name[j] + '.pdf',format='pdf')
	close()