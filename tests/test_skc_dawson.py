from skc.operator import *
from skc.dawson import *
from skc.utils import *
from skc.compose import *
from skc.basis import *
from skc.group_factor import *
import math

d = 2
basis = get_hermitian_basis(d=d)
theta = math.pi / 4 # 45 degrees

axis_U = cart3d_to_h2(x=1, y=1, z=1)
angle_U = math.pi / 12

#matrix_U = axis_to_unitary(axis_U, theta/2.0, basis)
(matrix_U, components, angle) = get_random_unitary(basis)

print "U= " + str(matrix_U)

#load_basic_approxes("basic_approxes_su4.pickle")
sk_set_basis(basis)
random_axis = pick_random_axis(basis)
sk_set_axis(random_axis)
sk_set_factor_method(dawson_group_factor)

Uop = Operator(name="U", matrix=matrix_U)

sk_build_tree("su2", 16)
Un = solovay_kitaev(Uop, 3, 'U', '')
print "Approximated U: " + str(Un)

print "Un= " + str(Un.matrix)
print "dist(U,Un)= " + str(fowler_distance(Un.matrix, Uop.matrix))