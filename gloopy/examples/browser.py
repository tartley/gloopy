#! /usr/bin/env python
from __future__ import division
from random import randint, uniform

from pyglet.event import EVENT_HANDLED
from pyglet.window import key

from gloopy import Gloopy
from gloopy.color import Color
from gloopy.geom.vector import Vector
from gloopy.geom.orientation import Orientation
from gloopy.gameitem import GameItem
from gloopy.move import Spinner, WobblySpinner, WobblyOrbit
from gloopy.move.cycle_frames import CycleFrames
from gloopy.shapes.cube import Cube, TruncatedCube, SpaceStation
from gloopy.shapes.cube_groups import (
    BitmapCubeCluster, CubeCross, CubeCorners, CubeGlob, RgbCubeCluster,
)
from gloopy.shapes.dodecahedron import Dodecahedron
from gloopy.shapes.extrude import extrude
from gloopy.shapes.icosahedron import Icosahedron
from gloopy.shapes.normalize import normalize
from gloopy.shapes.octahedron import Octahedron
from gloopy.shapes.ring import Ring, TriRings
from gloopy.shapes.shape import Shape
from gloopy.shapes.stellate import stellate
from gloopy.shapes.subdivide import subdivide
from gloopy.shapes.tetrahedron import Tetrahedron, DualTetrahedron
from gloopy.view.shape_to_glyph import shape_to_glyph


def _get_selected_faces(shape, category):
    if shape is None:
        return None
    return [
        index
        for index, face in enumerate(shape.faces)
        if face.category is None or face.category == category
    ]

def _get_highlight_shape(original, category):
    return Shape(
        vertices=original.vertices,
        faces=[
            original.faces[idx].indices
            for idx in _get_selected_faces(original, category)
        ],
        colors=Color.White,
    )



class Controller(object):

    def __init__(self, world, camera):
        self.world = world
        self.world.update += self.world_update
        self.camera = camera
        self.camera_radius = 3
        self.selected_item = None
        self.face_category = None

        def _update_highlight(highlight, _, __):
            if self.selected_item:
                highlight.position = self.selected_item.position

        self.highlight = GameItem(
            update=_update_highlight,
        )
        world.add(self.highlight)

        
    def add_shape(self, shape, **kwargs):
        self.selected_item = GameItem(shape=shape, **kwargs)
        self.world.add(self.selected_item)
        return self.selected_item

    def _get_next_selectable_item(self):
        shape_ids = [
            item.id
            for item in self.world
            if item.shape and item is not self.highlight
        ]
        if shape_ids:
            return self.world[max(shape_ids)]

    def remove_shape(self):
        if self.selected_item:
            self.world.remove(self.selected_item)
            self.selected_item = self._get_next_selectable_item()

    def _update_highlight_shape(self):
        self.world.remove(self.highlight)
        self.highlight.shape = _get_highlight_shape(
            self.selected_item.shape, self.face_category
        )
        self.world.add(self.highlight)

    def select_faces(self, value):
        if value is None:
            self.face_category = None
        else:
            if self.face_category is None:
                self.face_category = 0
            else:
                self.face_category += value
        self._update_highlight_shape()


    def camera_orbit(self, factor):
        self.camera_radius *= factor

    def world_update(self, time, dt):
        if self.camera.update:
            rate = 3 * dt
            self.camera.update.radius += (
                self.camera_radius - self.camera.update.radius) * rate


    def mod_move(self, offset=None):
        item = self.selected_item

        if offset is None:
            offset = Vector.RandomShell(5)
        rate = 1

        def mover(item, time, dt):
            item.position = item.position + (offset- item.position) * rate * dt

        item.update = mover


    def add_coaxial_rings(self):
        height = randint(-10, 11)
        radius = randint(3, 10)
        color1 = Color.Blue.tinted(Color.Grey, abs(height/10))
        color2 = Color.Blue.tinted(Color.White, abs(height/10))
        self.add_shape(
            shape=Ring(
                CubeCross(4, color1, color2),
                radius * 6, 
                int(radius * 5),
            ),
            position=Vector(0, height * 6, 0),
            orientation=Orientation(Vector.y_axis),
            update=Spinner(Vector.y_axis, speed=uniform(-1, 1)),
        )

    def add_koche_tetra(self):
        color1 = Color.Random()
        color2 = Color.Random()
        shape = Tetrahedron(1, color1)
        for i in range(6):
            faces = _get_selected_faces(shape, i + 1)
            subdivide(shape, color=color1.tinted(color2, i/5))
            stellate(shape, faces=faces, height=1.2)
        return self.add_shape(shape)

    def mod_shape(self, modifier, *args):
        faces = _get_selected_faces(self.selected_item.shape, self.face_category)
        modifier(self.selected_item.shape, faces, *args)
        self.selected_item.glyph = [shape_to_glyph(self.selected_item.shape)]

    def mod_extrude(self, length):
        self.mod_shape(extrude, length)

    def mod_normalize(self):
        normalize(self.selected_item.shape)
        self.selected_item.glyph = [shape_to_glyph(self.selected_item.shape)]

    def mod_subdivide(self):
        self.mod_shape(subdivide)

    def mod_stellate_out(self, amount=1):
        self.mod_shape(stellate, amount)

    def mod_stellate_in(self, amount=-0.33):
        self.mod_shape(stellate, amount)

    def recolor(self, shape, faces, color):
        for face_index in faces:
            shape.faces[face_index].color = color

    def mod_color(self):
        self.mod_shape(self.recolor, Color.Random())

    def mod_spin(self):
        if isinstance(self.selected_item.update, WobblySpinner):
            self.selected_item.update = None
        else:
            self._selected_item.update = WobblySpinner()


class KeyHandler(object):

    def __init__(self, controller):
        self.controller = controller

        self.keys = {
            key._1: lambda: controller.add_shape(
                Tetrahedron(1, Color.Random())),
            key._2: lambda: controller.add_shape(
                Cube(0.75, Color.Random())),
            key._3: lambda: controller.add_shape(
                Octahedron(0.75, Color.Random())),
            key._4: lambda: controller.add_shape(
                Dodecahedron(0.65, Color.Random())),
            key._5: lambda: controller.add_shape(
                Icosahedron(0.4, Color.Random())),
            key._6: lambda: controller.add_shape(
                DualTetrahedron(0.9, Color.Random())),
            key._7: lambda: controller.add_shape( 
                SpaceStation(1.1),
                orientation=Orientation(),
                update=Spinner(
                    Vector.x_axis,
                    speed=1,
                    orientation=Orientation()
                ),
            ),

            key.Q: lambda: controller.add_shape(
                CubeCross(0.67, Color.Red, Color.Red.tinted(Color.Orange)),
            ),
            key.W: lambda: controller.add_shape(
                CubeCorners(
                    0.6, Color.Yellow.tinted(Color.White), Color.Yellow
                ),
            ),
            key.E: lambda: controller.add_shape(
                Ring(Cube(0.5, Color.Green), 2, 20),
                orientation=Orientation(Vector.y_axis),
                update=Spinner(Vector.y_axis),
            ),
            key.R: lambda: controller.add_shape(
                Ring(
                    TruncatedCube(1.75, 0.8, Color.SeaGreen, Color.Periwinkle),
                    6, 25
                ),
                update=Spinner(axis=Vector.x_axis, speed=0.5),
            ),
            key.T: lambda: controller.add_shape(
                TriRings(Cube(1.02, Color.DarkTeal), 8, 40),
                update=WobblySpinner(speed=-0.2),
            ),
            key.Y: lambda: controller.add_shape(
                shape=TriRings(Octahedron(5, Color.Teal), 12, 8),
                update=WobblySpinner(speed=-1),
            ),
            key.U: controller.add_coaxial_rings,

            key.Z: lambda: controller.add_shape(
                CubeGlob(4, 70, 1000, Color.DarkRed)
            ),
            key.X: lambda: controller.add_shape(
                CubeGlob(8, 150, 2000, Color.Red)
            ),
            key.C: lambda: controller.add_shape(
                RgbCubeCluster(16, 4000, scale=2, hole=70)
            ),
            key.V: lambda: controller.add_shape(
                [
                    BitmapCubeCluster('invader1.png', edge=10),
                    BitmapCubeCluster('invader2.png', edge=10)
                ],
                position=Vector.RandomShell(350),
                update=CycleFrames(1),
            ),
            key.B: controller.add_koche_tetra,

            key.BACKSPACE: controller.remove_shape,

            key.UP: lambda: controller.camera_orbit(0.5),
            key.DOWN: lambda: controller.camera_orbit(2.0),
            key.PAGEUP: lambda: controller.camera_orbit(0.5),
            key.PAGEDOWN: lambda: controller.camera_orbit(2.0),

            key.EQUAL: lambda: controller.select_faces(+1),
            key.MINUS: lambda: controller.select_faces(-1),
            key._0: lambda: controller.select_faces(None),
        }
        self.keys_ctrl = {
            key.M: controller.mod_move,
            key.Q: lambda: controller.mod_extrude(0.25),
            key.W: lambda: controller.mod_extrude(0.5),
            key.E: lambda: controller.mod_extrude(1),
            key.R: lambda: controller.mod_extrude(2),
            key.T: lambda: controller.mod_extrude(4),
            key.Y: lambda: controller.mod_extrude(8),
            key.N: controller.mod_normalize,
            key.S: controller.mod_subdivide,
            key.U: lambda: controller.mod_stellate_in(-0.67),
            key.I: lambda: controller.mod_stellate_in(-0.33),
            key.O: lambda: controller.mod_stellate_out(0.5),
            key.P: lambda: controller.mod_stellate_out(1),
            key.C: controller.mod_color,
            key.X: controller.mod_spin,
        }

    def on_key_press(self, symbol, modifiers):
        if modifiers & key.MOD_CTRL:
            if symbol in self.keys_ctrl:
                self.keys_ctrl[symbol]()
                return EVENT_HANDLED
        elif modifiers == 0:
            if symbol in self.keys:
                self.keys[symbol]()
                return EVENT_HANDLED



def main():
    gloopy = Gloopy()
    gloopy.init()
    gloopy.world.background_color = Color.Orange
    gloopy.camera.update=WobblyOrbit(
        center=Vector.origin,
        radius=3,
        axis=Vector(2, -3, 1),
        angular_velocity=0.8,
        wobble_size=0.0,
        wobble_freq=0.01,
    )
    controller = Controller(gloopy.world, gloopy.camera)
    gloopy.window.push_handlers( KeyHandler(controller) )
    gloopy.run()


if __name__ == '__main__':
    main()

