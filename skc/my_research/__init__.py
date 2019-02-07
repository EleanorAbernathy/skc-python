import verboselogs as vl
import logging as lg
import getopt, sys
from os.path import join, abspath, dirname
from skc.basis import cart3d_to_h2, get_hermitian_basis

X_AXIS = cart3d_to_h2(x=1, y=0, z=0)
H2 = get_hermitian_basis(d=2)

PICKLES_PATH = join(dirname(abspath(__file__)), "../../pickles/su2/")


def get_module_logger(
    verbosity=lg.SPAM,
    file=None, # if no file, stdout
    msg_format="%(asctime)s [%(levelname)-5.5s]  %(message)s"
    ):
    logFormatter = lg.Formatter(msg_format)
    theloger = vl.VerboseLogger(__name__)
    if not file:
        handler = lg.StreamHandler()
    else:
        handler = lg.FileHandler(file)
    handler.setFormatter(logFormatter)
    theloger.addHandler(handler)
    theloger.setLevel(level)
    return theloger





# Command line option defaults.
verbosity = 0


# Parse command line options.
opts, args = getopt.getopt(sys.argv[1:], 'vqho', ['verbose', 'quiet', 'help', 'output'])
filedir=None
# Map command line options to variables.
for option, argument in opts:
    if option in ('-v', '--verbose'):
        verbosity += 1
    elif option in ('-q', '--quiet'):
        verbosity -= 1
    elif option in ('-h', '--help'):
        print __doc__.strip()
        sys.exit(0)
    elif option in ('-o', '--output'):
        filedir=join(abspath(dirname(__file__)), option)
    else:
        assert False, "Unhandled option!"
level = lg.INFO
# Configure logger for requested verbosity.
if verbosity >= 4:
    level = lg.SPAM
elif verbosity >= 3:
    level = lg.DEBUG
elif verbosity >= 2:
    level = lg.VERBOSE
elif verbosity >= 1:
    level = lg.NOTICE
elif verbosity <= 0:
    level = lg.WARNING


MODULE_LOGGER = get_module_logger(level)

'''
logFormatter = lg.Formatter("%(asctime)s [%(threadName)-12.12s] [%(levelname)-5.5s]  %(message)s")
rootLogger = lg.getLogger()

fileHandler = lg.FileHandler("{0}/{1}.log".format(logPath, fileName))
fileHandler.setFormatter(logFormatter)
rootLogger.addHandler(fileHandler)

consoleHandler = lg.StreamHandler()
consoleHandler.setFormatter(logFormatter)
rootLogger.addHandler(consoleHandler)
'''
#Prints to the format of:
#2012-12-05 16:58:26,618 [MainThread  ] [INFO ]  my message