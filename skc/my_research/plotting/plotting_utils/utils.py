from os.path import join, abspath, dirname

from figures_module import create_axis, dump_image


def _finish(original, output_name, traces, layout):
    if not output_name:
        output_name = _build_output_name(original)
    else:
        output_name = _build_output_name(output_name)
    dump_image(traces, layout, output_name)

def _create_axis_group(x_title, y1_title, y1_color=None, y2_title=None, y2_color=None, y2_position='right', x_args = {}, y1_args={}, y2_args={}):

    axis_x = create_axis(x_title, showline=True, **x_args)
    if y1_color:
        y1_args['color'] = y1_color
    if y2_color:
        y2_args['color'] = y2_color
    axis_y1 = create_axis(y1_title, zeroline=False, **y1_args)
    axis_y2 = None
    if y2_title:
        axis_y2 = create_axis(y2_title, side=y2_position,
            overlaying='y', zeroline=False, **y2_args)

    return axis_x, axis_y1, axis_y2


def _build_output_name(filepath):
    return join(dirname(abspath(__file__)), "../output/", filepath.split('.csv')[0].split("/")[-1].split("-results_")[-1])