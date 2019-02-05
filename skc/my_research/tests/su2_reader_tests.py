import unittest as ut
<<<<<<< HEAD
from skc.my_research.su2_reader import SU2Reader


class SU2ReaderTest(ut.TestCase):
=======
from skc.my_research import SU2Reader


class SU2ReaderTest(ut.unittest):
>>>>>>> 7611c9415bf67f717f2fc2dabdb7c08263edf957

	reader = SU2Reader()
	group = reader.read_and_create()
	#def setUp(self):

	def test_create(self):
		self.assertNotEqual(self.reader, None)
		self.assertNotEqual(self.group, [])
		