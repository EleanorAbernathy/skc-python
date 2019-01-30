from os.path import join, dirname, abspath

from skc.basic_approx import *
from skc.basis import get_hermitian_basis
from skc.basic_approx.search import find_basic_approx
from skc.operator import H, Operator
from skc.decompose import get_random_unitary
from skc.utils import trace_distance, fowler_distance
from skc.dawson.factor import dawson_group_factor, dawson_x_group_factor_su2, dawson_x_group_factor
import cPickle
import time

basis = None
def solovay_kitaev(U, n, basic_approxes):
    global basis
    if (n == 0):
        basic_approx, min_dist = find_basic_approx(basic_approxes, U, fowler_distance)
        # discard min_dist for now. but just you wait...
        print "Returning basic approx: %s, Min dist %s" %( str(basic_approx), min_dist)
        return basic_approx
    else:
        print "Beginning level " + str(n)
        U_n1 = solovay_kitaev(U, n-1, basic_approxes) # U_{n-1}
        #print "U_"+str(n-1)+": " + str(U_n1)
        U_n1_dagger = U_n1.dagger()
        V,W = dawson_x_group_factor(U.multiply(U_n1_dagger).matrix, basis)
        #print "V: " + str(V)
        #print "W: " + str(W)
        V_n1 = solovay_kitaev(V, n-1, basic_approxes) # V_{n-1}
        print "V_"+str(n-1)+": " + str(V_n1)
        V_n1_dagger = V_n1.dagger()
        W_n1 = solovay_kitaev(W, n-1, basic_approxes) # W_{n-1}
        print "W_"+str(n-1)+": " + str(W_n1)
        W_n1_dagger = W_n1.dagger()
        V_n1_dagger_W_n1_dagger = V_n1_dagger.multiply(W_n1_dagger)
        V_n1_W_n1 = V_n1.multiply(W_n1)
        delta = V_n1_W_n1.multiply(V_n1_dagger_W_n1_dagger)
        U_n = delta.multiply(U_n1)
        print "delta_"+str(n)+": " + str(U_n)
        print "Ending level " + str(n)
        return U_n

def main():
    global basis
    #f = open('basic_approxes.pickle', 'rb')
    with open(join(dirname(abspath(__file__)),'../pickles/su2/gen-iset.pickle'), 'rb') as f: 
        begin_time = time.time()

        iset = cPickle.load(f)

        iset_time = time.time() - begin_time
    print "Loaded instruction set in: " + str(iset_time)
    print "Iset = " + str(iset)



    basis = get_hermitian_basis(d=2)
    (search_U, components, angle) = get_random_unitary(basis)
    dawson_x_group_factor(search_U, basis)
    with open(join(dirname(abspath(__file__)),'../pickles/su2/--final-group-4.pickle'), 'rb') as f: 
        begin_time = time.time()
        #with open(join(dirname(abspath(__file__)),'../pickles/su2/gen-g16-2.pickle'), 'rb') as g:
        basic_approxes = cPickle.load(f)
            #basic_approxes.extend(cPickle.load(g))
        #basic_approxes = [I2]
        approx_time = time.time() - begin_time
    print "Loaded basic approximations in: " + str(approx_time)
    print "Number of BA: " + str(len(basic_approxes))

    import pdb
    pdb.set_trace()
    basic_approx, min_dist = find_basic_approx(basic_approxes, search_U, fowler_distance)
    aprox = solovay_kitaev(Operator('search_U', search_U), 1, basic_approxes)
    print "trace_dist(op,U)= " + str(trace_distance(aprox.matrix, search_U))
    print "fowler_dist(op,U)= " + str(fowler_distance(aprox.matrix, search_U))



if __name__ == '__main__':
    main()