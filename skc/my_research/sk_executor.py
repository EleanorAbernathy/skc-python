from os.path import join, abspath
from datetime import datetime
import time, csv
from collections import OrderedDict

from skc.my_research import H2, X_AXIS, MODULE_LOGGER
from skc.compose import get_random_unitary
from skc.operator import Operator

from solovay_kitaev import SolovayKitaev, SolovayKitaevEph

class SolovayKitaevExecutor():


    @staticmethod
    def execute(sk, approxes_finder, distance, operator_U=None, **kwargs):

        if not operator_U:
            operator_U = SolovayKitaevExecutor._get_random_operator()
        MODULE_LOGGER.debug("The algorithm is going to find approx to "+str(operator_U.matrix))

        approxes_finder.init_approxes()
        begin_time = time.time()
        result = sk.solovay_kitaev(operator_U, **kwargs)
        end_time = time.time()
        final_time = end_time - begin_time
        MODULE_LOGGER.info("Executed sk in "+ str(final_time))
        MODULE_LOGGER.debug("Matrix found: "+str(result.matrix))

        accurance = distance.distance(result, operator_U)
        MODULE_LOGGER.debug("Distance: " +str(accurance))

        return {'accurance' : accurance,
                'final_time' :  final_time, 
                'result' : result,
                'operator_U' : operator_U}


    @staticmethod
    def execute_several(sk, approxes_finder, distance, factor_method, operator_U=None, times=1, **kwarg):

        results = OrderedDict({})
        assert times > 0
        operators = [None] * times
        arg_name = kwarg.keys()[0]
        arg_values = kwarg[arg_name]
        for val in arg_values:
            results[str(val)] = {'times' : [], 'distances' : []}
            MODULE_LOGGER.info("Starting iterations for %s=%s"%(arg_name, val))
            key = str(val)
            for tt in range(times):
                matrix = operators[tt]
                returned = SolovayKitaevExecutor.execute(sk, approxes_finder, distance, matrix, **{arg_name : val} )
                operators[tt] = returned['operator_U']
                MODULE_LOGGER.debug("Operator saved (%s), (%s)"%(returned['operator_U'],operators))
                results[key]['times'].append(returned['final_time'])
                results[key]['distances'].append(returned['accurance'])


        for key in results:
            times_list = results[key]['times']
            distances = results[key]['distances']
            results[key]['average_times'] = float(sum(times_list)) / times
            results[key]['average_distances'] = float(sum(distances)) / times

        filepath = SolovayKitaevExecutor._build_file_path(sk, approxes_finder, distance, factor_method)
        SolovayKitaevExecutor._dump_results(results, filepath, ["#" + arg_name, 'times', 'average_times', 'distances', 'average_distances'])

        return results

    @staticmethod
    def _build_file_path(sk, approxes_finder, distance, factor_method):
        currdir = join(dirname(abspath(__file__)), 'out')
        _filename = "%s-results_%s_%s_%s_%s.csv"
        timestamp = str(datetime.today()).replace(" ", "_").replace(":",".")
        filename = _filename%(timestamp, sk.name(), approxes_finder.name(), distance.name(), factor_method.name() )
        return join(currdir, filename)

    @staticmethod
    def _get_random_operator():
        return Operator(
            'matrix_U',
            get_random_unitary(H2)[0]
            )

    @staticmethod
    def _dump_results( results, filepath, header=[]):
        with open(filepath, 'w') as f:
            writer = csv.writer(f, delimiter=";")
            if header:
                writer.writerow(header)
            for n, content in results.iteritems():
                time=content['average_times']
                times =content['times']
                distance=content['average_distances']
                distances=content['distances']
                writer.writerow([n,times, time, distances, distance])



from operator_approxes_finder import *
from operator_distance import *
from operator_factor_method import *

#print SolovayKitaevExecutor.execute(BasicApproxesFinder(), FowlerDistance, DawsonGroupFactor(), 1)
#Change to QuickFinder!!!
approxes_finder = BasicApproxesFinder()
distance = FowlerDistance
factor_method = DawsonGroupFactor()
sk = SolovayKitaev(approxes_finder, distance, factor_method)
print SolovayKitaevExecutor.execute_several(sk,
            approxes_finder, distance, factor_method, times=2, n=[0, 1, 2])
#sk = SolovayKitaevEph(approxes_finder, distance, factor_method)
#print SolovayKitaevExecutor.execute_several(sk,
#            approxes_finder, distance, factor_method, accurance=[0.2, 0.1])