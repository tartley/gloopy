#! /usr/bin/env python
from __future__ import division
from random import randint, uniform

from pyglet.event import EVENT_HANDLED
from pyglet.window import key

# find gloopy in '../..', so we can run even if Gloopy is not installed
import fixpath

from gloopy import Gloopy
from gloopy.color import Color
from gloopy.geom.vector import Vector
from gloopy.geom.orientation import Orientation
from gloopy.gameitem import GameItem
from gloopy.move import Spinner, WobblySpinner, WobblyOrbit
from gloopy.shapes.cube import Cube, TruncatedCube, SpaceStation
from gloopy.shapes.cube_groups import (
    CubeCross, CubeCorners, CubeGlob, RgbCubeCluster,
)
from gloopy.shapes.dodecahedron import Dodecahedron
from gloopy.shapes.extrude import extrude
from gloopy.shapes.icosahedron import Icosahedron
from gloopy.shapes.normalize import normalize
from gloopy.shapes.octahedron import Octahedron
from gloopy.shapes.ring import Ring, TriRings
from gloopy.shapes.shape_to_glyph import shape_to_glyph
from gloopy.shapes.stellate import stellate
from gloopy.shapes.subdivide import subdivide
from gloopy.shapes.tetrahedron import Tetrahedron, DualTetrahedron


class KeyHandler(object):

    def __init__(self, world, render, camera):
        self.world = world
        self.world.update += self.world_update
        self.render = render
        self.camera = camera
        self.coaxials = set()

        self.keys = {
            key._1: lambda: self.add_shape(Tetrahedron(1, Color.Random())),
            key._2: lambda: self.add_shape(Cube(1, Color.Random())),
            key._3: lambda: self.add_shape(Octahedron(1, Color.Random())),
            key._4: lambda: self.add_shape(Dodecahedron(1, Color.Random())),
            key._5: lambda: self.add_shape(Icosahedron(1, Color.Random())),
            key._6: lambda: self.add_shape(DualTetrahedron(1, Color.Random())),
            key._7: lambda: self.add_shape(
                TruncatedCube(1, 0.5, Color.Cyan, Color.Blue),
            ),
            key._8: lambda: self.add_shape( 
                SpaceStation(1.1),
                update=Spinner(Vector.XAxis, speed=1),
            ),

            key.Q: lambda: self.add_shape(
                CubeCross(1, Color.Red, Color.Red.tinted(Color.Orange)),
            ),
            key.W: lambda: self.add_shape(
                CubeCorners(
                    1, Color.Yellow.tinted(Color.White), Color.Yellow
                ),
            ),
            key.E: lambda: self.add_shape(
                Ring(Cube(1, Color.Green), 2, 13),
                update=WobblySpinner(speed=1),
            ),
            key.R: lambda: self.add_shape(
                Ring(
                    TruncatedCube(1, 0.67, Color.SeaGreen, Color.Periwinkle),
                    3.45, 25
                ),
                update=Spinner(axis=Vector.XAxis, speed=0.5),
            ),
            key.T: lambda: self.add_shape(
                TriRings(Cube(1, Color.DarkTeal), 6, 32),
                update=WobblySpinner(speed=-0.2),
            ),
            key.Y: lambda: self.add_shape(
                shape=TriRings(
                    CubeCorners(1, Color.Lavender, Color.Gold),
                    8, 24),
                update=WobblySpinner(speed=-1),
            ),
            key.U: self.add_coaxial_rings,

            key.Z: lambda: self.add_shape(
                CubeGlob(40, 4000, Color.Red)
            ),
            key.X: lambda: self.add_shape( RgbCubeCluster(1, 40, 4000) ),
            key.C: self.add_koche_tetra,

            key.BACKSPACE: self.remove,
            key.F11: self.toggle_backface_culling,
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
        self.keys_alt = {
            key.N: self.mod_normalize,
            key.S: self.mod_subdivide,
            key.O: self.mod_stellate_out,
            key.I: self.mod_stellate_in,
            key.E: self.mod_extrude,
            key.C: self.mod_color,
            key.R: self.mod_spin,
        }
        self.faces_suffix = ''
        self.camera_radius = 3


    def world_update(self, time, dt):
        if self.camera.update:
            rate = 3 * dt
            self.camera.update.radius += (
                self.camera_radius - self.camera.update.radius) * rate


    def on_key_press(self, symbol, modifiers):
        if modifiers & key.MOD_SHIFT:
            if symbol in self.keys_shift:
                self.keys_shift[symbol]()
                return EVENT_HANDLED
        elif modifiers & key.MOD_ALT:
            if symbol in self.keys_alt:
                self.keys_alt[symbol]()
                return EVENT_HANDLED
        else:
            if symbol in self.keys:
                self.keys[symbol]()
                return EVENT_HANDLED

    def get_selected_item(self):
        if self.world.items:
            itemid = max(self.world.items.iterkeys())
            item = self.world[itemid]
            if item.glyph:
                return self.world[itemid]

    def add_shape(self, shape, **kwargs):
        item = GameItem(shape=shape, **kwargs)
        self.world.add(item)
        return item

    def remove(self):
        item = self.get_selected_item()
        if item:
            self.world.remove(item)


    def add_coaxial_rings(self):
        height = randint(-10, 11)
        radius = randint(3, 10)
        color1 = Color.Blue.tinted(Color.Grey, radius/10)
        self.add_shape(
            shape=Ring(
                CubeCross(4, color1, color1.inverted()),
                radius * 6, 
                int(radius * 5),
            ),
            position=Vector(0, height * 6, 0),
            orientation=Orientation(Vector.YAxis),
            update=Spinner(Vector.YAxis, speed=uniform(-1, 1)),
        )

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
        This makes a mess when the selected shape has a longer edge of a single
        face which abuts a chain of shorter edges of smaller faces.
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

    def mod_spin(self):
        item = self.get_selected_item()
        if item.update:
            item.update = None
        else:
            item.update = WobblySpinner()


    def toggle_backface_culling(self):
        self.render.backface_culling = not self.render.backface_culling

    def camera_orbit(self, factor):
        self.camera_radius *= factor


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
            wobble_freq=0.01,
        )
        self.gloopy.camera.look_at = Vector(0, 0, 0)
        
        self.keyhandler = KeyHandler(
            self.gloopy.world,
            self.gloopy.render,
            self.gloopy.camera,
        )
        self.gloopy.window.push_handlers(self.keyhandler)

        self.gloopy.run()


if __name__ == '__main__':
    Application().run()

