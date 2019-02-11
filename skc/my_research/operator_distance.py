from abc import abstractmethod
from skc.utils import trace_distance, fowler_distance


class OperatorDistance():

    @staticmethod
    @abstractmethod
    def distance(op_A, op_B):
        pass

    @staticmethod
    @abstractmethod
    def name():
        pass



class TraceDistance(OperatorDistance):
    ''' Trace distance usually gets smaller distances than fowler.
    It is classical matrixes norm '''

    @staticmethod
    def distance(op_A, op_B):
        return trace_distance(op_A.matrix, op_B.matrix)

    @staticmethod
    def name():
        return "trace_distance"

class FowlerDistance(OperatorDistance):

    @staticmethod
    def distance(op_A, op_B):
        return fowler_distance(op_A.matrix, op_B.matrix)

    @staticmethod
    def name():
        return "fowler_distance"