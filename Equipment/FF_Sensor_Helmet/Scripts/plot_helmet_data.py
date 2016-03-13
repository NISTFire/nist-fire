# -*- coding: utf-8 -*-
import time
import numpy as np
import pandas as pd
import argparse
from bokeh.plotting import *
from bokeh.plotting import figure,hplot,show,output_file,ColumnDataSource,output_server,curdoc
from bokeh.models import HoverTool, LinearAxis, Range1d, GlyphRenderer
from bokeh.client import push_session

# Parse command line arguments
parser = argparse.ArgumentParser()
parser.add_argument('test_name', help='Name for test to be displayed on plot')
parser.add_argument('data_file', help='Location of data file')
args = parser.parse_args()

# Bokeh plot options
TOOLS="pan,box_zoom,wheel_zoom,reset,resize,save,hover"
plt_width = 680
plt_height = 700
line_width = 4
title_size = '24pt'
axis_label_size = '21pt'
tick_label_size = '17pt'

output_server('FF_HF_T')

time_x = np.array([])
T_data = np.array([])
HF_data = np.array([])

p1 = figure(title=args.test_name+': FF Temperature', 
	x_axis_label = 'Time (s)', y_axis_label = 'Temperature (°C)', 
	tools=TOOLS, plot_width=plt_width, plot_height=plt_height)
p1.line(time_x, T_data, color="#dd0022", line_width=line_width)

p1.title_text_font_size = title_size
p1.xaxis.axis_label_text_font_size = axis_label_size
p1.yaxis.axis_label_text_font_size = axis_label_size
p1.xaxis.major_label_text_font_size = tick_label_size
p1.yaxis.major_label_text_font_size = tick_label_size
p1.yaxis.axis_label_standoff = 10
# p1.title_label_standoff = 20

p2 = figure(title=args.test_name+': FF Heat Flux', 
	x_axis_label = 'Time (s)', y_axis_label = 'Heat Flux (kW/m²)',
	tools=TOOLS, plot_width=plt_width, plot_height=plt_height)
p2.line(time_x, HF_data, color="#0000dd", line_width=line_width, line_dash = 'dashed') 

p2.title_text_font_size = title_size
p2.xaxis.axis_label_text_font_size = axis_label_size
p2.yaxis.axis_label_text_font_size = axis_label_size
p2.xaxis.major_label_text_font_size = tick_label_size
p2.yaxis.major_label_text_font_size = tick_label_size
p2.yaxis.axis_label_standoff = 10

p = hplot(p1, p2)

session = push_session(curdoc())

renderer = p1.select(dict(type=GlyphRenderer))
ds1 = renderer[0].data_source
renderer = p2.select(dict(type=GlyphRenderer))
ds2 = renderer[0].data_source

def update():
	new_data = pd.read_csv(args.data_file, index_col=0)
	time_x = new_data.iloc[-60: , 1]
	T_data = new_data.iloc[-60: , 4]
	HF_data = new_data.iloc[-60: , 5]
	# new_data = pd.read_csv('../Data/UL_Exp_5_031116_revised.csv')
	# time_x = new_data.loc[ : , 'Plot Time']
	# T_data = new_data.loc[ : , 'T old']
	# HF_data = new_data.loc[ : , 'HF new']
	# Update with latest HF and T readings
	ds1.data["x"] = time_x
	ds1.data["y"] = T_data
	ds1._dirty = True

	ds2.data["x"] = time_x
	ds2.data["y"] = HF_data
	ds2._dirty = True

curdoc().add_periodic_callback(update, 1000)

session.show()

session.loop_until_closed()



