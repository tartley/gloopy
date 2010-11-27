#! /usr/bin/env python
from __future__ import division
from random import choice

import OpenGL
OpenGL.ERROR_CHECKING = __debug__
OpenGL.ERROR_ON_COPY = __debug__

# allow this script to import gloopy from the parent directory, so we can
# run from the 'examples' dir, even if gloopy isn't installed.
import sys
from os.path import abspath, dirname, join
sys.path.insert(0, abspath(join(dirname(__file__), '..')))

from pyglet.event import EVENT_HANDLED
from pyglet.window import key

from gloopy import Gloopy
from gloopy.geom.vec3 import Vec3
from gloopy.geom.orientation import Orientation
from gloopy.model.item.gameitem import GameItem
from gloopy.model.cube import Cube
from gloopy.model.move import Newtonian, WobblyOrbit
from gloopy.util.color import Color
from gloopy.geom.vec3 import origin



SIZE = 20


def add_items(gloopy, number=None):
    '''
    add 'number' cubes to the world
    if 'number' not specified, default doubles the number of items
    '''
    if number is None:
        number = max(1, len(gloopy.world.items))
    shape = Cube(1, Color.Random())
    for _ in range(number):
        item = GameItem(
            shape=shape,
            position=Vec3.RandomSphere(SIZE)
        )
        gloopy.world.add( item )


def remove_items(gloopy, number=None):
    '''
    remove 'number' items from the world
    if number not specified, default removes half the items from the world
    '''
    if number is None:
        number = len(gloopy.world.items) // 2

    while number > 0:
        item = choice( gloopy.world.items.values() )
        gloopy.world.remove( item )
        number -= 1


currently_set = {}

def toggle_attr(gloopy, name, get_value):
    new_state = not currently_set.get(name, False)
    currently_set[name] = new_state
    print name, new_state
    for item in gloopy.world:
        if new_state:
            setattr(item, name, get_value())
        else:
            setattr(item, name, None)


def on_key_press(gloopy, symbol, modifiers):

    if symbol == key.EQUAL:
        add_items(gloopy)

    elif symbol == key.MINUS:
        remove_items(gloopy)

    elif symbol == key.GRAVE:
        toggle_attr(gloopy, 'update', Newtonian)

    elif symbol == key._1:
        toggle_attr(gloopy, 'orientation', Orientation.Random)

    elif symbol == key._2:
        toggle_attr(gloopy, 'angular_velocity', Orientation.Random)

    elif symbol == key._3:
        toggle_attr(gloopy, 'velocity', lambda: Vec3.Random(radius=10))

    elif symbol == key._4:
        toggle_attr(gloopy, 'acceleration', lambda: Vec3.Random(radius=10))

    elif symbol == key.BACKSPACE:
        gloopy.world.items.clear()
        gloopy.world.add(gloopy.camera)

    else:
        return

    return EVENT_HANDLED



def main():
    gloopy = Gloopy()
    gloopy.init()
    gloopy.world.background_color = Color.Random()

    add_items(gloopy, 512)
    toggle_attr(gloopy, 'orientation', Orientation.Random)

    gloopy.eventloop.window.push_handlers(
        on_key_press=lambda s, m: on_key_press(gloopy, s, m)
    )
    gloopy.camera.update=WobblyOrbit(
        origin, 50, Vec3(2, 3, 1),
        wobble_size=0.9, wobble_freq=0.4,
    )
    gloopy.start()
    gloopy.stop()


if __name__ == '__main__':
    main()

