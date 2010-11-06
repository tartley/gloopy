
# ensure 'import euclid' will use the local copy in 'gloopy/lib/euclid.py'
import sys
from os.path import join
sys.path.append(join('gloopy', 'lib'))

# must be done before importing other modules that use .util.log
from .util.log import init_log
init_log()

from .controller.eventloop import Eventloop
from .model.world import World
from .util.options import Options
from .util.log import log


VERSION = '0.1'


class Gloopy(object):

    def __init__(self):
        self.options = None
        self.world = None
        self.eventloop = None

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
        
