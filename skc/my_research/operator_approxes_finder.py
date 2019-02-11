from abc import abstractmethod
from os.path import join, dirname, abspath

import time
import cPickle
import sys

from skc.basic_approx import search 
from skc.my_research import MODULE_LOGGER
#from skc.my_research import MODULE_LOGGER


class OperatorApproxesFinder():
    #@staticmethod
    @abstractmethod
    def find_basic_approx(self,operator, distclass):
        '''Operator with                               
        its matrix, the search method calls it'''
        pass

    @abstractmethod
    def init_approxes(self):
        ''' Un metodo que valga tanto para leer los pickles como para inicializar el arbol? interesante
        '''
        pass

    @abstractmethod
    def name(self):
        pass

class KDTreeApproxesFinder(OperatorApproxesFinder):

    #TO THINK ABOUT
    def __init__(self, *args):
        '''
        Como el tiempo para construir el arbol deberia tenerse en cuenta... o no?
        se le pasa ya hecho el arbol?
        '''
        pass

    def find_basic_approx(self,operator, distclass):
        pass

    def name(self):
        return "kd_tree_finder"


class BasicApproxesFinder(OperatorApproxesFinder):

    def __init__(self, *args):
        self._basic_approxes = []

    def find_basic_approx(self,operator, distclass):
        #import pdb
        #pdb.set_trace()
        #try:
        min_dist = sys.maxint # set to max float value at first
        closest_approx = operator
        for approx in self._basic_approxes:
            current_dist = distclass.distance(approx, operator)
        
            if (current_dist < min_dist):
                min_dist = current_dist
                closest_approx = approx
        return closest_approx, min_dist


    def init_approxes(self):
        if self._basic_approxes:
            MODULE_LOGGER.info("Basic aproxes already loaded")
            return
        with open(join(dirname(abspath(__file__)),
            '../../pickles/su2/final-group-su2-256214.pickle'), 'rb') as f:
            MODULE_LOGGER.info("Starting to load approxes")
            begin_time = time.time()
            basic_approxes = cPickle.load(f)
            approx_time = time.time() - begin_time
            MODULE_LOGGER.info("Loaded basic approximations in: " + str(approx_time))
            MODULE_LOGGER.info("Number of BA: " + str(len(basic_approxes)))
        self._basic_approxes = basic_approxes


    def name(self):
        return "bassic_finder"


class QuikBasicApproxesFinder(BasicApproxesFinder):
    def __init__(self, initial_approxes):
        ''' Approxes is a list of Operators'''
        self._basic_approxes = initial_approxes

    def init_approxes(self):
        pass

    def name(self):
        return "quik_bassic_finder"