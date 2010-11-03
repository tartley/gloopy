'''
Access to all application path values should go via this module. In
particular, use this module instead of using __file__ to locate resources,
since resources will be separated from source code under some circumstances
(e.g. when installed from rpm.)
'''

import sys
from sys import argv, exit, platform
from os.path import abspath, dirname, join

from .. import NAME


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


# context = (platform, setup)
# platform = windows | mac | linux
# setup = source | frozen
CONTEXT = (get_platform(), get_setup())


# define values for public constants: APP_ROOT, SOURCE, DATA

if CONTEXT[1] == 'source': # run from source
    # running from source
    APP_ROOT = abspath(join(dirname(__file__), '..', '..'))
elif CONTEXT == ('windows', 'binary'):
    APP_ROOT = dirname(argv[0])
else:
    exit('Error %s' % (CONTEXT,))

SOURCE = join(APP_ROOT, NAME)
DATA = join(APP_ROOT, 'data')

