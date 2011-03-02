'''
Users of Gloopy shouldn't have to mess with this much.
'''

from __future__ import division
import logging

from pyglet import app, clock
from pyglet.window import key

from .view.render import Render
from .util.screenshot import screenshot


log = logging.getLogger(__name__)


class Eventloop(object):
    '''
    Schedules world updates, screen redraws, and application-level key
    handling.

    .. function:: __init__(world, camera, options)

        ``world``: instance of :class:`~gloopy.model.world.World`.

        ``camera``: instance of :class:`~gloopy.gameitem.GameItem` that
                    represents the camera.
        
        ``options``: instance of :class:`~gloopy.util.options.Options`
    '''

    def __init__(self, world, camera, options):
        self.world = world
        self.camera = camera
        self.options = options

        self.window = None
        self.render = None
        self.fpss = []
        self.time = 0.0


    def init(self, window):
        '''
        Attach handlers for window.on_draw and on_key_press
        '''
        log.info('init')
        self.window = window
        self.render = Render(self.window, self.camera, self.options)
        self.render.init()
        self.window.on_draw = lambda: self.render.draw(self.world)
        self.window.on_key_press = self.on_key_press


    def start(self):
        '''
        Schedules calls to self.update, makes window visible and starts the
        event loop by calling pyglet.app.run()
        '''
        log.info('start')
        clock.schedule(self.update)
        self.window.set_visible()
        self.window.invalid = False
        try:
            app.run()
            log.info('stop')
        except:
            log.error('abnormal stop')
        finally:
            if self.window:
                self.window.close()


    def update(self, dt):
        '''
        Called before every screen refresh,
        '''
        dt = min(dt, 1 / 30)
        self.time += dt
        self.world.update_all(self.time, dt)
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

