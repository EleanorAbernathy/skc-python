import random
from os.path import join, abspath, dirname, isfile
import os, cPickle

from skc.my_research import PICKLES_PATH, MODULE_LOGGER, H2
from skc.operator import Operator
from skc.kdtree import KDTree
from skc import utils



class SU2TreeBuilder():

    def __init__(self, tree_path=PICKLES_PATH + "/kdtree"):
        self._path = tree_path
        #group = []
        self._kdtree = None

    def get_and_create(self, approxes ,filename="kdtree_su2.pickle"):
        if not self._kdtree:
            self._build_kdtree(approxes)
            self._dump_tree(filename)
        return self._kdtree

    def _build_kdtree(self, approxes):
        #MODULE_LOGGER.info("KD tree not inizialised, creating")
        data = []
        for o in approxes:
            utils.set_operator_dimensions(o, H2)
            data.append(o)
        self._kdtree = KDTree.construct_from_data(data)

    def _dump_to_file(self, obj, filename):
        filedir = join(self._path, filename)
        with open(filedir, "w") as f:
            cPickle.dump(obj, f, cPickle.HIGHEST_PROTOCOL)

    def _read_from_file(self, filename):
        with open(filename, 'rb') as f:
            obj = cPickle.load(f)
        return obj





class SU2Reader(SU2TreeBuilder):

    def __init__(self, group_path=PICKLES_PATH + "/su2"):
        SU2TreeBuilder.__init__(self, group_path)
        self._group = []

    def read_and_create(self, max_len=16, file_base_name='gen-g%d-1.pickle'):
        matrix_number = 1
        # Start numbering gates from 1, since identity is 0
        filename_pattern="final-group-su2-%s.pickle"
        for seq_len in range(1, max_len+1):
            filename = join(self._path, file_base_name%seq_len)
            if not os.path.isfile(filename):
                MODULE_LOGGER.warning("No generation found for lenght %d"%seq_len)
                continue

            new_sequences = self._read_from_file(filename)
            
            MODULE_LOGGER.debug("Generation %d, %d read:"%(seq_len, len(new_sequences)))
    
            for newop in new_sequences:
                new_op = Operator(newop.name, newop.matrix, newop.ancestors)
                new_op.name = "G%d"%matrix_number
                matrix_number += 1
                self._group.append(new_op)

            self._dump_to_file(self._group, filename_pattern%str(len(self._group)))
        return self._group

class GroupReducer(SU2TreeBuilder):

    def __init__(self, tree = None):
        self._kdtree = tree

    @staticmethod    
    def get_random_subgroup(group,  percentage=None, n_items=None):
        n_items = GroupReducer._get_subgroup_checks(group, percentage, n_items
            )
        return random.sample(group, n_items)

    def get_smoother_subgroup(self, group, percentage=None, n_items=None ):
        n_items = GroupReducer._get_subgroup_checks(group, percentage, n_items)
        final_group = []
        glen = 0

        if not self._kdtree:
            MODULE_LOGGER.info("KD tree not inizialised, creating")
            SU2TreeBuilder._build_kdtree(self, group)
        #determine nn_range to look in
        #50% => split into len/2 groups ==> 2 nn?
        #33% => split into len/3 groups ==> 3 nn?
        nn = int(len(group) / n_items) if not percentage else int(1/percentage)
        for ii, op in enumerate(group):

            nneighs = self._kdtree.query(op, nn)
            if any([neig in final_group for neig in nneighs]):
                continue
            else:
                final_group.append(op)
                glen +=1
            if glen == n_items:
                break

        return final_group
    
    @staticmethod        
    def get_filtered_subgroup(group, percentage=None, n_items=None):
        n_items = GroupReducer._get_subgroup_checks(group, percentage, n_items)
        data = []
        tolerance = 1e-9
        for op in group:
            for filtered_op in data:
                if utils.fowler_distance(filtered_op.matrix, op.matrix) < tolerance:
                    break
            else:
                data.append(op)
        return data

    
    @staticmethod        
    def _get_subgroup_checks(group,  percentage, n_items):
        
        glen = len(group)
        assert (percentage and percentage > 0 and percentage <= 1) or \
                (n_items and n_items > 0 and n_items <= glen)
        if not n_items:
            n_items = int(glen * percentage)
        return n_items

