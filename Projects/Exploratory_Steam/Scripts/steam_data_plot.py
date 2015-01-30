#Weinschenk
#1-15

from __future__ import division
import os
import numpy as np
import pandas as pd
from pylab import *
import datetime
#from bokeh.plotting import *
from matplotlib import rcParams
rcParams.update({'figure.autolayout': True})

def DP_sub (b,c,temp,RH):
	DP_func = (c*(log(RH/100)+ (b*temp)/(c+temp)))/(b-(log(RH/100)+ (b*temp)/(c+temp)))
	return DP_func;
b = 17.67
c = 243.5

# Location of experimental data files
data_dir = '../Experimental_Data/'

# Read in test times file
info = pd.read_csv('../Experimental_Data/Description_of_Experiments.csv', header=0, index_col=0)

# Skip files
skip_files = ['description_']

for f in os.listdir(data_dir):
	if f.endswith('.csv'):

		# Skip files with time information or reduced data files
		if any([substring in f.lower() for substring in skip_files]):
			continue

		# Strip test name from file name
		test_name = f[:-4]
		print 'Test ' + test_name

		# Load exp. data file
		data = pd.read_csv(data_dir + f, header=5, index_col=0)

		Temp_DewPoint_Chamber = np.zeros(len(data['Chamber_Temp']))
		Chamber_Time = np.zeros(len(data['Chamber_Temp']))
		start_of_chamber = info['Start of Chamber'][test_name]

		Temp_DewPoint_Sample = np.zeros(len(data['Sample_Temp']))
		Sample_Time = np.zeros(len(data['Sample_Temp']))
		start_of_sample = info['Start of Sample'][test_name]

		for i in range(len(data['Chamber_Temp'])):
			Chamber_Time[i] = info['Sample_Rate'][test_name]*(i-int(start_of_chamber))
			Temp_DewPoint_Chamber[i] = DP_sub(b,c,data['Chamber_Temp'][i],data['Chamber_Humidity'][i])

		k=1		
		for i in range(len(data['Sample_Temp'])):
			Sample_Time[i] = info['Sample_Rate'][test_name]*(i-int(start_of_sample))
			Temp_DewPoint_Sample[i] = DP_sub(b,c,data['Sample_Temp'][i],data['Sample_Humidity'][i])
			if Temp_DewPoint_Sample[i] > 37 and k == 1:
				j = Sample_Time[i]
				k = -1

		fig = figure()
		plot(Chamber_Time,Temp_DewPoint_Chamber,'rs',lw=2, label='Test Chamber Conditions')
		plot(Sample_Time,Temp_DewPoint_Sample,'bo',lw=2, label='Sample Penetration Conditions')
		axvline(x=j,linestyle='-',linewidth=2,color = '#000000')
		plt.text(j+5., 90, 'Temperature for skin burn reached at '+str(j)+' s', 
			 horizontalalignment='left',
		     verticalalignment='center')
		ax1 = gca()
		xlabel('Time (s)')
		ylabel('Dew Point Temperature ($^{\circ}$C)')
		xlim(0,info['End Time'][test_name])
		ylim(0,100)
		grid(True)
		ax = gca()
		legend(numpoints=1,loc=4)
		savefig('../Figures/' + test_name + '.pdf')
		close('all')

# output_file("steam.html", title="Steam Through Turnout Gear")
# p1 = figure()
# p1.line(T80_RH97_FC_Time, TDP_T80_RH97_FC, color='#1F78B4', legend='Test Chamber Conditions')
# p1.line(T80_RH97_FS_Time, TDP_T80_RH97_FS, color='#FB9A99', legend='Sample Penetration Conditions')
# p1.title = "Steam Penetration"
# p1.grid.grid_line_alpha=0.3
# p1.xaxis.axis_label = 'Time (sec)'
# p1.yaxis.axis_label = 'Dew Point Temperature (C)'
# show(VBox(p1))
