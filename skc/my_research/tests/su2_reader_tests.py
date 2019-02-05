import unittest as ut
from skc.my_research.su2_reader import SU2Reader


class SU2ReaderTest(ut.TestCase):

	reader = SU2Reader()
	group = reader.read_and_create()
	#def setUp(self):

	def test_create(self):
		self.assertNotEqual(self.reader, None)
		self.assertNotEqual(self.group, [])
		