'''
Access to all application path values should go via this module. In
particular, use this module instead of using __file__ to locate resources,
since resources will be separated from source code under some circumstances
(e.g. when installed from an rpm.)
See excellent talk on cross-platform development using these ideas at:
http://us.pycon.org/2010/conference/schedule/event/38/

| `CONTEXT`: tuple of (platform, setup), where:
|     `platform`: windows | mac | linux
|     `setup`: source | frozen

| `ROOT`: application root directory
| `DATA`: application data directory
| `SOURCE`: root of application source code
| `SHADERS`: location of application shader source code
'''

import sys
from sys import argv, exit, platform
from os.path import abspath, dirname, join

# TODO: Maybe Context should be a mini class, with named fields. Or named tuple

# context = (platform, setup)
# platform = windows | mac | linux
# setup = source | frozen
CONTEXT = None

# directories we might be interested in
ROOT = None
DATA = None


def _get_platform():
    if platform.startswith('win'):
        return 'windows'
    elif platform.startswith('darwin'):
        return 'mac'
    return 'linux'

def _get_setup():
    if hasattr(sys, 'frozen'):
        # ie. output of py2exe, py2app or similar
        return 'binary'
    return 'source'


CONTEXT = (_get_platform(), _get_setup())

if CONTEXT[1] == 'source':
    ROOT = abspath(join(dirname(__file__), '..', '..'))
elif CONTEXT == ('windows', 'binary'):
    ROOT = dirname(argv[0])
else:
    exit('Error %s' % (CONTEXT,))

DATA = join(ROOT, 'data')
SOURCE = join(ROOT, 'gloopy')
SHADERS = join(DATA, 'shaders')

