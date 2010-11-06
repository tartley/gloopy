
import logging
from os.path import join
import sys

sys.path.append(join('gloopy', 'lib'))

from .controller.eventloop import Eventloop
from .model.world import World
from .util.options import Options
from .util import path


def _init_logging(name):
    logging.basicConfig(
        filename='%s-debug.log' % (name,),
        filemode='w',
        level=logging.DEBUG,
    )


class Gloopy(object):

    def __init__(self, app_name):
        self.app_name = app_name
        self.options = None
        self.world = None
        self.eventloop = None

    def init(self):
        _init_logging(self.app_name)
        path.init(self.app_name)
        self.options = Options(sys.argv)
        self.world = World()
        self.eventloop = Eventloop(self.world, self.options)

    def run(self):
        self.eventloop.init()
        self.eventloop.start()

    def end(self):
        self.eventloop.stop()
        
