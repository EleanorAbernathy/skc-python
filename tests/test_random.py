# Test generating random matrices

import numpy
from skc.utils import *
from skc.operator import *
from skc.basis import *

# Get SU(2) basis (I plus Pauli matrices)
B2 = get_unitary_basis(d=2)

random_U = get_random_unitary(B2)
print str(random_U)