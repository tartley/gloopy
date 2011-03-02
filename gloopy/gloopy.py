import logging
import sys

from pyglet.window import Window

from .eventloop import Eventloop
from .gameitem import GameItem
from .geom.vector import Vector
from .model.world import World
from .util.log import init_log
from .util.options import Options
from .version import RELEASE


log = None


class Gloopy(object):

    def __init__(self):
        global log
        init_log()
        log = logging.getLogger(__name__)

        self.window = None
        self.world = None
        self.camera = None
        self.eventloop = None
        self.options = Options(sys.argv)

    def init(self):
        log.info('v%s' % (RELEASE,))
        self.world = World()
        self.camera = GameItem(
            position=Vector(0, 0, 10),
            look_at=Vector.Origin,
        )
        self.world.add(self.camera)
        self.window = Window(
            fullscreen=self.options.fullscreen,
            vsync=self.options.vsync,
            visible=False,
            resizable=True)
        self.eventloop = Eventloop(self.world, self.camera, self.options)
        self.eventloop.init(self.window)

    def run(self):
        self.eventloop.start()

