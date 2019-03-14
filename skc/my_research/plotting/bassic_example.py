from os.path import join, abspath, dirname
import sys
from plotting_utils.results_parser import *
from plotting_utils.figures_module import create_scatter, create_layout, create_axis, dump_image
from plotting_utils.color_scales import *
from plotting_utils.utils import *

def generate_basic_example(filepath, output_name=None):
    results_data = parse_file(filepath)
    x_values = results_data['x']
    times = results_data['y1']
    distances = results_data['y2']


    axis_x, axis_y1, axis_y2 = create_axis_group(
        "Algorithm's depth (n)", 
        "Tolerance (%1)", BLUES[0], 
        "Time (s)", GREENS[0]  )

    trace_accurance = create_scatter(
        x=x_values,
        y=distances,
        mode='markers+lines',
        name='tolerance',
        color=BLUES[0]
    )

    trace_time = create_scatter(
        x=x_values,
        y=times,
        mode='markers+lines',
        name='time',
        color=GREENS[0],
        yaxis='y2'
    )

    layout = create_layout("Results kd-tree finder for largest group", xaxis=axis_x, 
        yaxis=axis_y1, yaxis2=axis_y2, legend={'x': 1.1,'xanchor': 'left', 'y': 1 })

    traces = [trace_accurance, trace_time]

    _finish(filepath, output_name, traces, layout)


if __name__ == '__main__':

    filepath = sys.argv[1]

    generate_basic_example(filepath)