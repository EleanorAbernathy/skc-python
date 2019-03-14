from os.path import join, abspath, dirname

from plotting_utils.results_parser import *
from plotting_utils.figures_module import create_scatter, create_layout, create_axis, dump_image
from plotting_utils.color_scales import *




def generate_distances_and_times(filesnames, output_name=None):
    x_values, times, distances = parse_several(filesnames)
    traces_times = []
    traces_distances = []
    axis_x, axis_y1, axis_y2 = _create_axis_group(
        "Group density (#items)", y1_color=BLUES[2],
        y1_title = "Error for each density (%1)", y2_color=GREENS[2],
        y2_title="Time for each density (s)" , y1_args={'type': 'log'}, 
        y2_args={'type': 'log'}
    )
    ns = times.keys()
    for nn in ns:
        traces_times.append(
            create_scatter(
                x=x_values,
                y=times[nn],
                mode='markers+lines+text',
                name="time for n=%s"%nn,
                symbol='square',
                text=['']*3 + ['n=%s'%nn],
                textposition='top center',
                color=GREENS[int(nn) - 1],
                yaxis='y2'
            )
        )
        traces_distances.append(
            create_scatter(
                x=x_values,
                y=distances[nn],
                mode='markers+lines+text',
                name="distance for n=%s"%nn,
                text=['n=%s'%nn],
                textposition='top center',
                color=BLUES[int(nn) - 1]
            )
        )
    layout = create_layout("Distace and time increasing group density", 
                        xaxis=axis_x, yaxis=axis_y1, yaxis2=axis_y2, width=1000,
                        legend={'x': 1.1,'xanchor': 'left', 'y': 1 }
                        )
    _finish('distance_and_time', output_name, traces_times+traces_distances, layout)

if __name__ == '__main__':

    directory = sys.argv[1]
    pattern = sys.argv[2]
    files = search_files(directory, pattern)
    generate_distances_and_times(files, 'times_and_distances_.png')