
import logging
import sys

from os.path import join
sys.path.append(join('gloopy', 'lib'))

from .util.options import Options


NAME = 'gloopy'
VERSION = '0.1'


def _init_logging():
    logging.basicConfig(
        filename='%s-debug.log' % (NAME,),
        filemode='w',
        level=logging.DEBUG,
    )
    logging.debug('%s v%s' % (NAME, VERSION,))


def init():
    _init_logging()
    return Options(sys.argv)

