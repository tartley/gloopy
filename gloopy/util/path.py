'''
Access to all application path values should go via this module. In
particular, use this module instead of using __file__ to locate resources,
since resources will be separated from source code under some circumstances
(e.g. when installed from rpm.)
'''

import sys
from sys import argv, exit, platform
from os.path import abspath, dirname, join


# context = (platform, setup)
# platform = windows | mac | linux
# setup = source | frozen
CONTEXT = None

# directories we might be interested in
ROOT = None
SOURCE = None
DATA = None


def _get_platform():
    if platform.startswith('win'):
        return 'windows'
    elif platform.startswith('darwin'):
        return 'mac'
    return 'linux'

def _get_setup():
    if hasattr(sys, 'frozen'):
        # ie. py2exe, py2app or similar, either standalone or installed
        return 'binary'
    return 'source'


def init(name):
    global CONTEXT, ROOT, SOURCE, DATA

    CONTEXT = (_get_platform(), _get_setup())

    if CONTEXT[1] == 'source':
        ROOT = abspath(join(dirname(__file__), '..', '..'))
    elif CONTEXT == ('windows', 'binary'):
        ROOT = dirname(argv[0])
    else:
        exit('Error %s' % (CONTEXT,))

    SOURCE = join(ROOT, name)
    DATA = join(ROOT, 'data')

