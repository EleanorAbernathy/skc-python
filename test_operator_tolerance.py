g1 = (['H', 'T', 'H', 'Td', 'H', 'Td', 'H', 'T', 'T', 'H', 'T', 'T', 'H', 'T'], ['H', 'T', 'H', 'T', 'H', 'T', 'T', 'H'])

g2 = (['H', 'T', 'H', 'Td', 'H', 'Td', 'H', 'T', 'T', 'H', 'T', 'T', 'H', 'Td'] , ['H', 'T', 'H', 'T', 'H', 'T', 'T', 'H', 'Td', 'Td'])

g3 = (['H', 'T', 'H', 'Td', 'H', 'Td', 'H', 'T', 'T', 'H', 'T', 'T', 'T', 'H'] , 
	['H', 'T', 'H', 'T', 'H', 'T', 'T', 'H', 'Td', 'H', 'T', 'H'])

g4 = (['H', 'T', 'H', 'Td', 'H', 'Td', 'H', 'T', 'T', 'H', 'T', 'T', 'T', 'T'] , ['H', 'T', 'H', 'T', 'H', 'T', 'T', 'H', 'Td', 'H', 'T', 'T'])

g5 = (['H', 'T', 'H', 'T', 'T', 'T'],['H', 'T', 'H', 'Td', 'Td', 'Td', 'Td', 'Td'])

from skc.basic_approx.generate import *

from skc.operator import *
from skc.simplify import *
from skc.basic_approx import *
from skc.basis import *

import numpy

iset2 = [H, T, T_inv]


# Simplifying rules
identity_rule = IdentityRule()
double_H_rule = DoubleIdentityRule('H')
adjoint_rule = AdjointRule()
double_adjoint_rule = DoubleAdjointRule()
T8_rule = GeneralRule(['T','T','T','T','T','T','T','T'], 'I')
Td8_rule = GeneralRule(['Td','Td','Td','Td','Td','Td','Td','Td'], 'I')
# We should also add a rule for 8T gates -> I

simplify_rules = [
	identity_rule,
	double_H_rule,
	adjoint_rule,
	T8_rule,
	Td8_rule,
	#double_adjoint_rule
	]
#simplify_rules = []

H2 = get_hermitian_basis(d=2)


set_filename_prefix("pickles/su2/gen")

settings = BasicApproxSettings()
settings.set_iset(iset2)
settings.init_simplify_engine(simplify_rules)
settings.set_identity(I2)
settings.basis = H2

identity = settings.identity
for group in [g1, g2, g3, g4, g5]:
	s = set([])
	o1 = o2 = identity
	for ancestor in group[0]:
		oa = settings.iset_dict[ancestor]
		o1 = o1.multiply(oa)

	for ancestor in group[1]:
		oa = settings.iset_dict[ancestor]
		o2 = o2.multiply(oa)

	print "dist = %s"%fowler_distance(o1.matrix, o2.matrix)

	ot1 = OperatorTolerance(o1.name, o1.matrix, o1.ancestors, distance=fowler_distance)
	ot2 = OperatorTolerance(o2.name, o2.matrix, o2.ancestors, distance=fowler_distance)

	s.add(ot1)
	print s
	assert ot2 in s
	s.add(ot2)
	s.add(ot1)
	s.add(ot2)
	print s
	print ot1 == ot2, ot2 in s, ot2.__hash__() == ot1.__hash__()

