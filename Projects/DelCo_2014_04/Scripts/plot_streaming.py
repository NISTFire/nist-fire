#!usr/bin/env python

"""
Reads a constantly updating .csv file and streams data to a plot
in a bokeh server. You should start bokeh-server on the local machine.
The plots can be accessed at http://localhost:5006/bokeh/
"""

import numpy as np
import bokeh.plotting as bk
from bokeh.objects import Glyph
import time

#  =================
#  = User Settings =
#  =================

data_file = '../Experimental_Data/test_data.csv'

#  ============
#  = Plotting =
#  ============

data = np.genfromtxt(data_file, delimiter=',', names=True)
x = data['Time']
y = data['TC_A1_0p03_BC']

bk.output_server('Plots')

bk.line(x, y, color='#0000FF',
        tools='pan,wheel_zoom,box_zoom,reset,resize,crosshair,select,previewsave,embed',
        width=1200,height=300)
bk.xaxis()[0].axis_label = 'Time'
bk.yaxis()[0].axis_label = 'Temperature (C)'

renderer = [r for r in bk.curplot().renderers if isinstance(r, Glyph)][0]
ds = renderer.data_source

while True:
    data = np.genfromtxt(data_file, delimiter=',', names=True)
    ds.data['x'] = data['Time']
    ds.data['y'] = data['TC_A1_0p03_BC']

    ds._dirty = True
    bk.session().store_obj(ds)

    time.sleep(1)
