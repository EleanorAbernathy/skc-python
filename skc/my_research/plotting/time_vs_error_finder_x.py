from os.path import join, abspath, dirname
import sys
import numpy as np
from plotting_utils.results_parser import *
from plotting_utils.figures_module import create_scatter, create_layout, create_axis, dump_image
from plotting_utils.color_scales import *
from plotting_utils.utils import *
from __init__ import build_complete_path

def generate_time_vs_error(directory, output_name=None):

    filesnames = search_files(directory, "*results*.csv")
    all_results = parse_several_error_time(filesnames)
    #random_results = all_results['random'] #[n_items] , {N: [times]}, {N: [distances]}
    #bassic_results = all_results['bassic']
    tree_results = all_results['tree']
    axis_x, axis_y1, _ = create_axis_group(
        "Time (s)", 
        "Error (%1)", y1_args={'type':'log'}, x_args={'type': 'log', 'range' : [np.log10(0.02), np.log10(150)]})


    densities = tree_results[0]
    times = tree_results[1]
    distances = tree_results[2]
    
    traces_tree = []
    for index in range(len(densities)):
        density = densities[index]
        x_values = [tim[index] for ene, tim in times.iteritems()]
        y_values = [err[index] for ene, err in distances.iteritems()]
        traces_tree.append(create_scatter(
            x=x_values,
            y=y_values,
            name="tree d=%d"%( density),
            mode="lines+markers+text",
            text=['n=%s'%(nn+1) for nn in range(len(x_values))],
            textposition='top center',
            textfont=dict(
                color=GREENS[index]
            ),
            color=GREENS[index],
            symbol='star',
            yaxis='y1'

        ))
    traces = traces_tree
    layout = create_layout("Compare error and time for tree searcher as n increases for several densities", 
        xaxis=axis_x, yaxis=axis_y1, width=1000,
        legend={'x': 1.1,'xanchor': 'left', 'y': 1 }
    )
    #traces = traces_random + traces_bassic + traces_tree

    output_name = "new_only_tree"
    finish(directory, output_name, traces, layout)

if __name__ == '__main__':

    directory = sys.argv[1]
    generate_time_vs_error(build_complete_path(directory))