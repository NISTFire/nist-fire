from __future__ import division
import os
import numpy as np
import pandas as pd
from bokeh.plotting import figure,show,output_file,vplot,ColumnDataSource
from bokeh.models import HoverTool
from collections import OrderedDict
from bokeh.plotting import figure

#  =================
#  = User Settings =
#  =================

# Choose Test Number

current_test = 'Test_64_West_81215'

# Location of experimental data files
data_dir = '../Experimental_Data/'

# Location of file with timing information
all_times_file = '../Experimental_Data/All_Times.csv'

# Location of scaling conversion files
scaling_file_west = '../DAQ_Files/West_DelCo_DAQ_Channel_List.csv'
scaling_file_east = '../DAQ_Files/East_DelCo_DAQ_Channel_List.csv'

# Location of test description file
info_file = '../Experimental_Data/Description_of_Experiments.csv'

# Time averaging window for data smoothing
data_time_averaging_window = 5

# Duration of pre-test time for bi-directional probes and heat flux gauges (s)
pre_test_time = 60

# Load exp. timings and description file
all_times = pd.read_csv(all_times_file)
all_times = all_times.set_index('Time')
info = pd.read_csv(info_file, index_col=3)

# Files to skip
skip_files = ['_times', '_reduced', 'description_','zero_','_rh']

colors=['#cc5500', '#228b22','#f4a460','#4c177d','firebrick', 'mediumblue', 'darkgreen', 'cadetblue', 'indigo', 'crimson', 'gold']

# Bokeh options
TOOLS="pan,box_zoom,wheel_zoom,reset,resize,save,hover"

for f in os.listdir(data_dir):
	if f.endswith('.csv'):

		# Skip files with time information or reduced data files
		if any([substring in f.lower() for substring in skip_files]):
		    continue

		# Strip test name from file name
		test_name = f[:-4]
		print 'Test ' + test_name

		# Option to specify which test is run
		if test_name != current_test:
		  continue

		# Load exp. scaling file
		if 'West' in test_name:
		    channel_list_file = scaling_file_west
		elif 'East' in test_name:
		    channel_list_file = scaling_file_east

		channel_list = pd.read_csv(channel_list_file)
		channel_list = channel_list.set_index('Channel Name')
		channel_groups = channel_list.groupby('Group Name')

		# Read in test times to offset plots
		start_of_test = info['Start of Test'][test_name]
		end_of_test = info['End of Test'][test_name]

		# Load exp. data file
		data = pd.read_csv(data_dir + f)
		data = data.set_index('TimeStamp(s)')

		# Offset data time to start of test
		data['Time'] = data['Time'].values - start_of_test

		# Smooth all data channels with specified data_time_averaging_window
		data_copy = data.drop('Time', axis=1)
		data_copy = pd.rolling_mean(data_copy, data_time_averaging_window, center=True)
		data_copy.insert(0, 'Time', data['Time'])
		data_copy = data_copy.dropna()
		data = data_copy

		output_file(test_name +'.html')

		for group in channel_groups.groups:
			
			# Skip excluded groups listed in test description file
			if any([substring in group for substring in info['Excluded Groups'][test_name].split('|')]):
				continue
			if 'TC A17' == group:
				p=figure(tools=TOOLS, title = group, x_axis_label = 'Time (s)', y_axis_label = 'Temperature (C)')
				i=0
				for channel in channel_groups.get_group(group).index.values:
					# Skip excluded channels listed in test description file
					if any([substring in channel for substring in info['Excluded Channels'][test_name].split('|')]):
						continue
					# Scale channel and set plot options depending on quantity
					current_channel_data = data[channel_list['Device Name'][channel]]
					calibration_slope = float(channel_list['Calibration Slope'][channel])
					calibration_intercept = float(channel_list['Calibration Intercept'][channel])
					x=data['Time']
					y=current_channel_data
					channel_label= np.tile(channel[:-5], [len(x),1])
					source = ColumnDataSource({'channels': channel_label})
					p.line(x, y, source=source,legend=channel,line_width=4,color=colors[i])
					hover = p.select(dict(type=HoverTool))
					hover.tooltips = [('Time','$x{000}'), ('Temperature','$y{000}'),('Channel','@channels')]
					p.legend.orientation = "top_left"
					i=i+1
				show(p)

