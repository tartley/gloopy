import logging
import sys

from . import VERSION, NAME
from .util.options import Options
from .controller.eventloop import Eventloop


def init_logging():
    logging.basicConfig(
        filename='%s-debug.log' % (NAME,),
        filemode='w',
        level=logging.DEBUG,
    )
    logging.debug('%s v%s' % (NAME, VERSION,))


def main():
    init_logging()
    options = Options(sys.argv)
    try:
        eventloop = Eventloop(options)
        eventloop.prepare(options)
        eventloop.run()
    finally:
        eventloop.stop()

    logging.debug('end of program')

