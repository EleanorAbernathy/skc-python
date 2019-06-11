from os.path import join, abspath, dirname
import sys
import numpy as np
from plotting_utils.results_parser import parse_file, search_files
from plotting_utils.figures_module import create_scatter, create_layout, create_axis, dump_image
from plotting_utils.color_scales import BLUES, REDS, GREENS
from plotting_utils.utils import create_scatter, create_axis_group, create_layout, finish
from __init__ import build_complete_path

def get_values(errors_dict):
    x_values = []
    y_values = []
    for n, errors in errors_dict.iteritems():
        x_values.extend(errors)
        y_values.extend([int(n)] * len(errors))
    return x_values, y_values

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

def generate_error_from_n(errors_dict, errors_dict2={}):
    # n = ln( ln(eph * 32 )/ln(0.14 * 32 ) / 0.405 
    y_values, x_values = get_values(errors_dict)
    y_values_2, x_values_2 = get_values(errors_dict2)

    axis_x, axis_y1, _ = create_axis_group(
        "Algorithm's depth (n)", 
        "Error reached (%1)", y1_args={'type': 'log'}, y1_color=BLUES[2], x_args={'rangemode':'nonnegative'})

    trace = dots_trace(x_values, y_values, name="error large group",color=BLUES[2])
    trace_2 = dots_trace(x_values_2, y_values_2, name="error other groups",color=GREENS[2])
    x_lin = np.linspace(1,6,100)
    import pdb;pdb.set_trace()
    trace_real = create_scatter(
        x=x_lin,
        y=0.0325*np.power(0.014 * 32, np.power(1.5, x_lin)),
        color=REDS[2],
        yaxis='y1',
        mode="lines",
        name="theorical error(n) 0.014"
    )
    trace_real2 = create_scatter(
        x=x_lin,
        y=0.0325*(0.009 * 32)**((1.5)**x_lin),
        color=REDS[6],
        yaxis='y1',
        mode="lines",
        name="theorical error(n) 0.009"
    )
    layout = create_layout("Level of recursion required for given errors", 
        xaxis=axis_x, yaxis=axis_y1, width=1000,
        legend={'x': 1.1,'xanchor': 'left', 'y': 1 }
    )

    output_name = "error_from_n"
    finish("", output_name, [
        trace, trace_2, 
        trace_real, trace_real2
        ], layout)

def generate_n_from_error(errors_dict, errors_dict2={}):

    # n = ln( ln(eph * 32 )/ln(0.14 * 32 ) / 0.405 
    x_values, y_values = get_values(errors_dict)
    x_values_2, y_values_2 = get_values(errors_dict2)

    axis_x, axis_y1, _ = create_axis_group(
        "Error reached (%1)", 
        "Algorithm's depth (n)", x_args={'type': 'log'}, y1_color=BLUES[2], y1_args={'rangemode':'nonnegative'})

    trace = dots_trace(x_values, y_values, name="n level large group",color=BLUES[2])
    trace_2 = dots_trace(x_values_2, y_values_2, name="n level other groups",color=GREENS[2])
    x_lin = np.linspace(5e-8,0.05,500)

    trace_real = create_scatter(
        x=x_lin,
        y=np.ceil(np.log( np.log(x_lin * 32 )/np.log(0.014 * 32 ) )/ 0.405),
        color=REDS[2],
        yaxis='y1',
        mode="lines",
        name="theorical n(error) 0.014"
    )
    trace_real2 = create_scatter(
        x=x_lin,
        y=np.ceil(np.log( np.log(x_lin * 32 )/np.log(0.009 * 32 ) )/ 0.405),
        color=REDS[6],
        yaxis='y1',
        mode="lines",
        name="theorical n(error) 0.009"
    )
    layout = create_layout("Error reached for depth levels", 
        xaxis=axis_x, yaxis=axis_y1, width=1000,
        legend={'x': 1.1,'xanchor': 'left', 'y': 1 }
    )

    output_name = "n_from_error"
    finish("", output_name, [trace, trace_2, trace_real, trace_real2], layout)


def create_dict(files):
    errors_dict = {}
    for file in files:
        results = parse_file(file)
        for ii in range(len(results["x"])):
            n = str(results["x"][ii])
            error = results["y2"][ii]
            if n in errors_dict:
                errors_dict[n].append(error)
            else:
                errors_dict[n] = [error]
    return errors_dict

if __name__ == '__main__':
    directory = sys.argv[1]
    files = search_files(directory, "*finder_fowler*.csv")
    files.extend(search_files(directory, "*kdtree-su2-256214*"))
    errors_dict = create_dict(files)
    files2 = search_files(directory, "*bassic_finder-su2-*")
    errors_dict2 = create_dict(files2)
    #generate_n_from_error(errors_dict, errors_dict2)


    ''' Error en funcion de n '''
    generate_error_from_n(errors_dict, errors_dict2)
