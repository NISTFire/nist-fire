#!usr/bin/env python

"""
Generates synthetic pressure vs. time data and streams data to a plot
in a bokeh server. You should start bokeh-server on the local machine.

TODO: Replace synthetic data with data streaming from a .csv file from different sensors.
"""

import numpy as np
import bokeh.plotting as bk
from bokeh.objects import Glyph
import time

t = 0
time_x = np.array([0])
pres_y = np.array([20])

bk.output_server('Pressure')

bk.line(time_x, pres_y, color='#0000FF',
        tools='pan,wheel_zoom,box_zoom,reset,resize,crosshair,select,previewsave,embed',
        width=1200,height=300)
bk.xaxis()[0].axis_label = 'Time'
bk.yaxis()[0].axis_label = 'Pressure'

renderer = [r for r in bk.curplot().renderers if isinstance(r, Glyph)][0]
ds = renderer.data_source

while True:
    ds.data["x"] = time_x
    ds.data["y"] = pres_y
    ds._dirty = True
    bk.session().store_obj(ds)

    time.sleep(1)

    t = t + 1
    time_x = np.append(time_x,
                       time_x[t-1]+1)
    pres_y = np.append(pres_y,
                       pres_y[t-1] + np.random.random()*pres_y[t-1]*0.01)

