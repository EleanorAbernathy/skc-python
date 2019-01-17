# Generate the single-qubit Fowler group

from skc.basic_approx.generate import *

import numpy
from skc.operator import *
from skc.simplify import *
from skc.simplify import *
from skc.basis import *
from skc.basic_approx import *

# S matrix
S_matrix = matrixify([[1, 0], [0, 1.0j]])
S = Operator("S", S_matrix)
Sd_matrix = matrixify([[1, 0], [0, -1.0j]])
Sd = Operator("Sd", Sd_matrix)

gset = [H, SX, SZ, S, Sd]

##############################################################################
# Hermitian basis

H2 = get_hermitian_basis(d=2)

print "BASIS H2"
for (k,v) in H2.items_minus_identity():
	print str(k) + " => " + str(v.matrix)

##############################################################################
# Simplifying rules
double_rules = []

for gate in gset:
	new_double_rule = DoubleIdentityRule(symbol=gate.name, id_sym=H2.identity.name)
	double_rules.append(new_double_rule)


simplify_rules = [
	IdentityRule(H2.identity.name),
	AdjointRule(id_sym=H2.identity.name),
	DoubleAdjointRule()
	]
simplify_rules.extend(double_rules)

##############################################################################
# Prepare settings

set_filename_prefix("pickles/su2/gen")

print filename_prefix
settings = BasicApproxSettings()
settings.set_iset(gset)
settings.init_simplify_engine(simplify_rules)
settings.set_identity(H2.identity)
settings.basis = H2
#settings.custom_rules_func = None
