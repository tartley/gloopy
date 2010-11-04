#! /usr/bin/env python

import logging
import sys

from os.path import join
sys.path.append(join('gloopy', 'lib'))

from gloopy import VERSION, NAME
from gloopy.controller.eventloop import Eventloop
from gloopy.util.options import Options


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
        eventloop.prepare()
        eventloop.start()
    finally:
        eventloop.stop()


if __name__ == '__main__':
    main()

