from __future__ import division

import pyglet
from pyglet.event import EVENT_HANDLED

from .util.screenshot import screenshot
from .view.render import Render



def mainloop(world, window, options, camera):

    time = 0.0
    timerate = 1.0

    render = Render(world, window, camera, options)
    render.init()

    def draw():
        render.draw_window(
            (item.position, item.orientation, item.glyph[item.frame])
            for item in world
            if item.glyph and hasattr(item, 'frame') and item.glyph[item.frame]
        )

    window.on_draw = draw

    def on_key_press(symbol, modifiers):
        nonlocal timerate
        key = pyglet.window.key
        if symbol == key.ESCAPE:
            window.dispatch_event('on_close')
        elif symbol == key.F12:
            options.fps = not options.fps
        elif symbol == key.F10:
            window.set_vsync(not window.vsync)
        elif symbol == key.F9:
            screenshot()
        elif symbol == key.ENTER and (modifiers & key.MOD_ALT):
            window.set_fullscreen(not window.fullscreen)
        elif symbol == key.HOME:
            timerate *= 2
        elif symbol == key.END:
            timerate /= 2
        else:
            return
        return EVENT_HANDLED

    window.push_handlers(on_key_press)

    def update(dt):
        nonlocal time, timerate

        dt = min(dt, 1.0 / 30) * timerate
        time += dt

        for item in world:
            if item.update:
                item.update(item, time, dt)
        camera.update(camera, time, dt)

        window.invalid = True

    pyglet.clock.schedule(update)
    pyglet.app.run()

