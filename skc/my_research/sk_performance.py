from sk_factor.operator_approxes_finder import *
from sk_factor.operator_distance import *
from sk_factor.operator_factor_method import *
from skc.my_research.sk_executor import SolovayKitaevExecutor
from skc.my_research.solovay_kitaev import SolovayKitaev

def random_vs_shorter():
	bassic_finder = BasicApproxesFinder(filename='final-group-su2-128482.pickle')
	random_finder = RandomApproxesFinder(n_items=128482)
	distance = FowlerDistance
	factor_method = DawsonGroupFactor()
	
	sk = SolovayKitaev(bassic_finder, distance, factor_method)
	results_1 = SolovayKitaevExecutor.execute_several(sk,
        bassic_finder, distance, factor_method, times=2, n=[0, 1, 2])
	matrixes = results_1['operators']
	
	sk = SolovayKitaev(random_finder, distance, factor_method)
	SolovayKitaevExecutor.execute_several(sk,
        random_finder, distance, factor_method, operators=matrixes, times=2, n=[0, 1, 2])
	

if __name__ == '__main__':
	random_vs_shorter()