from os.path import abspath, dirname, join

def build_complete_path(reldir):
	return join(dirname(abspath(__file__)), reldir)