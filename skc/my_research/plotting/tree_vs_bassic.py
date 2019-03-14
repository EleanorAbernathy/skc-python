from os.path import join, abspath, dirname
import sys
from plotting_utils.results_parser import *
from plotting_utils.figures_module import create_scatter, create_layout
from plotting_utils.color_scales import *
from plotting_utils.utils import *

def generate_tree_vs_bassic(tree_file, bassic_file, output_name=None):
    results_tree = parse_file(tree_file)
    results_bassic = parse_file(bassic_file)

    x_values = results_tree['x'] #it has 5, bassic only 4
    times_tree = results_tree['y1']
    times_bassic = results_bassic['y1']
    distances_tree = results_tree['y2']
    distances_bassic = results_bassic['y2']

    axis_x, axis_y1, axis_y2 = _create_axis_group(
        "Algorithm's depth (n)", 
        "Tolerance (%1)", BLUES[0], 
        "Time (s)", GREENS[0]  )

    trace_accurance_bassic = create_scatter(
        x=x_values,
        y=distances_bassic,
        mode='markers+lines',
        name='bassic tolerance',
        color=BLUES[0]
    )

    trace_time_bassic = create_scatter(
        x=x_values,
        y=times_bassic,
        mode='markers+lines',
        name='bassic time',
        color=GREENS[0],
        yaxis='y2'
    )
    trace_accurance_tree = create_scatter(
        x=x_values,
        y=distances_tree,
        mode='markers+lines',
        name='tree tolerance',
        color=BLUES[2],
        symbol='square'
    )

    trace_time_tree = create_scatter(
        x=x_values,
        y=times_tree,
        mode='markers+lines',
        name='tree time',
        color=GREENS[2],
        yaxis='y2',
        symbol='square'
    )
    layout = create_layout("Results kd-tree finder vs bassic (largest group)", xaxis=axis_x, 
                yaxis=axis_y1, yaxis2=axis_y2, legend={'x': 1.1,'xanchor': 'left', 'y': 1 })
    traces = [trace_accurance_bassic, trace_time_bassic, trace_accurance_tree, trace_time_tree]

    _finish(tree_file, output_name, traces, layout)

if __name__ == '__main__':

    tree_file = sys.argv[1]
    bassic_file = sys.argv[2]

    generate_tree_vs_bassic(tree_file, bassic_file)