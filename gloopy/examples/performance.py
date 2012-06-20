#! /usr/bin/env python
from __future__ import division
from math import pi, sqrt
from random import choice, uniform

# find gloopy in '../..', so we can run even if Gloopy is not installed
import fixpath

from pyglet.event import EVENT_HANDLED
from pyglet.window import key

from gloopy import Gloopy
from gloopy.color import Color
from gloopy.geom.vector import Vector
from gloopy.geom.orientation import Orientation
from gloopy.gameitem import GameItem
from gloopy.move import Newtonian, Orbit, WobblyOrbit
from gloopy.shapes.cube import Cube


SIZE = 50


def add_items(gloopy, number=None):
    '''
    add 'number' cubes to the world
    if 'number' not specified, default doubles the number of items
    '''
    if number is None:
        number = max(1, len(gloopy.world.items))

    col1 = Color.Random()
    col2 = Color.Random()
    for _ in range(number):
        length = uniform(0, sqrt(SIZE)) ** 2
        color = col1.tinted(col2, abs(length) / SIZE)
        item = GameItem(
            shape=Cube( 1 + length / 5, color ),
            position=Vector.Origin,
            update=Orbit(
                Vector(0, -50/length, 0),
                radius=length,
                angular_velocity=10/length,
                phase=uniform(0, 2*pi),
            ),
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
        axis = Vector.RandomShell(1)
        toggle_attr(gloopy, 'angular_velocity', lambda: (axis, uniform(-5, 5)))

    elif symbol == key._3:
        toggle_attr(gloopy, 'velocity', lambda: Vector.RandomSphere(10))

    elif symbol == key._4:
        toggle_attr(gloopy, 'acceleration', lambda: Vector.RandomSphere(10))

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

    add_items(gloopy, 400)
    toggle_attr(gloopy, 'orientation', Orientation.Random)

    gloopy.window.push_handlers(
        on_key_press=lambda s, m: on_key_press(gloopy, s, m)
    )
    gloopy.camera.update=WobblyOrbit(
        center=Vector.Origin,
        radius=SIZE * 0.8,
        axis=Vector(2, 3, 1),
        angular_velocity=0,
        wobble_size=0.9,
        wobble_freq=pi/10,
    )
    gloopy.camera.look_at = Vector(0, -10, 0)
    gloopy.run()


if __name__ == '__main__':
    main()

