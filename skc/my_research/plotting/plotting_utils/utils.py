from os.path import join, abspath, dirname

from figures_module import *
from color_scales import *

def finish(original, output_name, traces, layout):
    if not output_name:
        output_name = build_output_name(original)
    else:
        output_name = build_output_name(output_name)
    dump_image(traces, layout, output_name)

def create_axis_group(x_title, y1_title, y1_color=None, y2_title=None, y2_color=None, y2_position='right', x_args = {}, y1_args={}, y2_args={}):

    axis_x = create_axis(x_title, showline=True, **x_args)
    if y1_color:
        y1_args['color'] = y1_color
    if y2_color:
        y2_args['color'] = y2_color
    axis_y1 = create_axis(y1_title, zeroline=False, **y1_args)
    axis_y2 = None
    if y2_title:
        axis_y2 = create_axis(y2_title, side=y2_position,
            overlaying='y', zeroline=False, **y2_args)

    return axis_x, axis_y1, axis_y2


def create_3_axis_group(x_title, x_args = {}, 
                y1_title=None, y1_color=None, y1_args={}, 
                y2_title=None, y2_color=None, y2_args={},
                y3_title=None, y3_color=None, y3_args={}):
    axis_x, axis_y1, axis_y2 = create_axis_group(
        x_title, y1_title, y1_color,
        y2_title, y2_color, 'right', x_args, y1_args, y2_args)
    axis_y3 = create_axis(y3_title, side='right',
            overlaying='y', zeroline=False, color=y3_color, anchor='free', position= 0.9, **y3_args)

    return axis_x, axis_y1, axis_y2, axis_y3

def get_rate_trace(x_values, times=None, distances=None, color=REDS[0], rate_values=[], axis='y3', name='rate', width=4):
    assert rate_values or (times and distances)
    if not rate_values:
        rate_values = [float(1/(time*10*error)) for time, error in zip(times, distances)]
    trace = create_scatter(
        x=x_values,
        y=rate_values,
        mode='markers+lines',
        color=color,
        name=name,
        line=dict(color=color,
            width=width),
        yaxis=axis
    )

    return trace


def build_output_name(filepath):
    return join(dirname(abspath(__file__)), "../output/", filepath.split('.csv')[0].split("/")[-1].split("-results_")[-1]+ ".png")