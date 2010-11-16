from __future__ import division
import logging

import pyglet
from pyglet.window import Window

from ..view.render import Render


log = logging.getLogger(__name__)


class Eventloop(object):

    def __init__(self, world, options):
        self.world = world
        self.options = options
        self.window = None
        self.fpss = []
        self.time = 0.0


    def init(self, camera):
        log.info('init')
        self.window = Window(
            fullscreen=self.options.fullscreen,
            vsync=self.options.vsync,
            visible=False,
            resizable=True)
        self.render = Render(self.window, camera, self.options)
        self.render.init()
        self.window.on_draw = lambda: self.render.draw(self.world)


    def start(self):
        log.info('start')
        pyglet.clock.schedule(self.update)
        self.window.set_visible()
        self.window.invalid = False
        pyglet.app.run()


    def update(self, dt):
        dt = min(dt, 1 / 30)
        self.time += dt

        self.world.update(self.time, dt)
        self.window.invalid = True


    def stop(self):
        log.info('stop')
        if self.window:
            self.window.close()

