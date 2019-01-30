from skc.basis import get_hermitian_basis
from skc.my_research import H2, MODULE_LOGGER

class SolovayKitaev():

    def __init__(self, approxes_finder, distance, factor_method,
        basis=H2,
        #vervosity
        ):
        #basis?
        #returns closest approx of a operator from others
        self._finder = approxes_finder

        #distance btw 2 operators
        self._distance = distance
        
        #expects an operator to factorize, returns 2
        self._factor_method = factor_method

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
        return U_approx


