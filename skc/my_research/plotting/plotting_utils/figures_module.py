
import plotly.plotly as py
from plotly.graph_objs import *
import plotly.io as pio
import numpy as np



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
    f = a * np.exp(b*x*np.log(base))
    return f

def create_layout(title, xaxis, **y_axis):
    return Layout(
        title=title,
        xaxis=xaxis,
        **y_axis
    )


def dump_image(traces, layout, output_name):
    fig = Figure(data=traces, layout=layout)
    pio.write_image(fig, output_name, format='png')

'''

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