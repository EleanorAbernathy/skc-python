import unittest as ut
from skc.my_research.sk_executor import SolovayKitaevExecutor
from skc.my_research.operator_approxes_finder import *
from skc.my_research.operator_distance import *
from skc.my_research.operator_factor_method import *



class SKExecutorTest(ut.TestCase):

    def setUp(self):
        self.executor = SolovayKitaevExecutor

    def _test_base_case(self):
        self.executor.execute(
            BasicApproxesFinder(), FowlerDistance, DawsonGroupFactor(), 1
        )

    def test_depht_3(self):
        print self.executor.execute_several(
            BasicApproxesFinder(), FowlerDistance, DawsonGroupFactor(), till_n=3
        )