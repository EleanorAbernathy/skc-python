import unittest as ut
from skc.my_research.su2_reader import SU2Reader, GroupReducer, SU2TreeBuilder
from skc.my_research.sk_factor.operator_approxes_finder import RandomApproxesFinder

class SU2ReaderTest(ut.TestCase):
    #def setUp(self):
    #reader = SU2Reader()
    #group = reader.read_and_create()
    reducer = GroupReducer()
    builder = SU2TreeBuilder()

    def _test_create(self):
        self.assertNotEqual(self.reader, None)
        self.assertNotEqual(self.group, [])

    def _test_build_trees(self):
        self.builder.read_and_create_all()

    def test_build_random_tree(self):
        random_finder = RandomApproxesFinder(filename="final-group-su2-256214.pickle", n_items=1)
        for ni in [32289, 16176 ]:
            random_finder._n_items = ni
            approxes = random_finder.init_approxes()
            tree_filename="random-kdtree-su2-%d.pickle"%ni
            self.builder.build_and_dump(approxes, tree_filename)


    def _test_random_subgroup(self):
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