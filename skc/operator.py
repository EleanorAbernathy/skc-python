# Operator/gate, including annotation and ancestry
# The most basic kind of operator is a basic instruction from a universal gate set

import numpy;
import math;
import scipy.linalg;

from skc.utils import *
from skc.basic_approx.process import unitary_to_kdpoint, components_to_kdpoint
from skc.decompose import unitary_to_axis



class Operator:

    def __init__(self, name, matrix, ancestors=[]):
        from skc.basis import get_hermitian_basis
        self.name = name
        self.matrix = matrix
        if (len(ancestors) == 0):
            ancestors = [name]
        self.ancestors = ancestors
        self.dimensions = self._get_dimensions(matrix, get_hermitian_basis(len(matrix)))

    def __str__(self):
        return "Operator: " + str(self.name) + "\n" \
            "  Ancestors: " + str(self.ancestors)
            
    def __hash__(self):
        h = self.name.__hash__()
        for ancestor in self.ancestors:
            h *= ancestor.__hash__()
        return h
            
    def print_matrix(self):
        print "  Matrix: " + str(self.matrix)
            
    def add_ancestors(self, other, new_name=""):
        # Append new ancestors to the end of self
        new_ancestors = self.ancestors + other.ancestors
        new_op = Operator(new_name, None, new_ancestors)
        return new_op
        
    def ancestors_as_string(self):
        return list_as_string(self.ancestors)
    
    # Sets the matrix of this operator by its ancestors taken from a set
    # iset - a dictionary of labels to operators for the instruction set
    # identity - the identity to start multiplication with
    def matrix_from_ancestors(self, iset_dict, identity):
        self.matrix = identity.matrix
        for ancestor in self.ancestors:
            self.matrix = self.matrix * iset_dict[ancestor].matrix
        #print "MATRIX IS UNITARY"
        assert_matrix_unitary(self.matrix)
        msg = "Looks like someone forgot to simplify away this sequence, hmm?" \
            + str(self.ancestors)
        dist = trace_distance(self.matrix, identity.matrix)
        close_to_identity = approx_equals(dist, 0)
        named_identity = (self.name == identity.name)
        # Uncomment the following two lines if you want to catch identities
        #assert_matrices_approx_not_equal(self.matrix, identity.matrix, message=msg)
        return close_to_identity and (not named_identity)

    def multiply(self, other, new_name=""):
        new_matrix = self.matrix * other.matrix
        new_ancestors = self.ancestors + other.ancestors
        new_op = Operator(new_name, new_matrix, new_ancestors)
        return new_op
        
    def dagger(self):
        new_matrix = self.matrix.H
        reversed_ancestors = list(self.ancestors)
        reversed_ancestors.reverse()
        new_ancestors = []
        for ancestor in reversed_ancestors:
            new_ancestors.append(ancestor+"d")
        new_name = self.name + "d"
        return Operator(new_name, new_matrix, new_ancestors)
        
    def scale(self, scalar, new_name=""):
        new_matrix = self.matrix * scalar
        new_ancestors = self.ancestors + [scalar]
        return Operator(new_name, new_matrix, new_ancestors)
    
    def _get_dimensions(self, matrix, basis):

        (components, K, matrix_H) = unitary_to_axis(search_U, basis)
        # Re-center angles from 0 to 2pi, instead of -pi to pi
        if (K < 0):
            for (k,v) in components.items():
                components[k] = v * -1
            K *= -1
        
        dimensions = components_to_kdpoint(components, basis, K)
        return dimensions

    def __eq__(self, other):
        return (self.name == other.name) and (self.ancestors == other.ancestors)

class OperatorTolerance(Operator):
    def __init__(self, name, matrix, ancestors=[], tolerance=TOLERANCE10, distance=fowler_distance):
        Operator.__init__(self, name, matrix, ancestors)
        self.tol = tolerance
        self.distance = distance
        self.dist_id = self.distance(self.matrix, I2.matrix)
    def __eq__(self, other):
        #d = abs(self.dist_id - other.dist_id)
        #return d < self.tol
        d = self.distance(self.matrix, other.matrix) 
        return d < self.tol
    def __ne__(self, other):
        return not self.__eq__(other)

    #def __hash__(self):
    #   #import pdb
    #   #pdb.set_trace()
    #   dist = self.dist_id
    #   decimals = int(abs(round(math.log(self.tol, 10))))
    #   dist = round(dist, decimals)
    #   return str(dist).__hash__()


    

def get_identity(d):
    return Operator("I", matrixify(numpy.eye(d)))

##############################################################################
# SU(2) constants
# 2x2 identity matrix
I2 = get_identity(2)

# Pauli X matrix
SX_matrix = matrixify([[0, 1], [1, 0]])
SX = Operator("SX", SX_matrix)

# Pauli Y matrix
SY_matrix = matrixify([[0, -1j], [1j, 0]])
SY = Operator("SY", SY_matrix)

# Pauli Z matrix
SZ_matrix = matrixify([[1, 0], [0, -1]])
SZ = Operator("SZ", SZ_matrix)

# Hadamard gate
H_matrix = (1/math.sqrt(2)) * matrixify([[1, 1], [1, -1]])
H = Operator("H", H_matrix)

# pi/8 gate
T_matrix = matrixify([[1, 0], [0, numpy.exp(1j * math.pi / 4)]])
T = Operator("T", T_matrix)

# Inverse pi/8 gate
T_inv = Operator("Td", T.matrix.I)
