
from os.path import join, abspath, dirname
import sys
from plotting_utils.results_parser import *
from plotting_utils.figures_module import create_scatter, create_layout
from plotting_utils.color_scales import *
from plotting_utils.utils import *


def generate_random_vs_shorter_times(directory, output_name=None):
    #directory, output_name=None, yaxis_title, key_results, legend_text, plot_title, color1, color2
    _random_vs_shorter_stuff(directory, output_name, 
        "Time (s) for each depth", 'times', 'time', 
        "Time for several depths random vs shorter", REDS, BLUES )

def generate_random_vs_shorter_distances(directory, output_name=None):
    #directory, output_name=None, yaxis_title, key_results, legend_text, plot_title, color1, color2
    _random_vs_shorter_stuff(directory, output_name, 
        "Error (%1) for each depth", 'distances', 'error', 
        "Errors for several depths random vs shorter", PINKS, GREENS )


def _random_vs_shorter_stuff(directory, output_name, yaxis_title, key_results, legend_text, plot_title, color1, color2):
    random_files = search_files(directory, "*finder-random-kdtree*.csv")
    shorter_files = search_files(directory, "*finder-kdtree*.csv")
    results = several_random_shorter_parse(random_files, shorter_files)
    x_values = results['x']
    axis_x, axis_y1, _ = _create_axis_group(
        "Group density (#items)", 
        yaxis_title, y1_args={'type': 'log'})

    traces_shorter = []
    traces_random = []
    for nn, values in results[key_results + '_random'].items():
        traces_random.append(
            create_scatter(
                x=x_values,
                y=values,
                mode='markers+lines',
                name='random %s n=%s'%(legend_text, nn),
                color=color1[int(nn)-1],
                symbol='square'
            )
        )
    for nn, values in results[key_results + '_shorter'].items():
        traces_shorter.append(
            create_scatter(
                x=x_values,
                y=values,
                text=['n=%s'%nn],
                textposition='top center',
                mode='text+markers+lines',
                name='shorter %s n=%s'%(legend_text, nn),
                color=color2[int(nn)-1],
                symbol='circle'
            )
        )
    layout = create_layout(plot_title, 
                            xaxis=axis_x, yaxis=axis_y1, width=1000,
                            legend={'x': 1.1,'xanchor': 'left', 'y': 1 }
                            )
    traces = traces_random + traces_shorter

    _finish(directory, output_name, traces, layout)



if __name__ == '__main__':

    directory = sys.argv[1]

	generate_random_vs_shorter_times(directory, output_name='random_vs_shorter_times.png')
	generate_random_vs_shorter_distances(directory, output_name='random_vs_shorter_distances.png')
