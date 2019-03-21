from os.path import join, abspath, dirname
import sys
import numpy as np
from plotting_utils.results_parser import *
from plotting_utils.figures_module import create_scatter, create_layout, create_axis, dump_image
from plotting_utils.color_scales import *
from plotting_utils.utils import *
from plotting import build_complete_path

def generate_time_vs_error(directory, output_name=None,):
    def _complete_stuff(results, traces, sk_type, color_scale, symbol, text=False, pos=None):
        densities, times, distances = results
        studing_densities = densities if pos == None else densities[pos:pos+1]
        for jj, density in enumerate(studing_densities):
            index = jj if pos == None else p
            x_values = [t[index] for ene, t in times.iteritems()]
            y_values = [err[index] for ene, err in distances.iteritems()]
            traces.append(create_scatter(
                x=x_values,
                y=y_values,
                name="%s d=%d"%(sk_type, density),
                mode="lines+markers+text",
                text=['n=%s'%(nn+1) for nn in range(len(x_values))] if text else [],
                textposition='top center',
                textfont=dict(
                    color=color_scale[index]
                ),
                color=color_scale[index],
                symbol=symbol

            ))

    filesnames = search_files(directory, "*results*.csv")
    all_results = parse_several_error_time(filesnames)
    random_results = all_results['random'] #[n_items] , {N: [times]}, {N: [distances]}
    bassic_results = all_results['bassic']
    tree_results = all_results['tree']
    axis_x, axis_y1, _ = create_axis_group(
        "Time (s)", 
        "Error (%1)", y1_args={'type':'log'}, x_args={'type': 'log', 'range' : [np.log10(0.001), np.log10(150)]})
    
    for p in range(len(random_results[0])):
        traces_random = []
        traces_tree = []
        traces_bassic = []
        density = random_results[0][p]
        output_name = "time_error_only_%s"%density
        _complete_stuff(random_results, traces_random, "random", REDS, "circle", True, pos=p)
        _complete_stuff(bassic_results, traces_bassic, "bassic", BLUES, "square", pos=p)
        _complete_stuff(tree_results, traces_tree, "tree", GREENS, "star", pos=p)
        layout = create_layout("Compare error and time for several searchers as n increases for density = %s"%density, 
            xaxis=axis_x, yaxis=axis_y1, width=1000,
            legend={'x': 1.1,'xanchor': 'left', 'y': 1 }
        )
        traces = traces_random + traces_bassic + traces_tree

        finish(directory, output_name, traces, layout)

if __name__ == '__main__':

    directory = sys.argv[1]
    generate_time_vs_error(build_complete_path(directory))