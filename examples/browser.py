#! /usr/bin/env python
from __future__ import division

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
        self.bestiary = {
            key._1: self.add_tetrahedron,
            key._2: self.add_cube,
            key._3: self.add_octahedron,
            key._4: self.add_dodecahedron,
            key._5: self.add_icosahedron,
            key._6: self.add_dualtetrahedron,

            key.S: self.mod_subdivide,
            key.N: self.mod_normalize,
            key.O: self.mod_stellate_out,
            key.I: self.mod_stellate_in,
            key.P: self.mod_stellate_out_central,
            key.L: self.mod_stellate_out_corners,

            key.U: self.mod_color_uniform,
            key.V: self.mod_color_variations,
            key.R: self.mod_color_random,
        }

    def on_key_press(self, symbol, modifiers):
        if symbol in self.bestiary:
            if modifiers & key.MOD_SHIFT:
                self.remove_by_symbol(symbol)
            else:
                item = self.bestiary[symbol]()
                if item:
                    item.key = symbol
            return EVENT_HANDLED

    def add_shape(self, shape):
        item = GameItem(shape=shape)
        self.world.add(item)
        return item


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


    def remove_by_symbol(self, symbol):
        to_remove = [
            item
            for item in self.world
            if item.key == symbol
        ]
        for item in to_remove:
            self.world.remove(item)

    def get_selected_item(self):
        if self.world.items:
            itemid = max(self.world.items.iterkeys())
            return self.world[itemid]

    def mod_shape(self, modifier):
        item = self.get_selected_item()
        modifier(item.shape)
        item.glyph = shape_to_glyph(item.shape)

    def mod_normalize(self): self.mod_shape(normalize)

    def mod_subdivide(self): self.mod_shape(subdivide)

    def stellate_out(self, shape): stellate(shape, 0.5)
    def stellate_in(self, shape): stellate(shape, -0.33)
    def mod_stellate_out(self): self.mod_shape(self.stellate_out)
    def mod_stellate_in(self): self.mod_shape(self.stellate_in)

    def faces_subdivide_central(self, shape):
        for index, face in enumerate(shape.faces):
            if face.source.endswith('subdivide-center'):
                yield index

    def faces_subdivide_corners(self, shape):
        for index, face in enumerate(shape.faces):
            if face.source.endswith('subdivide-corner'):
                yield index

    def stellate_out_central(self, shape):
        stellate(shape, 1, self.faces_subdivide_central(shape))

    def mod_stellate_out_central(self):
        self.mod_shape(self.stellate_out_central)

    def stellate_out_corners(self, shape):
        stellate(shape, 1, self.faces_subdivide_corners(shape))

    def mod_stellate_out_corners(self):
        self.mod_shape(self.stellate_out_corners)

    def mod_color(self, get_color):
        item = self.get_selected_item()
        for face in item.shape.faces:
            face.color = get_color()
        item.glyph = shape_to_glyph(item.shape)

    def mod_color_random(self):
        self.mod_color(Color.Random)

    def mod_color_uniform(self):
        c = Color.Random()
        self.mod_color(lambda: c)

    def mod_color_variations(self):
        self.mod_color(Color.Random().variations().next)



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

