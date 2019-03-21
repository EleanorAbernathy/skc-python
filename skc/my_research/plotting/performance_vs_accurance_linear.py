from os.path import join, abspath, dirname
import sys
import numpy as np
from plotting_utils.results_parser import *
from plotting_utils.figures_module import *
from plotting_utils.color_scales import *
from plotting_utils.utils import *
from __init__ import build_complete_path, BASSIC_REFERENCE_RATE

def generate_performance_vs_accurance(directory, output_name=None, log =False):
    filesnames = search_files(directory, "*bassic_finder*.csv")

    n_items, times, distances = parse_several(filesnames) #[densities], {n : [times for n ]} , {n : [error for n]}
    traces_time = []
    traces_distance = []
    axis_x, axis_y1, axis_y2 = create_axis_group(
        "Algorithm's depth (n)", 
        "Tolerance (%1)", BLUES[2], 
        "Time (s)", GREENS[2], y1_args={'type' : 'log'} if log else {} ,
        y2_args={'type' : 'log'} if log else {}  )
    x_values = [int(n) for n in times.keys()]

    for dd, density in enumerate(n_items):
        times_d = [times_list[dd] for nn, times_list in times.iteritems()]
        distances_d = [distances_list[dd] for nn, distances_list in distances.iteritems()]

        traces_time.append(create_scatter(
            x=x_values,
            y=times_d,
            name="time d=%d"%(density),
            yaxis='y2',
            mode="lines+markers+text",
            textposition='top center',
            textfont=dict(
                color=GREENS[dd]
            ),
            text = ['']*(len(x_values) - 1) + ["d=%d"%density],
            color=GREENS[dd],
        ))
        traces_distance.append(create_scatter(
            x=x_values,
            y=distances_d,
            name="distance d=%d"%(density),
            mode="lines+markers+text",
            textposition='top center',
            textfont=dict(
                color=BLUES[dd]
            ),
            text = ["d=%d"%density],
            color=BLUES[dd],
            symbol='square'
        ))
    layout = create_layout("Time and error for bassic finder as n increases for several depths",
             xaxis=axis_x, yaxis=axis_y1, yaxis2=axis_y2, width=1000,
             legend={'x': 1.1,'xanchor': 'left', 'y': 1 }
             )

    traces = traces_time + traces_distance

    finish(directory, output_name, traces, layout)

def generate_performance_vs_accurance_rate(directory, pattern, plot_title, output_name=None):
    filesnames = search_files(directory, pattern)

    n_items, times, distances = parse_several(filesnames) #[densities], {n : [times for n ]} , {n : [error for n]}
    density = n_items[0]
    traces = []
    axis_x, axis_y1, axis_y2, axis_y3 = create_3_axis_group(
        "Algorithm's depth (n)", x_args = dict(domain=[0, 0.8]),
        y1_title="Tolerance (%1)", y1_color=BLUES[0], 
        y2_title="Time (s)", y2_color=GREENS[0],
        y3_title="Rate (s^-1)", y3_color=REDS[4], y3_args={'type' : 'log'})
    x_values = [int(n) for n in times.keys()]

    times_d = [times_list[0] for nn, times_list in times.iteritems()]
    distances_d = [distances_list[0] for nn, distances_list in distances.iteritems()]
    ref_rate_trace = get_rate_trace(x_values,rate_values=BASSIC_REFERENCE_RATE, name="rate reference", width=5)
    rate_trace = get_rate_trace(x_values, times_d, distances_d, color=REDS[4], name='obtained rate', width=3)
    traces.append(create_scatter(
        x=x_values,
        y=distances_d,
        name="distance d=%d"%(density),
        mode="lines+markers",
        color=BLUES[0],
        symbol='square'
    ))
    traces.append(create_scatter(
            x=x_values,
            y=times_d,
            name="time d=%d"%(density),
            yaxis='y2',
            mode="lines+markers",
            color=GREENS[0],
        ))
    traces.append(ref_rate_trace)
    traces.append(rate_trace)
    layout = create_layout(plot_title,
             xaxis=axis_x, yaxis=axis_y1, yaxis2=axis_y2, yaxis3=axis_y3, width=1000,
             legend={'x': 1.1,'xanchor': 'left', 'y': 1 }
             )

    finish(directory, output_name, traces, layout)


if __name__ == '__main__':

    directory = sys.argv[1]
    #generate_performance_vs_accurance(build_complete_path(directory), 'performance_vs_accurance.png')
    #generate_performance_vs_accurance(build_complete_path(directory), 'performance_vs_accurance_log.png', True)
    generate_performance_vs_accurance_rate(
        build_complete_path(directory), "*bassic_finder-su2-64429*",
        "Time and error with rate for bassic finder as n increases for density 64429", 
        "performance_vs_accurance_64429")
    generate_performance_vs_accurance_rate(
        build_complete_path(directory), "*bassic_finder-su2-9*",
        "Time and error with rate for bassic finder as n increases for density 9", 
        "performance_vs_accurance_9")
    generate_performance_vs_accurance_rate(
        build_complete_path(directory), "*bassic_finder-su2-243*",
        "Time and error with rate for bassic finder as n increases for density 243", 
        "performance_vs_accurance_243")
    generate_performance_vs_accurance_rate(
        build_complete_path(directory), "*bassic_finder-su2-2023*",
        "Time and error with rate for bassic finder as n increases for density 2023", 
        "performance_vs_accurance_2023")
    generate_performance_vs_accurance_rate(
        build_complete_path(directory), "*bassic_finder-su2-16176*",
        "Time and error with rate for bassic finder as n increases for density 16176", 
        "performance_vs_accurance_16176")