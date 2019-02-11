import unittest as ut
import numpy as np
from skc.my_research.operator_approxes_finder import *
from skc.my_research.operator_distance import *
from skc.operator import Operator



class BassicApproxesFinderTest(ut.TestCase):

    self.finder = BasicApproxesFinder()
    def setUp(self):
        self.fowler_distance = FowlerDistance
        self.trace_distance = TraceDistance
        self.finder.init_approxes()


    def test_identity_approx(self):
        op = Operator("I", np.eye(2))
        aprox, dist = self.finder.find_basic_approx(op, self.fowler_distance)
        print aprox, dist

