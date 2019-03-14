from os.path import join, abspath, dirname
import sys
from plotting_utils.results_parser import *
from plotting_utils.figures_module import create_scatter, create_layout, create_axis, dump_image
from plotting_utils.color_scales import *


def generate_time_vs_error(directory, output_name=None):
    def _complete_stuff(results, traces, sk_type, color_scale, symbol):
        densities, times, distances = results
        for jj, density in enumerate(densities):
            x_values = [t[jj] for ene, t in times.iteritems()]
            y_values = [err[jj] for ene, err in distances.iteritems()]
            print x_values, y_values
            traces.append(create_scatter(
                x=x_values,
                y=y_values,
                name="%s d=%d"%(sk_type, density),
                mode="lines+markers+text",
                text=['n=%s'%(nn+1) for nn in range(len(x_values))],
                textposition='top center',
                #textfont=dict(
                #    color=color_scale[jj]
                #),
                color=color_scale[jj]

            ))

    filesnames = search_files(directory, "*results*.csv")
    all_results = parse_several_error_time(filesnames)
    random_results = all_results['random'] #[n_items] , {N: [times]}, {N: [distances]}
    bassic_results = all_results['bassic']
    tree_results = all_results['tree']
    axis_x, axis_y1, _ = _create_axis_group(
        "Time (s)", 
        "Error (%1)")
    traces_random = []
    traces_tree = []
    traces_bassic = []
    
    _complete_stuff(random_results, traces_random, "random", PINKS, "circle")
    _complete_stuff(bassic_results, traces_bassic, "bassic", BLUES, "square")
    _complete_stuff(tree_results, traces_tree, "tree", GREENS, "star")
    layout = create_layout("Compare error and time for several searchers as n increases for several depths", 
        xaxis=axis_x, yaxis=axis_y1, width=1000,
        legend={'x': 1.1,'xanchor': 'left', 'y': 1 }
    )
    traces = traces_random + traces_bassic + traces_tree
    print traces
    _finish(directory, output_name, traces, layout)

if __name__ == '__main__':

    directory = sys.argv[1]
    generate_time_vs_error(directory)