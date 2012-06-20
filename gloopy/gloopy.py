from __future__ import division

import logging
import sys

import pyglet
from pyglet.window import key

from .gameitem import GameItem
from .geom.vector import Vector
from .world import World
from .util.log import init_log
from .util.options import Options
from .util.screenshot import screenshot
from .view.render import Render
from .version import RELEASE


log = None


class Gloopy(object):
    '''
    .. function:: __init__()
        
        Parses the command-line options, stores results in self.options
    '''
    def __init__(self):
        global log
        init_log()
        log = logging.getLogger(__name__)

        self.window = None
        self.world = None
        self.camera = None
        self.render = None
        self.options = Options(sys.argv)


    def init(self, window=None):
        '''
        Initialise Gloopy. Must be called before calling :func:`run` to start
        the event loop. You may pass in a pyglet.window.Window instance, or
        if it is None, we will create a (non-visible) one, using self.options
        to determine its parameters.
        '''
        log.info('v%s' % (RELEASE,))
        if window is None:
            window = pyglet.window.Window(
                fullscreen=self.options.fullscreen,
                vsync=self.options.vsync,
                visible=False,
                resizable=True,
            )
        self.window = window
            
        self.world = World()

        self.camera = GameItem(
            position=Vector(0, 0, 10),
            look_at=Vector.origin,
        )
        self.world.add(self.camera)
        self.render = Render(self.world, self.window, self.camera, self.options)
        self.render.init()

        def draw():
            self.render.draw_window(
                (item.position, item.orientation, item.glyph[item.frame])
                for item in self.world if item.glyph
            )

        self.window.on_draw = draw
        self.window.on_key_press = self.on_key_press


    def run(self):
        '''
        Schedules calls to self.update, makes window visible and starts the
        event loop by calling pyglet.app.run()
        '''
        log.info('start')
        pyglet.clock.schedule(self.update)
        self.window.set_visible()
        self.window.invalid = False
        try:
            pyglet.app.run()
            log.info('stop')
        except:
            log.error('abnormal stop')
            raise
        finally:
            if self.window:
                self.window.close()


    def update(self, dt):
        '''
        Called before every screen refresh,
        '''
        self.world.update_all(min(dt, 1 / 30.0))
        self.window.invalid = True


    def on_key_press(self, symbol, modifiers):
        '''
        Handle key presses:

        ========= ==================
        escape    quit
        --------- ------------------
        f12       toggle fps display
        --------- ------------------
        f9        take screenshot
        --------- ------------------
        alt-enter toggle fullscreen
        ========= ==================
        '''
        if symbol == key.ESCAPE:
            self.window.dispatch_event('on_close')
        elif symbol == key.F12:
            self.options.fps = not self.options.fps
        elif symbol == key.ENTER and (modifiers & key.MOD_ALT):
            log.info('fullscreen: %s' % (not self.window.fullscreen,))
            self.window.set_fullscreen(not self.window.fullscreen)
        elif symbol == key.F9:
            screenshot()

