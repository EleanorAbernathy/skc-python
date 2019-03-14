import csv, sys
from os.path import abspath, dirname, join
from os import getcwd
import plotly.plotly as py
from plotly.graph_objs import *
import plotly.io as pio
import numpy as np

from plot_helloworld import create_scatter, create_pow_function, create_axis, parse_file, create_layout
from color_scales import *


filename = sys.argv[1]
filepath = join(getcwd(), filename)
data = parse_file(filepath)

axis_x = create_axis("Algorithm's depth (n)", showline=True)
axis_y1 = create_axis("Accurance", zeroline=False, type='log', color=BLUES[0])
axis_y2 = create_axis("Time (s)", side='right' , anchor='x',
        overlaying='y', zeroline=False, color=GREENS[0])

trace_accurance = create_scatter(
    x=data['x'],
    y=data['y2'],
    mode='markers+lines+text',
    name='accurance',
    color=BLUES[0],
    text=['hOla'],
    textposition='top center'
)
trace_time = create_scatter(
    x=data['x'],
    y=data['y1'],
    mode='markers+lines',
    name='time',
    color=GREENS[0],
    yaxis='y2'
)

layout = create_layout("Results kd-tree finder for largest group", xaxis=axis_x, yaxis=axis_y1, yaxis2=axis_y2)


traces = [trace_accurance, trace_time]

fig = Figure(data=traces, layout=layout)
pio.write_image(fig, filename.split('.csv')[0].split("/")[-1] + '.png')
