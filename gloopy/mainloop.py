from __future__ import division

import pyglet

from .util.screenshot import screenshot
from .view.render import Render


time = 0.0


def mainloop(world, window, options, camera):

    render = Render(world, window, camera, options)
    render.init()

    def draw():
        render.draw_window(
            (item.position, item.orientation, item.glyph[item.frame])
            for item in world
            if item.glyph and hasattr(item, 'frame') and item.glyph[item.frame]
        )

    window.on_draw = draw

    def on_key_press(self, symbol, modifiers):
        key = pyglet.window.key
        if symbol == key.ESCAPE:
            self.window.dispatch_event('on_close')
        elif symbol == key.F12:
            self.options.fps = not self.options.fps
        elif symbol == key.F11:
            self.window.set_vsync(not self.window.vsync)
        elif symbol == key.F9:
            screenshot()
        elif symbol == key.ENTER and (modifiers & key.MOD_ALT):
            self.window.set_fullscreen(not self.window.fullscreen)

    def update(dt):
        global time

        dt = min(dt, 1.0 / 30)
        time += dt

        for item in world:
            if item.update:
                item.update(item, time, dt)
        camera.update(camera, time, dt)

        window.invalid = True

    pyglet.clock.schedule(update)

    pyglet.app.run()

