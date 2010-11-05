
import logging
import sys

from os.path import join
sys.path.append(join('gloopy', 'lib'))

from .util.options import Options
from .util import path
from .controller.eventloop import Eventloop


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
    path.init(NAME)
    return Options(sys.argv)


def run(options=None):
    eventloop = Eventloop(options)
    try:
        eventloop.init()
        eventloop.start()
    finally:
        eventloop.stop()
    

