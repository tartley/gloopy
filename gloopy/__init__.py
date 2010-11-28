import logging
import sys

from .controller.eventloop import Eventloop
from .geom.vector import Vector, origin
from .model.item.gameitem import GameItem
from .model.world import World
from .util.log import init_log
from .util.options import Options


VERSION = '0.1'

log = None


class Gloopy(object):

    def __init__(self):
        global log
        init_log()
        log = logging.getLogger(__name__)

        self.options = None
        self.world = None
        self.camera = None
        self.eventloop = None

    def init(self):
        log.info('v%s' % (VERSION,))
        self.options = Options(sys.argv)
        self.world = World()
        self.camera = GameItem(
            position=Vector(0, 0, 10),
            look_at=origin,
        )
        self.eventloop = Eventloop(self.world, self.camera, self.options)
        self.eventloop.init()

    def start(self):
        self.eventloop.start()

    def stop(self):
        self.eventloop.stop()


