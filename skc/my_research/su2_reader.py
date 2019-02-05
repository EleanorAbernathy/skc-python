import random
from os.path import join, abspath, dirname, isfile
import os, cPickle

from skc.my_research import PICKLES_PATH, MODULE_LOGGER
from skc.operator import Operator
from skc.kdtree import KDTree

class SU2Reader():

    def __init__(self, group_path=PICKLES_PATH):
        self._path = group_path
        self._group = []
        self._kdtree = None

    def read_and_create(self, max_len=16, file_base_name='gen-g%d-1.pickle'):
        matrix_number = 1
        # Start numbering gates from 1, since identity is 0
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

        data = list(self._group)
        self._kdtree = KDTree.construct_from_data(data)
        self._dump_to_file(self._group, str(len(self._group)))
        return self._group


    def get_random_subgroup(self, percentage=None, n_items=None):
        n_items = self._get_subgroup_checks(percentage, n_items
            )
        return random.sample(self._group, n_items)

    def get_smoother_subgroup(self,percentage=None, n_items=None ):
        n_items = self._get_subgroup_checks(percentage, n_items
            )
        final_group = []
        glen = 0
        if not self._kdtree:
            MODULE_LOGGER.warning("KD tree not inizialised, reading group")
            self.read_and_create()

        #determine nn_range to look in
        #50% => split into len/2 groups ==> 2 nn?
        #33% => split into len/3 groups ==> 3 nn?
        nn = int(len(self._group) / n_items) if not percentage else int(1/percentage)
        for ii, op in enumerate(self._group):

            nneighs = self._kdtree.query(op, nn)
            if any([neig in final_group for neig in nneighs]):
                continue
            else:
                final_group.append(op)
                glen +=1
            if glen == n_items:
                break

        return final_group


    def _get_subgroup_checks(self, percentage, n_items):
        if not self._group:
            MODULE_LOGGER.warning("Group not initialised, reading it")
            self.read_and_create()
        
        glen = len(self._group)
        assert (percentage and percentage > 0 and percentage <= 1) or \
                (n_items and n_items > 0 and n_items <= glen)
        if not n_items:
            n_items = int(glen * percentage)
        return n_items

    def _read_from_file(self, filename):
        with open(filename, 'rb') as f:
            obj = cPickle.load(f)
        return obj
    
    def _dump_to_file(self, obj, filename ,filename_pattern="final-group-su2-%s.pickle"):
        filepath = join(self._path, filename_pattern%filename)
        with open(filepath, "w") as f:
            cPickle.dump(obj, f, cPickle.HIGHEST_PROTOCOL)