import csv, sys
from os.path import abspath, dirname, join
from os import getcwd
import plotly.plotly as py
from plotly.graph_objs import *
import plotly.io as pio
import numpy as np


def random_vs_shorter_parse(random_file, shorter_file):
    n_items = random_file.split("su2-")[-1].split("_")[0]
    n_items = int(n_items)

    random_data = parse_file(random_file)
    shorter_data = parse_file(shorter_file)

    return n_items, random_data, shorter_data

def several_random_shorter_parse(random_files, shorter_files):

    for rfile, sfile



def parse_file(filepath):
    with open(filepath, 'r') as f:
        reader = csv.reader(f, delimiter=';')
        next(reader, None)
        all_data = [l for l in reader]

    x_values = [line[0] for line in all_data]
    y1_values = [line[2] for line in all_data]
    y2_values = [line[4] for line in all_data]

    return {"x" : x_values, "y1" : y1_values, "y2": y2_values}

def create_scatter(x, y, name, mode='lines', color='rgb(220, 20, 60)', symbol='circle', **kwargs):
    return Scatter(
        x=x,
        y=y,
        mode=mode,
        name=name,
        marker=dict(
            color=color,
            symbol=symbol
        ),
        **kwargs
    )

def create_axis(title, size=18, color='#7f7f7f', side='left', **kwargs):
    return dict(
        title=title,
        titlefont=dict(
            #family='Courier New, monospace',
            size=size,
            color=color),
        side=side,
        **kwargs
        )

def create_pow_function(x, a, base, b=1):
    assert b > 0
    f = a * np.exp(b*x*np.log(b))
    return f

def create_layout(title, xaxis, **y_axis):
    return Layout(
        title=title,
        xaxis=xaxis,
        **y_axis
    )

filename = sys.argv[1]
filepath = join(getcwd(), filename)
data = parse_file(filepath)


x = np.linspace(0, 5, num=100)
f = create_pow_function(x, 0.33, 3)


trace1 = create_scatter(
    x=x,
    y=f,
    name='1/30 exp(x)',
    color='rgb(220, 20, 60)'
)
trace2 = create_scatter(
    x=data['x'],
    y=data['y1'],
    mode='markers',
    name='data',
    color='rgb(22, 20, 60)'
)



'''


layout = Layout(
    title='Plot Title',
    xaxis=dict(
        title='n',
        titlefont=dict(
            family='Courier New, monospace',
            size=18,
            color='#7f7f7f'
        )
    ),
    yaxis=dict(
        title='time(s)',
        titlefont=dict(
            family='Courier New, monospace',
            size=18,
            color='#7f7f7f'
        )
    )
)

data = [trace1, trace2]

fig = Figure(data=data, layout=layout)
pio.write_image(fig, 'exp.png')


yaxis2=dict(
    title='yaxis2 title',
    titlefont=dict(
        color='rgb(148, 103, 189)'
    ),
    tickfont=dict(
        color='rgb(148, 103, 189)'
    ),
    overlaying='y',
    side='right'
)
'''