#!/usr/bin/env python

import pyglet

def main():

    display = pyglet.canvas.get_display()
    screens = display.get_screens()
    for index, screen in enumerate(screens):
        print(f'Screen {index}: {screen.width}x{screen.height}')
    surface = pyglet.window.Window(
        fullscreen=True,
        vsync=True,
        screen=screens[1],
    )

    flash = False

    @surface.event
    def on_draw():
        nonlocal flash
        bgcolor = (0.7, 0.7, 0, 1) if flash else (0, 0.2, 0.2, 1)
        flash = not flash
        pyglet.gl.glClearColor(*bgcolor)
        surface.clear()

    def update(_):
        pass

    pyglet.clock.schedule(update)
    pyglet.app.run()



if __name__ == '__main__':
    main()

