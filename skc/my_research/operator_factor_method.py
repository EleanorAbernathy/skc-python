from abc import abstractmethod
from skc.my_research import X_AXIS, H2
from skc.dawson.factor import dawson_group_factor
from skc.group_factor import aram_diagonal_factor
from skc.operator import Operator

#X_AXIS = cart3d_to_h2(x=1, y=0, z=0)
#H2 = get_hermitian_basis(d=2)

class OperatorFactorMethod():

	def __init__(self, basis=H2, axis=X_AXIS):
		self._basis = basis
		self._axis = axis

	@abstractmethod
	def decompose(self, operator):
		pass

	@abstractmethod
	def name(self):
		pass

class AramDiagonalFactor(OperatorFactorMethod):
	''' This method doesnt do it well actually...'''

	def decompose(self, operator):
		return aram_diagonal_factor(operator.matrix, self._basis, self._axis)

	def name(self):
		return "aram_factor"	


class DawsonGroupFactor(OperatorFactorMethod):

	def decompose(self, operator):
		v, w = dawson_group_factor(operator.matrix, self._basis, self._axis)
		return	Operator('V', v), Operator('W', w)

	def name(self):
		return "dawson_factor"
