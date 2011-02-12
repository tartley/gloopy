#! /usr/bin/env python
from __future__ import division
from random import randint

from pyglet.event import EVENT_HANDLED
from pyglet.window import key

# let this script run within the 'examples' dir, even if Gloopy is not installed
import fixpath; fixpath

from gloopy import Gloopy
from gloopy.color import Color
from gloopy.geom.vector import origin, Vector
from gloopy.model.item.gameitem import GameItem
from gloopy.model.move import WobblyOrbit
from gloopy.shapes.shape import shape_to_glyph
from gloopy.shapes.cube import Cube
from gloopy.shapes.extrude import extrude
from gloopy.shapes.dodecahedron import Dodecahedron
from gloopy.shapes.icosahedron import Icosahedron
from gloopy.shapes.octahedron import Octahedron
from gloopy.shapes.tetrahedron import Tetrahedron, DualTetrahedron
from gloopy.shapes.normalize import normalize
from gloopy.shapes.subdivide import subdivide
from gloopy.shapes.stellate import stellate



class KeyHandler(object):

    def __init__(self, world):
        self.world = world
        self.faces_suffix = ''
        self.keys_add = {
            key._1: self.add_tetrahedron,
            key._2: self.add_cube,
            key._3: self.add_octahedron,
            key._4: self.add_dodecahedron,
            key._5: self.add_icosahedron,
            key._6: self.add_dualtetrahedron,
        }
        self.keys_modify = {
            key.N: self.mod_normalize,
            key.S: self.mod_subdivide,
            key.O: self.mod_stellate_out,
            key.I: self.mod_stellate_in,
            key.E: self.mod_extrude,

            key.U: self.mod_color_uniform,
            key.V: self.mod_color_variations,
            key.R: self.mod_color_random,
            key.BACKSPACE: self.remove,
        }
        self.keys_faces = {
            key.A: lambda: self.set_faces_suffix(None),
            key.S: lambda: self.set_faces_suffix('subdivide-center'),
            key.D: lambda: self.set_faces_suffix('subdivide-corner'),
            key.E: lambda: self.set_faces_suffix('extrude-end'),
            key.R: lambda: self.set_faces_suffix('extrude-side'),
        }

    def on_key_press(self, symbol, modifiers):
        if modifiers & key.MOD_SHIFT:
            if symbol in self.keys_faces:
                self.keys_faces[symbol]()
                return EVENT_HANDLED
        else:
            if symbol in self.keys_add:
                self.keys_add[symbol]()
                return EVENT_HANDLED
            if symbol in self.keys_modify:
                self.keys_modify[symbol](self.get_selected_item())
                return EVENT_HANDLED

    def get_selected_item(self):
        if self.world.items:
            itemid = max(self.world.items.iterkeys())
            return self.world[itemid]

    def add_shape(self, shape):
        item = GameItem(shape=shape)
        self.world.add(item)
        return item

    def remove(self, item):
        if item:
            self.world.remove(item)


    def add_tetrahedron(self):
        return self.add_shape(Tetrahedron(1, Color.Random()))

    def add_cube(self):
        return self.add_shape(Cube(1, Color.Random()))

    def add_octahedron(self):
        return self.add_shape(Octahedron(1, Color.Random()))

    def add_dodecahedron(self):
        return self.add_shape(Dodecahedron(1, Color.Random()))

    def add_icosahedron(self):
        return self.add_shape(Icosahedron(1, Color.Random()))

    def add_dualtetrahedron(self):
        return self.add_shape(DualTetrahedron(1, Color.Random()))


    def set_faces_suffix(self, suffix):
        self.faces_suffix = suffix

    def faces_endswith(self, shape, suffix):
        if suffix:
            return [
                index
                for index, face in enumerate(shape.faces)
                if face.source.endswith(suffix)
            ]

    def mod_normalize(self, item):
        normalize(item.shape)

    def mod_shape(self, modifier, item, *args):
        faces = self.faces_endswith(item.shape, self.faces_suffix)
        modifier(item.shape, faces, *args)
        item.glyph = shape_to_glyph(item.shape)

    def mod_subdivide(self, item):
        self.mod_shape(subdivide, item)
        self.set_faces_suffix('subdivide-center')

    def mod_stellate_out(self, item):
        self.mod_shape(stellate, item, 0.5)
        self.set_faces_suffix('stellate')

    def mod_stellate_in(self, item):
        self.mod_shape(stellate, item, -0.33)
        self.set_faces_suffix('stellate')
        
    def mod_extrude(self, item):
        self.mod_shape(extrude, item, 0.5)
        self.set_faces_suffix('extrude-end')


    def mod_color(self, item, get_color):
        for face in item.shape.faces:
            face.color = get_color()
        item.glyph = shape_to_glyph(item.shape)

    def mod_color_random(self, item):
        self.mod_color(item, Color.Random)

    def mod_color_uniform(self, item):
        c = Color.Random()
        self.mod_color(item, lambda: c)

    def mod_color_variations(self, item):
        self.mod_color(item, Color.Random().variations().next)



class Application(object):

    def __init__(self):
        self.gloopy = None

    def run(self):
        self.gloopy = Gloopy()
        self.gloopy.init()
        self.gloopy.world.background_color = Color.Orange
        self.gloopy.camera.update=WobblyOrbit(
            center=origin,
            radius=3,
            axis=Vector(2, -3, 1),
            angular_velocity=0.8,
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

