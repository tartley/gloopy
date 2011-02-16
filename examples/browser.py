#! /usr/bin/env python
from __future__ import division

from pyglet.event import EVENT_HANDLED
from pyglet.window import key

# let this script run within the 'examples' dir, even if Gloopy is not installed
import fixpath; fixpath

from gloopy import Gloopy
from gloopy.color import Color
from gloopy.geom.vector import Vector
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

    def __init__(self, world, render, camera):
        self.world = world
        self.world.update += self.update
        self.render = render
        self.camera = camera

        self.keys = {
            key._1: self.add_tetrahedron,
            key._2: self.add_cube,
            key._3: self.add_octahedron,
            key._4: self.add_dodecahedron,
            key._5: self.add_icosahedron,
            key._6: self.add_dualtetrahedron,
            key._7: self.add_koche_tetra,

            key.N: self.mod_normalize,
            key.S: self.mod_subdivide,
            key.O: self.mod_stellate_out,
            key.I: self.mod_stellate_in,
            key.E: self.mod_extrude,
            key.C: self.mod_color,

            key.BACKSPACE: self.remove,
            key.B: self.toggle_backface_culling,
            key.PAGEDOWN: lambda: self.camera_orbit(0.5),
            key.PAGEUP: lambda: self.camera_orbit(2.0),
        }
        self.keys_shift = {
            key.A: lambda: self.set_faces_suffix(''),
            key.S: lambda: self.set_faces_suffix('subdivide-center'),
            key.D: lambda: self.set_faces_suffix('subdivide-corner'),
            key.E: lambda: self.set_faces_suffix('extrude-end'),
            key.R: lambda: self.set_faces_suffix('extrude-side'),
        }
        self.faces_suffix = ''
        self.camera_radius = 3


    def on_key_press(self, symbol, modifiers):
        if modifiers & key.MOD_SHIFT:
            if symbol in self.keys_shift:
                self.keys_shift[symbol]()
                return EVENT_HANDLED
        else:
            if symbol in self.keys:
                self.keys[symbol]()
                return EVENT_HANDLED

    def get_selected_item(self):
        if self.world.items:
            itemid = max(self.world.items.iterkeys())
            return self.world[itemid]

    def add_shape(self, shape):
        item = GameItem(shape=shape)
        self.world.add(item)
        return item

    def remove(self):
        item = self.get_selected_item()
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

    def add_koche_tetra(self):
        color1 = Color.Random()
        color2 = Color.Random()
        shape = Tetrahedron(1, color1)
        for i in range(6):
            subdivide(shape, color=color1.tinted(color2, i/5))
            stellate(shape, self.faces_endswith(shape, 'subdivide-center'), 1)
        return self.add_shape(shape)


    def set_faces_suffix(self, suffix):
        self.faces_suffix = suffix

    def faces_endswith(self, shape, suffix):
        return [
            index
            for index, face in enumerate(shape.faces)
            if face.source.endswith(suffix)
        ]

    def mod_normalize(self):
        '''
        This makes a mess when the selected shape has longer edges of a
        single face which abut a chain of shorter edges of smaller faces.
        '''
        item = self.get_selected_item()
        normalize(item.shape)
        item.glyph = shape_to_glyph(item.shape)

    def mod_shape(self, modifier, *args):
        item = self.get_selected_item()
        faces = self.faces_endswith(item.shape, self.faces_suffix)
        modifier(item.shape, faces, *args)
        item.glyph = shape_to_glyph(item.shape)

    def mod_subdivide(self):
        self.mod_shape(subdivide)
        self.set_faces_suffix('subdivide-center')

    def mod_stellate_out(self):
        self.mod_shape(stellate, 0.5)
        self.set_faces_suffix('stellate')

    def mod_stellate_in(self):
        self.mod_shape(stellate, -0.33)
        self.set_faces_suffix('stellate')

    def mod_extrude(self):
        self.mod_shape(extrude, 0.5)
        self.set_faces_suffix('extrude-end')

    def recolor(self, shape, faces, color):
        for face_index in faces:
            shape.faces[face_index].color = color

    def mod_color(self):
        self.mod_shape(self.recolor, Color.Random())


    def toggle_backface_culling(self):
        self.render.backface_culling = not self.render.backface_culling

    def camera_orbit(self, factor):
        self.camera_radius *= factor

    def update(self, time, dt):
        rate = 10.0 * dt
        self.camera.update.radius += (
            self.camera_radius - self.camera.update.radius) * rate


class Application(object):

    def __init__(self):
        self.gloopy = None

    def run(self):
        self.gloopy = Gloopy()
        self.gloopy.init()
        self.gloopy.world.background_color = Color.Orange
        self.gloopy.camera.update=WobblyOrbit(
            center=Vector.Origin,
            radius=3,
            axis=Vector(2, -3, 1),
            angular_velocity=0.8,
            wobble_size=0.0,
            wobble_freq=1,
        )
        self.gloopy.camera.look_at = Vector(0, 0, 0)
        
        self.keyhandler = KeyHandler(
            self.gloopy.world,
            self.gloopy.eventloop.render,
            self.gloopy.camera,
        )
        self.gloopy.eventloop.window.push_handlers(self.keyhandler)

        try:
            self.gloopy.start()
        finally:
            self.gloopy.stop()


if __name__ == '__main__':
    Application().run()

