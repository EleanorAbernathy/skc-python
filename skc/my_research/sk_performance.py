from sk_factor.operator_approxes_finder import *
from sk_factor.operator_distance import *
from sk_factor.operator_factor_method import *
from skc.my_research.sk_executor import SolovayKitaevExecutor
from skc.my_research.solovay_kitaev import SolovayKitaev
from collections import OrderedDict

N_ITEMS = OrderedDict({
    '1': 3,
    '2': 9,
    '3': 24,
    '4': 54,
    '5': 117,
    '6': 243,
    '7': 498,
    '8': 1006,
    '9': 2023,
    '10': 4051,
    '11': 8100,
    '12': 16176,
    '13': 32289,
    '14': 64429,
    '15': 128482,
    '16': 256214
})
distance = FowlerDistance
factor_method = DawsonGroupFactor()

def density_random_and_shorter_and_kdtree(group_filename, tree_filename, n_items, times=2, n=[1,2,3,4,5]):
    ''' Randomly, shorterly and by kdtree for given density '''

    bassic_finder = BasicApproxesFinder(filename=group_filename)
    random_finder = RandomApproxesFinder(n_items=n_items)
    tree_finder = KDTreeApproxesFinder(filename=tree_filename)
    
    sk = SolovayKitaev(tree_finder, distance, factor_method)
    results_1 = SolovayKitaevExecutor.execute_several(sk,
        tree_finder, distance, factor_method, times=times, n=n, filepath='out/random_and_shorter_and_tree')
    matrixes = results_1['operators']
    
    sk = SolovayKitaev(bassic_finder, distance, factor_method)
    SolovayKitaevExecutor.execute_several(sk,
        bassic_finder, distance, factor_method, operators=matrixes, times=times, n=n, filepath='out/random_and_shorter_and_tree')
    
    sk = SolovayKitaev(random_finder, distance, factor_method)
    SolovayKitaevExecutor.execute_several(sk,
        random_finder, distance, factor_method, operators=matrixes, times=times, n=n, filepath='out/random_and_shorter_and_tree')
    
def n_tree_vs_basic(group_filename, tree_filename, times=3, n=[1,2,3,4,5]):
    ''' Efficiency of using kdtree as n increases vs basic aproxes, for fixed density'''

    bassic_finder = BasicApproxesFinder(filename=group_filename)
    tree_finder = KDTreeApproxesFinder(filename=tree_filename)
    
    sk = SolovayKitaev(tree_finder, distance, factor_method)
    results_1 = SolovayKitaevExecutor.execute_several(sk,
        tree_finder, distance, factor_method, times=times, n=n, filepath='out/tree_vs_basic')
    matrixes = results_1['operators']
    sk = SolovayKitaev(bassic_finder, distance, factor_method)
    SolovayKitaevExecutor.execute_several(sk,
        bassic_finder, distance, factor_method, operators=matrixes[:-1], times=times-1, n=n[:-1], filepath='out/tree_vs_basic')

def just_bassic(group_filename = '',tree_filename='', times=1, n=[1,2,3,4,5,6]):
    #finder = BasicApproxesFinder(filename=group_filename)
    finder = KDTreeApproxesFinder(filename=tree_filename)
    sk = SolovayKitaev(finder, distance, factor_method)
    SolovayKitaevExecutor.execute_several(sk,
        finder, distance, factor_method, times=times, n=n, filepath='out/bassic_examples')

def density_random_vs_shorter(tree_group_filename, tree_random_filename, n_items, times=6, n=range(1,8)):
    ''' For given density, tolerance as density increases, with one or several depth.
    Will be used kdtree finder because is faster '''

    bassic_finder = KDTreeApproxesFinder(filename=tree_group_filename)
    #random_finder = KDTreeApproxesFinder(filename=tree_random_filename)
    
    
    sk = SolovayKitaev(bassic_finder, distance, factor_method)
    results_1 = SolovayKitaevExecutor.execute_several(sk,
        bassic_finder, distance, factor_method, times=times, n=n, filepath='out/random_vs_shorter')
    matrixes = results_1['operators']
    
    #sk = SolovayKitaev(random_finder, distance, factor_method)
    #SolovayKitaevExecutor.execute_several(sk,
    #    random_finder, distance, factor_method, operators=matrixes, times=times, n=n, filepath='#out/random_vs_shorter_delme')
    

if __name__ == '__main__':
    filename_pattern = 'final-group-su2-%d.pickle' %(256214)
    filename_tree_pattern = 'kdtree-su2-%d.pickle'%(256214)
    random_tree_filename = 'random-kdtree-su2-%d.pickle'
    #just_bassic(filename_pattern, n=range(1,3))
    just_bassic("", filename_tree_pattern)
    just_bassic("", filename_tree_pattern)

    #for ii in ['2','6','9','12','14','16']: 
    #    N = N_ITEMS[ii]
    #    MODULE_LOGGER.info("density %d, random and shorter and kdtree..."%N)
    #    density_random_and_shorter_and_kdtree(filename_pattern%N, filename_tree_pattern%N, N)

    #MODULE_LOGGER.info("tree vs basic with density %d"%N_ITEMS['16'])
    #n_tree_vs_basic(filename_pattern%N_ITEMS['16'], filename_tree_pattern%N_ITEMS['16'])


    #for N in [N_ITEMS[i] for i in ['11', '12', '13', '14', '15']]:
    #for N in [N_ITEMS[i] for i in ['12', '14']]:
    #    MODULE_LOGGER.info("random vs shorter with tree finder for density %d"%N)
    #    density_random_vs_shorter(filename_tree_pattern%N, random_tree_filename%N, N)
    #    #density_random_vs_shorter(filename_tree_pattern%N, random_tree_filename%N, N, times=2, n=[2,3])