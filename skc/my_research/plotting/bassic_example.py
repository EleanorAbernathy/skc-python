from os.path import join, abspath, dirname
import sys
from plotting_utils.results_parser import *
from plotting_utils.figures_module import create_scatter, create_layout, create_axis, dump_image
from plotting_utils.color_scales import *
from plotting_utils.utils import *

def generate_basic_example(filepath, output_name=None, rate=False):
    results_data = parse_file(filepath)
    x_values = results_data['x']
    times = results_data['y1']
    distances = results_data['y2']


    axis_x, axis_y1, axis_y2 = create_axis_group(
        "Algorithm's depth (n)", 
        "Tolerance (%1)", BLUES[0], 
        "Time (s)", GREENS[0] , x_args = dict(domain=[0, 0.8]) if rate else {}, y2_args={'anchor' : 'x'} )

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
    traces = [trace_accurance, trace_time]
    y3axis = {}
    if rate:
        y3axis['yaxis3'] = create_axis("Rate (s^-1)", side='right',
            overlaying='y', zeroline=False, color=REDS[0], anchor='free', position= 0.9)
        traces.append(get_rate_trace(x_values, times, distances))

    layout = create_layout("Results bassic finder for largest group", xaxis=axis_x, 
        yaxis=axis_y1, yaxis2=axis_y2, width=1000, legend={'x': 1,'xanchor': 'left', 'y': 1 }, **y3axis)


    finish(filepath, output_name, traces, layout)


if __name__ == '__main__':

    filepath = sys.argv[1]

    generate_basic_example(filepath,'bassic_example_rate_5', True)
    generate_basic_example(filepath,'bassic_example_5')
    