import unittest as ut
from skc.my_research.solovay_kitaev import SolovayKitaev, SolovayKitaevEph
from skc.my_research.sk_executor import SolovayKitaevExecutor
from skc.my_research.operator_approxes_finder import *
from skc.my_research.operator_distance import *
from skc.my_research.operator_factor_method import *



class SKExecutorTest(ut.TestCase):

    def setUp(self):
        self.executor = SolovayKitaevExecutor
        self.finder, self.distance, self.factor = BasicApproxesFinder(), FowlerDistance, DawsonGroupFactor()
        self.sk = SolovayKitaev(self.finder, self.distance, self.factor)

    def _test_base_case(self):
        self.executor.execute(self.sk,
            self.finder, self.distance, n=1
        )

    def _test_depht_3(self):
        print self.executor.execute_several(self.sk,
            self.finder, self.distance, self.factor, n=range(1, 4)
        )

class SKExecutorEphTest(SKExecutorTest):

    def setUp(self):
        SKExecutorTest.setUp(self)
        self.sk = SolovayKitaevEph(self.finder, self.distance, self.factor)

    def test_base_case(self):
        self.executor.execute(self.sk,
            self.finder, self.distance, accurance=0.1
        )

    def _test_depht_3(self):
        print self.executor.execute_several(self.sk,
            self.finder, self.distance, self.factor, accurance=[0.1, 0.05, 0.03]
        )