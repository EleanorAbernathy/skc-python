import csv, sys, glob
from os.path import abspath, dirname, join
from os import getcwd
from collections import OrderedDict


def random_vs_shorter_parse(random_file, shorter_file):
    n_items = random_file.split("su2-")[-1].split("_")[0]
    n_items = int(n_items)

    random_data = parse_file(random_file) #x = [n], y1 = [times], y2 = [distances]
    shorter_data = parse_file(shorter_file)

    return n_items, random_data, shorter_data

def parse_several(filesnames):
    n_items = []
    times = OrderedDict({})
    distances = OrderedDict({})
    _sort_files(filesnames)

    for ii, filename in enumerate(filesnames):
        density = filename.split("su2-")[-1].split("_")[0]
        n_items.append(int(density))
        results_file = parse_file(filename)
        times_file = results_file['y1']
        distances_file = results_file['y2']
        n_values = results_file['x']
        if ii == 0:
            _init_dicts(n_values, times, distances)
        for index, nn in enumerate(n_values):
            times[str(nn)].append(times_file[index])
            distances[str(nn)].append(distances_file[index])

    return n_items, times, distances

def parse_several_error_time(all_filesnames):
    tree_files = filter(lambda name: "kd_tree_finder" in name, all_filesnames)
    random_files = filter(lambda name: "random_group" in name, all_filesnames)
    bassic_files = filter(lambda name: "bassic_finder" in name, all_filesnames)

    results = {'tree' : parse_several(tree_files),
    'bassic' : parse_several(bassic_files),
    'random' : parse_several(random_files)}
    return results



def _init_dicts(n_depth, *dicts):
    for nn in n_depth:
        for d in dicts:
            d[str(nn)] = []

def _sort_files(files):
    key=lambda name:  int(name.split("su2-")[-1].split("_")[0])
    files.sort(key=key)

def several_random_shorter_parse(random_files, shorter_files):
    assert len(random_files) == len(shorter_files)
    _sort_files(random_files)
    _sort_files(shorter_files)
    x_values = []
    times_random = OrderedDict({}) #n=1 : [yvalues], n=2 : [yvalues]
    times_shorter = OrderedDict({})
    distances_random = OrderedDict({})
    distances_shorter = OrderedDict({})

    
    for ii, pair in enumerate(zip(random_files, shorter_files)):
        rfile, sfile = pair
        n_items, random_data, shorter_data = random_vs_shorter_parse(rfile, sfile)
        x_values.append(n_items)
        n_list = random_data['x']
        if ii == 0:
            _init_dicts(n_list, times_random, times_shorter, distances_shorter, distances_random)
        rtimes = random_data['y1']
        stimes = shorter_data['y1']
        rdistances = random_data['y2']
        sdistances = shorter_data['y2']
        for index, jj in enumerate(n_list):
            times_random[str(jj)].append(rtimes[index])
            times_shorter[str(jj)].append(stimes[index])
            distances_random[str(jj)].append(rdistances[index])
            distances_shorter[str(jj)].append(sdistances[index])

    return {"x" : x_values, "times_random" : times_random, "times_shorter" : times_shorter,
    "distances_random" : distances_random, "distances_shorter" : distances_shorter}



def parse_file(filepath):
    with open(filepath, 'r') as f:
        reader = csv.reader(f, delimiter=';')
        next(reader, None)
        all_data = [l for l in reader]

    x_values = [int(line[0]) for line in all_data]
    y1_values = [float(line[2]) for line in all_data]
    y2_values = [float(line[4]) for line in all_data]

    return {"x" : x_values, "y1" : y1_values, "y2": y2_values}


def search_files(directory, pattern):
    #relative directory from repo root skc-python
    repo_root = dirname(abspath(join(dirname(abspath(__file__)), "../..")))
    filesdir = join(repo_root, directory)
    pattern_to_read = join(filesdir, pattern)
    filesnames = glob.glob(pattern_to_read)
    return filesnames
