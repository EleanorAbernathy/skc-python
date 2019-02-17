import unittest as ut
from skc.my_research.su2_reader import SU2Reader, GroupReducer


class SU2ReaderTest(ut.TestCase):
    #def setUp(self):
    reader = SU2Reader()
    group = reader.read_and_create()
    reducer = GroupReducer()

    def test_create(self):
        self.assertNotEqual(self.reader, None)
        self.assertNotEqual(self.group, [])


    def test_random_subgroup(self):
        subgroup = self.reducer.get_random_subgroup(self.group, 0.5)
        print len(subgroup)
        print len(self.group)
        assert len(subgroup) <= len(self.group)/2
        assert len(subgroup) >= len(self.group)/2 - 1

    def _test_smoother_subgroup(self):
        subgroup2 = self.reducer.get_smoother_subgroup(self.group, 0.5)
        subgroup3 = self.reducer.get_smoother_subgroup(self.group, 0.3)
        print len(subgroup2)
        print len(subgroup3)
        print len(self.group)
        assert len(subgroup3) < len(subgroup2)

    def _test_filtered_subgroup(self):
        subg = self.reducer.get_filtered_subgroup(self.group, 0.5)
        print len(subg)
        assert len(subg) < len(self.group)

if __name__ == '__main__':
    ut.main()