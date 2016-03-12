# -*- coding: utf-8 -*-
import time
import numpy as np
import pandas as pd
from bokeh.plotting import *
from bokeh.plotting import figure,hplot,show,output_file,ColumnDataSource,output_server,curdoc
from bokeh.models import HoverTool, LinearAxis, Range1d, GlyphRenderer
from bokeh.client import push_session
# from bokeh.embed import autoload_server

# Bokeh options
TOOLS="pan,box_zoom,wheel_zoom,reset,resize,save,hover"

output_server('FF_HF_T')

time_x = np.array([])
T_data = np.array([])
HF_data = np.array([])

p1 = figure(title='FF Helmet - Temperature', x_axis_label = 'Time (s)', y_axis_label = 'Temperature (°C)',
	tools=TOOLS, plot_width=700, plot_height=500)
p1.line(time_x, T_data, color="#dd0022", line_width = 4)
# legend='Amb T')
p1.xaxis.axis_label_text_font_size = '20pt'
p1.xaxis.major_label_text_font_size = '15pt'
p1.yaxis.major_label_text_font_size = '15pt'
p1.yaxis.axis_label_text_font_size = '20pt'
p1.yaxis.axis_label_standoff = 10
p1.title_text_font_size = '24pt'
# p1.title_label_standoff = 20

p2 = figure(title='FF Helmet - Heat Flux', x_axis_label = 'Time (s)', y_axis_label = 'Heat Flux (kW/m²)',
	tools=TOOLS, plot_width=700, plot_height=500)
p2.line(time_x, HF_data, color="#0000dd", line_width = 4, line_dash = 'dashed') 
#legend='Heat Flux')

p2.xaxis.axis_label_text_font_size = '20pt'
p2.xaxis.major_label_text_font_size = '15pt'
p2.yaxis.major_label_text_font_size = '15pt'
p2.yaxis.axis_label_text_font_size = '20pt'
p2.yaxis.axis_label_standoff = 10
p2.title_text_font_size = '24pt'

p = hplot(p1, p2)

# show(p)
session = push_session(curdoc())
# autoload_server(p, session_id=session.id)

renderer = p1.select(dict(type=GlyphRenderer))
ds1 = renderer[0].data_source

renderer = p2.select(dict(type=GlyphRenderer))
ds2 = renderer[0].data_source

def update():
	new_data = pd.read_csv('../Data/UL_Exp_19_031216_arduino.csv')
	time_x = new_data.iloc[ : , 1]
	T_data = new_data.iloc[ : , 4]
	HF_data = new_data.iloc[ : , 5]
	# new_data = pd.read_csv('../Data/UL_Exp_5_031116_revised.csv')
	# time_x = new_data.loc[ : , 'Plot Time']
	# T_data = new_data.loc[ : , 'T old']
	# HF_data = new_data.loc[ : , 'HF new']
	# Update with latest HF and T readings
	ds1.data["x"] = time_x
	ds1.data["y"] = T_data
	ds1._dirty = True
	# cursession().store_objects(ds1)
	# push_session(ds1)

	ds2.data["x"] = time_x
	ds2.data["y"] = HF_data
	ds2._dirty = True
	# push_session(ds2)
	# cursession().store_objects(ds2)

	# time.sleep(1)

curdoc().add_periodic_callback(update, 1000)

session.show()

session.loop_until_closed()



