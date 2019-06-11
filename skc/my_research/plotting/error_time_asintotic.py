from os.path import join, abspath, dirname
import sys
import numpy as np
from plotting_utils.results_parser import parse_file, search_files, parse_several
from plotting_utils.figures_module import create_scatter, create_layout, create_axis, dump_image
from plotting_utils.color_scales import BLUES, REDS, GREENS
from plotting_utils.utils import create_scatter, create_axis_group, create_layout, finish
from __init__ import build_complete_path



def dots_trace(x_values, y_values, name, color):
    return create_scatter(
        x=x_values,
        y=y_values,
        name=name,
        mode="markers",
        #text=['n=%s'%(nn+1) for nn in range(len(x_values))],
        color=color,
        yaxis='y1'
    )

def generate_time_from_error(errors, times, errors_2, times_2):
    # n = ln( ln(eph * 32 )/ln(0.14 * 32 ) / 0.405 
    y_values, x_values = times, errors
    y_values_2, x_values_2 = times_2, errors_2

    axis_x, axis_y1, _ = create_axis_group(
        "Error reached (%1)",
        "Time required (s)",
        x_args={'type': 'log'}, y1_color=BLUES[2], y1_args={'type': 'log', 'rangemode':'nonnegative'})

    trace = dots_trace(x_values, y_values, name="error large group",color=BLUES[2])
    trace_2 = dots_trace(x_values_2, y_values_2, name="error other groups",color=GREENS[2])
    x_lin = np.linspace(1e-7,1,100)

    trace_real = create_scatter(
        x=x_lin,
        y=np.log(1/x_lin)**2.71,
        color=REDS[2],
        yaxis='y1',
        mode="lines",
        name="theorical time(error)"
    )
    trace_real2 = create_scatter(
        x=x_lin,
        y=0.003*np.log(1/x_lin)**2.71,
        color=REDS[6],
        yaxis='y1',
        mode="lines",
        name="theorical time(error) x0.003"
    )
    layout = create_layout("Time required for reached errors", 
        xaxis=axis_x, yaxis=axis_y1, width=1000,
        legend={'x': 1.1,'xanchor': 'left', 'y': 1 }
    )

    output_name = "time_required_give_error"
    finish("", output_name, [
        trace, trace_2, 
        trace_real, trace_real2
        ], layout)


def get_values(files):
    x_values = []
    y_values = []
    for file in files:
        results = parse_file(file)
        x_values.extend(results["y2"])
        y_values.extend(results["y1"])
    return x_values, y_values

if __name__ == '__main__':
    directory = sys.argv[1]
    files = search_files(directory, "*finder_fowler*.csv")
    files.extend(search_files(directory, "*kdtree-su2-256214*"))

    files2 = search_files(directory, "*bassic_finder-su2-*")
    errors, times = get_values(files)
    errors2, times2 = get_values(files2)

    files2 = search_files(directory, "*bassic_finder-su2-*")
    #errors_dict2 = create_dict(files2)
    generate_time_from_error(errors, times, errors2, times2)
