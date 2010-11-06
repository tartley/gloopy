import logging

# ensure 'import euclid' will use the local copy in 'gloopy/lib/euclid.py'
import sys
from os.path import join
sys.path.append(join('gloopy', 'lib'))

from .controller.eventloop import Eventloop
from .model.world import World
from .util.log import init_log
from .util.options import Options


VERSION = '0.1'

log = None


class Gloopy(object):

    def __init__(self):
        self.options = None
        self.world = None
        self.eventloop = None

        init_log()
        global log
        log = logging.getLogger(__name__)

    def init(self):
        log.info('v%s' % (VERSION,))
        self.options = Options(sys.argv)
        self.world = World()
        self.eventloop = Eventloop(self.world, self.options)

    def start(self):
        self.eventloop.init()
        self.eventloop.start()

    def stop(self):
        self.eventloop.stop()
        
