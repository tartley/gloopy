#! /usr/bin/env python
from __future__ import division
import logging
from random import randrange, shuffle
import sys

import fixpath; fixpath

from pyglet.event import EVENT_HANDLED
from pyglet.window import key

from gloopy import Gloopy
from gloopy.color import Color
from gloopy.geom.vector import origin, Vector
from gloopy.model.item.gameitem import GameItem
from gloopy.model.move import WobblyOrbit
from gloopy.shapes.shape import shape_to_glyph
from gloopy.shapes.cube import Cube, Cuboid
from gloopy.shapes.dodecahedron import Dodecahedron
from gloopy.shapes.icosahedron import Icosahedron
from gloopy.shapes.octahedron import Octahedron
from gloopy.shapes.tetrahedron import Tetrahedron, DualTetrahedron
from gloopy.shapes.sphere import subdivided, normalize, nest
from gloopy.shapes.stellate import stellate
#from gloopy.shapes.truncate import truncate


log = logging.getLogger(__name__)


class KeyHandler(object):

    def __init__(self, world):
        self.world = world
        self.bestiary = {
            key._1: lambda symbol:
                self.add_shape(Tetrahedron(1, Color.Random()), key=symbol),
            key._2: lambda symbol:
                self.add_shape(Cube(1, Color.Random()), key=symbol),
            key._3: lambda symbol:
                self.add_shape(Octahedron(1, Color.Random()), key=symbol),
            key._4: lambda symbol:
                self.add_shape(Dodecahedron(1, Color.Random()), key=symbol),
            key._5: lambda symbol:
                self.add_shape(Icosahedron(1, Color.Random()), key=symbol),
            #key._6: self.add_cuboid,
            key._7: lambda symbol:
                self.add_shape(DualTetrahedron(1, Color.Random()), key=symbol),
            key.S: self.mod_subdivide,
            key.N: self.mod_normalize,
            key.O: self.mod_stellate,
            key.I: self.mod_stellate_in,
            key.U: self.mod_color_uniform,
            key.V: self.mod_color_variations,
            key.R: self.mod_color_random,
        }

    def on_key_press(self, symbol, modifiers):
        try:
            if symbol in self.bestiary:
                if modifiers & key.MOD_SHIFT:
                    self.remove_by_symbol(symbol)
                else:
                    self.bestiary[symbol](symbol)
                return EVENT_HANDLED
        except Exception as e:
            raise(e)

    def add_shape(self, shape, **kwargs):
        self.world.add(
            GameItem(
                shape=shape,
                **kwargs
            )
        )

    def remove_by_symbol(self, symbol):
        to_remove = [
            item
            for item in self.world
            if item.key == symbol
        ]
        for item in to_remove:
            self.world.remove(item)

    #def add_cuboid(self, symbol):
        #dimensions = [randrange(1, 3), randrange(2, 8), randrange(2, 8)]
        #shuffle(dimensions)
        #self.add_shape(
            #symbol,
            #Cuboid(*dimensions, colors=Color.Random()),
            #position=(randrange(-20,20), randrange(-20,20), randrange(-20,20)),
        #)

    def get_selected_item(self):
        if self.world.items:
            itemid = max(self.world.items.iterkeys())
            return self.world[itemid]

    def mod_shape(self, modifier):
        item = self.get_selected_item()
        item.shape = modifier(item.shape)
        item.glyph = shape_to_glyph(item.shape)

    def mod_subdivide(self, _):
        self.mod_shape(subdivided)

    def mod_normalize(self, _):
        self.mod_shape(normalize)

    def mod_spike(self, _):
        pass
        # TODO: peturb the height of existing vertices     
        # maybe at first just have spike_in and spike_out, that
        # move the positions of every 4th vertex?

    def mod_stellate(self, _):
        self.mod_shape(lambda s: stellate(s, 1))

    def mod_stellate_in(self, _):
        self.mod_shape(lambda s: stellate(s, -0.5))
               
    def mod_color_random(self, _):
        item = self.get_selected_item()
        for face in item.shape.faces:
            face.color = Color.Random()
        item.glyph = shape_to_glyph(item.shape)

    def mod_color_uniform(self, _):
        item = self.get_selected_item()
        color = Color.Random()
        for face in item.shape.faces:
            face.color = color
        item.glyph = shape_to_glyph(item.shape)

    def mod_color_variations(self, _):
        item = self.get_selected_item()
        colors = Color.Random().variations()
        for face in item.shape.faces:
            face.color = colors.next()
        item.glyph = shape_to_glyph(item.shape)


class Application(object):

    def __init__(self):
        self.gloopy = None

    def run(self):
        self.gloopy = Gloopy()
        self.gloopy.init()
        self.gloopy.world.background_color = Color.Orange
        self.gloopy.camera.update=WobblyOrbit(
            center=origin,
            radius=9,
            axis=Vector(2, -3, 1),
            angular_velocity=0.2,
            wobble_size=0.0,
            wobble_freq=1,
        )
        self.gloopy.camera.look_at = Vector(0, 0, 0)
        
        self.keyhandler = KeyHandler(self.gloopy.world)
        self.gloopy.eventloop.window.push_handlers(self.keyhandler)

        try:
            self.gloopy.start()
        finally:
            self.gloopy.stop()


if __name__ == '__main__':
    Application().run()

