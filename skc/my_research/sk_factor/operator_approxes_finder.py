from abc import abstractmethod
from os.path import join, dirname, abspath

import time
import cPickle
import sys
import numpy as np

from skc.basic_approx import search 
from skc.my_research import MODULE_LOGGER, H2
from skc.my_research.su2_reader import GroupReducer
from skc import utils


class OperatorApproxesFinder():
    #@staticmethod
    @abstractmethod
    def find_basic_approx(self,operator, distclass):
        '''Operator with                               
        its matrix, the search method calls it'''
        pass

    def init_approxes(self):
        self._init_approxes()
        return self._basic_approxes


    @abstractmethod
    def _init_approxes(self):
        ''' Read approxes, or the tree
        '''
        pass

    @abstractmethod
    def name(self):
        pass

class BasicApproxesFinder(OperatorApproxesFinder):

    def __init__(self, filedir="pickles/su2/", filename="final-group-su2-256214.pickle" ,**kwargs):
        self._basic_approxes = []
        self._filedir = filedir
        self._filename = filename

    def find_basic_approx(self,operator, distclass):
        min_dist = sys.maxint # set to max float value at first
        closest_approx = operator
        if not self._basic_approxes:
            MODULE_LOGGER.error("No approxes initialised!")
        for approx in self._basic_approxes:
            current_dist = distclass.distance(approx, operator)
        
            if (current_dist < min_dist):
                min_dist = current_dist
                closest_approx = approx
        return closest_approx, min_dist


    def _init_approxes(self):
        if self._basic_approxes:
            MODULE_LOGGER.info("Basic aproxes already loaded")
            return
        path = join(dirname(abspath(__file__)), "../../..")
        allpath = join(join(path, self._filedir), self._filename)
        with open(allpath, 'rb') as f:
            MODULE_LOGGER.info("Starting to load approxes")
            begin_time = time.time()
            basic_approxes = cPickle.load(f)
            approx_time = time.time() - begin_time
            MODULE_LOGGER.info("Loaded basic approximations in: " + str(approx_time))
            MODULE_LOGGER.info("Number of BA: " + str(len(basic_approxes)))
        self._basic_approxes = basic_approxes


    def name(self):
        return "bassic_finder"




class KDTreeApproxesFinder(BasicApproxesFinder):

    def __init__(self, filedir="pickles/kdtree", filename="kdtree_su2.pickle" ,**kwargs):
        BasicApproxesFinder.__init__(self, filedir, filename, **kwargs)
        self._tree = None
        
    def _init_approxes(self):
        if self._tree:
            MODULE_LOGGER.info("Tree already loaded")
            return
        path = join(dirname(abspath(__file__)), "../../..")
        allpath = join(join(path, self._filedir), self._filename)
        with open(allpath, "r") as f:
            MODULE_LOGGER.info("Starting to load tree")
            begin_time = time.time()
            self._tree = cPickle.load(f)
            approx_time = time.time() - begin_time
            MODULE_LOGGER.info("Loaded tree in: " + str(approx_time))
        

    def find_basic_approx(self,operator, distclass):
        if all((operator.matrix == np.eye(2)).flat):
            return operator, 0
        try:
            utils.set_operator_dimensions(operator, H2)
        except ValueError:
            MODULE_LOGGER.warning("Couldnt set operator dimensions for kd tree search")
            return operator, 0
        best = self._tree.query(operator, 1)[0]
        return best, distclass.distance(best, operator)


    def name(self):
        return "kd_tree_finder-" + str(self._filename.split(".pickle")[0])

class RandomApproxesFinder(BasicApproxesFinder):

    def __init__(self, filedir="pickles/su2/", filename="final-group-su2-256214.pickle" , percentage=None,n_items=None, **kwargs):
        BasicApproxesFinder.__init__(self, filedir, filename, **kwargs)
        assert percentage or n_items
        self._percentage = percentage
        self._n_items = n_items

    def _init_approxes(self):
        BasicApproxesFinder._init_approxes(self)
        self._basic_approxes = GroupReducer.get_random_subgroup(self._basic_approxes, self._percentage, self._n_items)

    def name(self):
        return "random_group_finder"