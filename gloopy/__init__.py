import logging

# ensure 'import euclid' will use the local copy in 'gloopy/lib/euclid.py'
import sys
from os.path import join
sys.path.append(join('gloopy', 'lib'))

from .controller.eventloop import Eventloop
from .lib.euclid import Vector3
from .model.item.gameitem import GameItem
from .model.move.orbit import WobblyOrbit
from .model.world import World
from .util.log import init_log
from .util.options import Options
from .util.vectors import origin


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
            position=Vector3(0, 0, 10),
            look_at=origin,
        )
        self.world.add( self.camera )
        self.eventloop = Eventloop(self.world, self.options)

    def start(self):
        self.eventloop.init( self.camera )
        self.eventloop.start()

    def stop(self):
        self.eventloop.stop()
        
