from __future__ import division

import logging
import sys

import pyglet
from pyglet.event import EVENT_HANDLED
from pyglet.window import Window

from euclid import Vector3

from ..model.cameraman import CameraMan
from ..model.item.gameitem import GameItem
from ..model.item.player import Player
from ..model.world import World
from ..view.render import Render
from ..util.vectors import origin


class Eventloop(object):

    def __init__(self, options):
        self.options = options
        self.window = None
        self.fpss = []
        self.time = 0.0
        self.level = None


    def prepare(self, options):
        self.window = Window(
            fullscreen=options.fullscreen,
            vsync=options.vsync,
            visible=False,
            resizable=True)
        self.window.on_draw = self.draw_window

        self.world = World()
        self.player = Player(self.world)
        self.camera = GameItem(
            position=Vector3(1, 2, 3),
            look_at=origin,
            update=CameraMan(self.player, (3, 2, 0)),
        )
        pyglet.clock.schedule_once(
            lambda *_: self.world.add(self.player),
            2.0,
        )
        
        self.update(1/60)

        self.render = Render(self.world, self.window, self.camera)
        self.render.init()


    def run(self):
        pyglet.clock.schedule(self.update)
        self.window.set_visible()
        self.window.invalid = False
        pyglet.app.run()


    def update(self, dt):
        if self.options.print_fps:
            self.fpss.append(1/max(1e-6, dt))
        dt = min(dt, 1 / 30)
        self.time += dt

        for item in self.world:
            if hasattr(item, 'update'):
                item.update(item, dt, self.time)

        self.window.invalid = True


    def draw_window(self):
        self.window.clear()
        self.render.draw_world()
        if self.options.display_fps:
            self.render.draw_hud()
        self.window.invalid = False
        return EVENT_HANDLED


    def stop(self):
        if self.window:
            self.window.close()
        if self.options.print_fps:
            print '  '.join("%6.1f" % (dt, ) for dt in self.fpss)

