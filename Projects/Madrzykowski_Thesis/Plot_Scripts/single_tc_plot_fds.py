# to run - ctrl + b
#these first lines are standard calls for including desired packages for data and plotting
from __future__ import division
import numpy as np
import pandas as pd
import itertools
from pylab import *
# from matplotlib import rcParams
# rcParams.update({'figure.autolayout': True})
from itertools import cycle

#read in data file(s) -- point to relative path in repository
#if more than one line of headers at top of document add header=n-1
#typically one header line, header = 1-1 -> header=0 which is default
data_dir = '../FDS_Output_Files/'
plot_dir = '../Figures/'
test_name = ['IWGB_NG_TC_Plume_Avg_FDS','IWGB_NG_TC_Surface_Center_Avg_FDS']

markers = ['s', '*', '^', 'o', '<', '>', '8', 'h','d','x','p','v','H', 'D', '1', '2', '3', '4', '|']
colors = [(31, 119, 180), (174, 199, 232), (255, 127, 14), (255, 187, 120),
             (44, 160, 44), (152, 223, 138), (214, 39, 40), (255, 152, 150),
             (148, 103, 189), (197, 176, 213), (140, 86, 75), (196, 156, 148),
             (227, 119, 194), (247, 182, 210), (127, 127, 127), (199, 199, 199),
             (188, 189, 34), (219, 219, 141), (23, 190, 207), (158, 218, 229)]
for i in range(len(colors)):
    r, g, b = colors[i]
    colors[i] = (r / 255., g / 255., b / 255.)


for j in range(len(test_name)):
	print(test_name[j])
	try:
		data = pd.read_csv(data_dir + test_name[j] + '.csv', header=0)
	except:
		continue

	if 'Plume' in test_name[j]:
		labels = ['0.2 m Above Burner','0.4 m Above Burner','0.6 m Above Burner','0.8 m Above Burner','1.0 m Above Burner',
			'1.2 m Above Burner','1.4 m Above Burner','1.6 m Above Burner','1.8 m Above Burner','2.0 m Above Burner',
			'2.2 m Above Burner']
	if 'NG_TC_Surface_Offset' in test_name[j]:
		labels = ['0.2 m Above Burner','0.4 m Above Burner','0.6 m Above Burner','0.8 m Above Burner','1.0 m Above Burner',
			'1.2 m Above Burner','1.4 m Above Burner','1.8 m Above Burner','2.0 m Above Burner',
			'2.2 m Above Burner']
	else:
		labels = ['0.2 m Above Burner','0.4 m Above Burner','0.6 m Above Burner','0.8 m Above Burner','1.0 m Above Burner',
			'1.2 m Above Burner','1.4 m Above Burner','1.6 m Above Burner','1.8 m Above Burner','2.0 m Above Burner',
			'2.2 m Above Burner']

	fig = figure()
	for i in range(len(labels)):
		y = data[data.columns[i+1]]
		if max(y) > 2500.:
			continue
		else:
			plot(data['Position'],y,marker=markers[i],color=colors[i],label=(labels[i]), ms=8)
	ax1 = gca()
	xlabel('Distance from Wall (m)', fontsize=20)
	ylabel('Temperature ($^{\circ}$C)', fontsize=20)
	xticks(fontsize=16)
	yticks(fontsize=16)
	grid(True)
	ax = gca()
	# axis([0, 0.7, 0, 700])
	box = ax1.get_position()
	ax1.set_position([box.x0, box.y0, box.width * 0.75, box.height])
	ax1.legend(loc='center left', bbox_to_anchor=(.9, 0.5),fontsize=14)
	# legend(numpoints=1,loc='upper right',fontsize=16 )
	#point figures to be written in Figures directory and desired file name
	savefig(plot_dir + test_name[j] + '.pdf',format='pdf')
	close()