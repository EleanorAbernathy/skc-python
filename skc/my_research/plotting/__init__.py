from os.path import abspath, dirname, join

BASSIC_REFERENCE_RATE = [0.18457376749021018, 0.28611292276224287, 0.6140807236130741, 4.620204412627869, 41.7855116259829]

def build_complete_path(reldir):
	return join(dirname(abspath(__file__)), reldir)