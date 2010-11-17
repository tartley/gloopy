#! /usr/bin/env python
from __future__ import division
from math import sqrt
from random import choice, randint, uniform

# allow this script to import gloopy from the parent directory, so we can
# run from the 'examples' dir, even if gloopy isn't installed.
import sys
from os.path import abspath, dirname, join
sys.path.insert(0, abspath(join(dirname(__file__), '..')))

from pyglet.event import EVENT_HANDLED
from pyglet.window import key

from gloopy import Gloopy
from gloopy.lib.euclid import Quaternion, Vector3
from gloopy.model.item.gameitem import GameItem
from gloopy.model.cube import Cube
from gloopy.model.move import Newtonian, WobblyOrbit
from gloopy.model.shape import Shape, MultiShape
from gloopy.util.color import Color
from gloopy.util.vectors import (
    origin, orientation_random, vec3_random_cube, x_axis, y_axis, z_axis,
)
from gloopy.view.glyph import Glyph



SIZE = 30


def add_items(gloopy, number=None):
    '''
    add 'number' cubes to the world
    '''
    if number is None:
        number = max(1, len(gloopy.world.items))
    shape = Cube(1, Color.Random())
    for _ in range(number):
        item = GameItem(
            shape=shape,
            position=vec3_random_cube(SIZE, ints=True),
        )
        gloopy.world.add( item )


def remove_items(gloopy, number=None):
    '''
    remove 'number' items from the world
    '''
    if number is None:
        number = len(gloopy.world.items) // 2

    while number > 0:
        item = choice( gloopy.world.items.values() )
        gloopy.world.remove( item )
        number -= 1


#def add_many_gameitems(world, number, orient=False, newtonian=False):
    #shape = Cube(1, Color.Green)
    #for _ in range(number):
        #item = GameItem(
            #shape=shape,
            #position=vec3_random(sqrt(uniform(0, SIZE ** 2))),
        #)
        #if orient:
            #item.orientation=orientation_random()
        #if newtonian:
            #item.update=Newtonian()
            #velocity=vec3_random(10)
            #args['update'.update(dict(
                #update=Newtonian(),
                #position=Vector3(0, 0, 0),
                #velocity=velocity,
                ##acceleration=-velocity / 3,
                #orientation=orientation_random(),
                #angular_velocity=orientation_random(uniform(0, 10)),
            #))
        #else:
            #args = dict(
                #shape=shape,
                #position=vec3_random(sqrt(uniform(0, SIZE ** 2))),
                #orientation=orientation_random(),
            #)
        #world.add( item )


def on_key_press(gloopy, symbol, modifiers):

    if symbol == key.EQUAL:
        add_items(gloopy)

    elif symbol == key.MINUS:
        remove_items(gloopy)

    #if symbol == key._1:
        #gloopy.world.items.clear()
        #add_many_gameitems(gloopy.world, 400)
        #gloopy.world.add(gloopy.camera)

    #elif symbol == key._2:
        #gloopy.world.items.clear()
        #add_many_gameitems(gloopy.world, 400, orient=True)
        #gloopy.world.add(gloopy.camera)

    #elif symbol == key._3:
        #gloopy.world.items.clear()
        #add_many_gameitems(gloopy.world, 400, newtonian=True)
        #gloopy.world.add(gloopy.camera)

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
    gloopy.eventloop.window.push_handlers(
        on_key_press=
        lambda symbol, modifiers: on_key_press(gloopy, symbol, modifiers)
    )
    gloopy.camera.update=WobblyOrbit(
        origin, 50, Vector3(2, 3, 1),
        wobble_size=0.9, wobble_freq=0.4,
    )
    gloopy.start()
    gloopy.stop()


if __name__ == '__main__':
    main()

