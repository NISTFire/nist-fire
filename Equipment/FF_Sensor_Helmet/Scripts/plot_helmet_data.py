# -*- coding: utf-8 -*-
import time
import numpy as np
import pandas as pd
from bokeh.plotting import figure,vplot,show,output_file,ColumnDataSource,output_server,cursession
from bokeh.models import HoverTool, LinearAxis, Range1d, GlyphRenderer

# Bokeh options
TOOLS="pan,box_zoom,wheel_zoom,reset,resize,save,hover"

output_server('FF_HF_T')

time_x = np.array([])
T_data = np.array([])
HF_data = np.array([])

p1 = figure(title='FF Helmet - Ambient Temp', x_axis_label = 'Time (s)', y_axis_label = 'Temperature (°C)',
	tools=TOOLS, plot_width=1000, plot_height=600)
p1.line(time_x, T_data, color="#dd0022", line_width = 3, legend='Amb T')

p2 = figure(title='FF Helmet - Heat Flux', x_axis_label = 'Time (s)', y_axis_label = 'Heat Flux (kW/m²)',
	tools=TOOLS, plot_width=1000, plot_height=600)
p2.line(time_x, HF_data, color="#0000dd", line_width = 3, line_dash = 'dashed', legend='Heat Flux')

p = vplot(p1, p2)

show(p)

renderer = p1.select(dict(type=GlyphRenderer))
ds1 = renderer[0].data_source

renderer = p2.select(dict(type=GlyphRenderer))
ds2 = renderer[0].data_source

while True:
	# Update with latest HF and T readings
	ds1.data["x"] = time_x
	ds1.data["y"] = T_data
	ds1._dirty = True
	cursession().store_objects(ds1)

	ds2.data["x"] = time_x
	ds2.data["y"] = HF_data
	ds2._dirty = True
	cursession().store_objects(ds2)

	time.sleep(1)

	new_data = pd.read_csv('../Data/output.csv', index_col=0)
	time_x = new_data.iloc[ : , 1]
	T_data = new_data.iloc[ : , 2]
	HF_data = new_data.iloc[ : , 3]