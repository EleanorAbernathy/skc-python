import sys, math
from skc.basis import get_hermitian_basis
from skc.my_research import H2, MODULE_LOGGER

#https://arxiv.org/pdf/quant-ph/0505030.pdf
EPH_0 = 0.14 
C_approx = 4 * math.sqrt(2)

class SolovayKitaev():

    def __init__(self, approxes_finder, distance, factor_method):
        #returns closest approx of a operator from others
        self._finder = approxes_finder

        #distance btw 2 operators
        self._distance = distance
        
        #expects an operator to factorize, returns 2
        self._factor_method = factor_method

        #store results
        self._results = {}

    def solovay_kitaev(self, op_matrix_U, n=3):
        ''' op_matrix_U: Operator
            n: recursion depth '''

        MODULE_LOGGER.debug("Starting level %d"%n)
        if (n <= 1):
            ''' Base case '''
            basic_approx, min_dist = self._finder.find_basic_approx(op_matrix_U, self._distance)
            return basic_approx


        #First aproxes
        U_n = self.solovay_kitaev(op_matrix_U, n-1)
        MODULE_LOGGER.debug("U_n: "+str(U_n.matrix))
        U_n_dagger = U_n.dagger()
        V, W = self._factor_method.decompose(
            op_matrix_U.multiply(U_n_dagger))
        MODULE_LOGGER.debug("V: "+str(V.matrix))
        MODULE_LOGGER.debug("W: "+str(W.matrix))

        #Aprox matrix factors
        V_n = self.solovay_kitaev(V, n-1)
        V_n_dagger = V_n.dagger()
        W_n = self.solovay_kitaev(W, n-1)
        W_n_dagger = W_n.dagger()
        MODULE_LOGGER.debug("V_n: "+str(V_n.matrix))
        MODULE_LOGGER.debug("W_n: "+str(W_n.matrix))

        #Multiply all
        U_approx = V_n.multiply(
                   W_n).multiply(
                   V_n_dagger).multiply(
                   W_n_dagger).multiply(
                   U_n)
        MODULE_LOGGER.debug("U_approx: "+str(U_approx.matrix))
        self._results['U_approx'] = U_approx
        return U_approx

    def get_results(self):
        return self._results

    def name(self):
        return "sk"


class SolovayKitaevEph(SolovayKitaev):

    def __init__(self, approxes_finder, distance, factor_method, max_iters = 5):
        SolovayKitaev.__init__(self, approxes_finder, distance, factor_method)
        self._max_iters = max_iters

    def solovay_kitaev(self, op_matrix_U, accurance):
        MODULE_LOGGER.debug("Starting level for accurance %2f"%accurance)
        if (accurance >= EPH_0 or self._max_iters == 0):
            ''' Base case '''
            basic_approx, min_dist = self._finder.find_basic_approx(op_matrix_U, self._distance)
            self._results['U_approx'] = basic_approx
            self._results['iters'] = 0 
            return basic_approx


        distance = sys.maxint
        n_iters = 0
        while accurance < distance and n_iters <= self._max_iters :
            n_iters += 1
            self._max_iters -= 1
            next_accurance = C_approx * math.pow(accurance, 1.5)
            #First aproxes
            U_n = self.solovay_kitaev(op_matrix_U, next_accurance)
            MODULE_LOGGER.debug("U_n: "+str(U_n.matrix))
            U_n_dagger = U_n.dagger()
            V, W = self._factor_method.decompose(
                op_matrix_U.multiply(U_n_dagger))
            MODULE_LOGGER.debug("V: "+str(V.matrix))
            MODULE_LOGGER.debug("W: "+str(W.matrix))

            #Aprox matrix factors
            V_n = self.solovay_kitaev(V, next_accurance)
            V_n_dagger = V_n.dagger()
            W_n = self.solovay_kitaev(W, next_accurance)
            W_n_dagger = W_n.dagger()
            MODULE_LOGGER.debug("V_n: "+str(V_n.matrix))
            MODULE_LOGGER.debug("W_n: "+str(W_n.matrix))

            #Multiply all
            U_approx = V_n.multiply(
                       W_n).multiply(
                       V_n_dagger).multiply(
                       W_n_dagger).multiply(
                       U_n)
            MODULE_LOGGER.debug("U_approx: "+str(U_approx.matrix))
            distance = self._distance.distance(U_approx, op_matrix_U)
            self._max_iters +=1

        self._results['U_approx'] = U_approx
        self._results['iters'] = n_iters 
        return U_approx

    def name(self):
        return "sk_eph"