from os.path import join, abspath, dirname
import sys
from plotting_utils.results_parser import *
from plotting_utils.figures_module import create_scatter, create_layout, create_axis, dump_image
from plotting_utils.color_scales import *
from plotting_utils.utils import *


def get_rate_trace(x_values, y_values, color=REDS[0], width=4):

    trace = create_scatter(
        x=x_values,
        y=y_values,
        mode='markers+lines',
        color=color,
        name='theoretical',
        line=dict(color=color,
            width=width)
    )

    return trace


if __name__ == '__main__':
    x_values = range(1, 17)
    emp_y = [3, 9, 24, 54, 117, 243, 498, 1006, 2023, 4051, 8100, 16176, 32289, 64429, 128482, 256214]
    teo_y = [3**l for l in x_values]
    x = np.linspace(1, 16, num=20)
    f = create_pow_function(x, 1, 3)

    axis_x, axis_y1, _ = create_axis_group(
        "Operator max lenght", 
        "Group size (#items)", y1_args={'type': 'log'}, x_args = dict(range=[0, 17], dtick=1, tickangle=0))

    trace_teo = get_rate_trace(x_values, teo_y)
    trace_emp = create_scatter(
        x=x_values,
        y=emp_y,
        mode='markers+lines',
        name='empirical',
        color=GREENS[0]
        )

    traces = [trace_teo, trace_emp]
    layout = create_layout("Theorical and empirical group size", xaxis=axis_x, 
        yaxis=axis_y1, legend={'x': 1,'xanchor': 'left', 'y': 1 })


    finish('filepath', 'group_len', traces, layout)
    
