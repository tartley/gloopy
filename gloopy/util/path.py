'''
Define all paths here. In particular, use this module instead of using
__file__ to locate resources, since these will be installed separate from the
source code in some circumstances (e.g. installed from rpm).
'''

import sys
from sys import argv, exit, platform
from os.path import abspath, dirname, join

from .. import NAME

# centralize *all* application path values here

def get_platform():
    if platform.startswith('win'):
        return 'windows'
    elif platform.startswith('darwin'):
        return 'mac'
    return 'linux'


def get_setup():
    if hasattr(sys, 'frozen'):
        # ie. py2exe, py2app or similar, either standalone or installed
        return 'binary'
    return 'source'


CONTEXT = (get_platform(), get_setup())

if CONTEXT[1] == 'source': # run from source
    # running from source
    APP_ROOT = abspath(join(dirname(__file__), '..', '..'))
elif CONTEXT == ('windows', 'binary'):
    APP_ROOT = dirname(argv[0])
else:
    exit('Error %s' % (CONTEXT,))

SOURCE = join(APP_ROOT, NAME)
DATA = join(APP_ROOT, 'data')

