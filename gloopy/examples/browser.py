#!/usr/bin/env python
from __future__ import division
import logging
import sys
from random import randint, uniform

import pyglet
from pyglet.event import EVENT_HANDLED
from pyglet.window import key

from gloopy.color import Color
from gloopy.geom.vector import Vector
from gloopy.geom.orientation import Orientation
from gloopy.gameitem import GameItem
from gloopy.mainloop import mainloop
from gloopy.move import Spinner, WobblySpinner, WobblyOrbit
from gloopy.move.cycle_frames import CycleFrames
from gloopy.move.interpolate import Interpolate
from gloopy.shapes.cube import Cube, TruncatedCube, SpaceStation
from gloopy.shapes.cube_groups import (
    BitmapCubeCluster, CubeCross, CubeCorners, CubeGlob, RgbCubeCluster,
)
from gloopy.shapes.dodecahedron import Dodecahedron
from gloopy.shapes.extrude import extrude
from gloopy.shapes.icosahedron import Icosahedron
from gloopy.shapes.multishape import MultiShape
from gloopy.shapes.normalize import normalize
from gloopy.shapes.octahedron import Octahedron
from gloopy.shapes.ring import Ring, TriRings
from gloopy.shapes.shape import Shape
from gloopy.shapes.stellate import stellate
from gloopy.shapes.subdivide import subdivide
from gloopy.shapes.tetrahedron import Tetrahedron, DualTetrahedron
from gloopy.view.shape_to_glyph import shape_to_glyph
from gloopy.util.options import Options
from gloopy.world import World


log = logging.getLogger(__name__)


def _get_selected_faces(shape, category):
    if shape is None:
        return None
    return [
        index
        for index, face in enumerate(shape.faces)
        if category is None or face.category == category
    ]


class Controller(object):

    def __init__(self, world, camera):
        self.world = world
        self.camera = camera
        self.camera_radius = 3
        self.selected_item = None
        self.face_category = None
        self.show_highlight = False
        cycle_highlight = CycleFrames(0.25)

        def _update_highlight(highlight, time, dt):
            if self.selected_item:
                highlight.position = self.selected_item.position
                highlight.orientation = self.selected_item.orientation
                cycle_highlight(highlight, time, dt)

        self.highlight = GameItem(
            update=_update_highlight,
            frame=0,
        )
        world.add(self.highlight)

    def add_shape(self, shape, **kwargs):
        self.selected_item = GameItem(shape=shape, **kwargs)
        self.face_category = None
        self.world.add(self.selected_item)
        self._update_highlight_shape()
        return self.selected_item

    def _get_next_selectable_item(self):
        shape_ids = [
            item.id
            for item in self.world
            if item.shape and item is not self.highlight
        ]
        if shape_ids:
            return self.world[max(shape_ids)]

    def toggle_highlight(self):
        self.show_highlight = not self.show_highlight
        self._update_highlight_shape()

    def _get_highlight_shape(self, selected_item, category):
        if not self.show_highlight:
            return None
        if selected_item is None:
            return None
        color = (
            Color.Red
            if isinstance(selected_item.shape, MultiShape) else
            Color.White
        )
        return Shape(
            vertices=selected_item.shape.vertices,
            faces=[
                list(selected_item.shape.faces)[idx].indices
                for idx in _get_selected_faces(selected_item.shape, category)
            ],
            colors=color,
        )

    def _update_highlight_shape(self):
        shape = self._get_highlight_shape(
            self.selected_item, self.face_category
        )
        if shape:
            self.highlight.shape = [shape, None]
        else:
            self.highlight.shape = None

        if self.highlight.shape:
            self.highlight.glyph = [
                shape_to_glyph(shape) for shape in self.highlight.shape
            ]
        else:
            self.highlight.glyph = None

    def remove_shape(self):
        if self.selected_item:
            self.world.remove(self.selected_item)
            self.selected_item = self._get_next_selectable_item()
        self._update_highlight_shape()

    def select_all_faces(self):
        self.face_category = None
        self._update_highlight_shape()

    def select_nothing(self):
        self.face_category = None
        self.selected_item = None
        self._update_highlight_shape()

    def select_next_faces(self):
        if self.selected_item:
            if self.face_category is None:
                self.face_category = 0
            elif self.face_category < self.selected_item.shape.next_category():
                self.face_category += 1
        self._update_highlight_shape()

    def select_prev_faces(self):
        if self.selected_item:
            if self.face_category is None:
                self.face_category = self.selected_item.shape.next_category() - 1
            elif self.face_category >= 0:
                self.face_category -= 1
        self._update_highlight_shape()


    def set_camera_orbit(self, factor):
        # urgh, replace ASAP
        self.camera.update.mover.radius *= factor


    def mod_move(self, offset=None):
        item = self.selected_item

        if offset is None:
            offset = Vector.RandomShell(5)
        rate = 1

        def mover(item, time, dt):
            item.position = item.position + (offset - item.position) * rate * dt

        item.update = mover


    def add_coaxial_rings(self):
        height = randint(-10, 11)
        radius = randint(3, 10)
        color1 = Color.Blue.tinted(Color.Grey, abs(height/10))
        color2 = Color.Blue.tinted(Color.White, abs(height/10))
        return self.add_shape(
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
        if isinstance(self.selected_item.shape, MultiShape):
            self.show_highlight = True
            self._update_highlight_shape()
            return
        faces = _get_selected_faces(
            self.selected_item.shape, self.face_category)
        modifier(self.selected_item.shape, faces, *args)
        self.selected_item.glyph = [shape_to_glyph(self.selected_item.shape)]
        self._update_highlight_shape()

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
            self.selected_item.update = WobblySpinner()


def create_keyhandler(controller):
    keys = {
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

        key.UP: lambda: controller.set_camera_orbit(0.5),
        key.DOWN: lambda: controller.set_camera_orbit(2.0),
        key.PAGEUP: lambda: controller.set_camera_orbit(0.5),
        key.PAGEDOWN: lambda: controller.set_camera_orbit(2.0),

        key.SPACE: controller.toggle_highlight,
        key.EQUAL: controller.select_next_faces,
        key.MINUS: controller.select_prev_faces,
        key._0: controller.select_all_faces,
        key.DELETE: controller.select_nothing,
    }
    keys_ctrl = {
        key.M: controller.mod_move,
        key.Q: lambda: controller.mod_extrude(0.5),
        key.W: lambda: controller.mod_extrude(1),
        key.E: lambda: controller.mod_extrude(2),
        key.R: lambda: controller.mod_extrude(4),
        key.N: controller.mod_normalize,
        key.S: controller.mod_subdivide,
        key.U: lambda: controller.mod_stellate_in(-0.67),
        key.I: lambda: controller.mod_stellate_in(-0.33),
        key.O: lambda: controller.mod_stellate_out(0.5),
        key.P: lambda: controller.mod_stellate_out(1),
        key.C: controller.mod_color,
        key.X: controller.mod_spin,
    }

    def on_key_press(symbol, modifiers):
        lookup = keys_ctrl if modifiers & key.MOD_CTRL else keys
        if symbol in lookup:
            lookup[symbol]()
            return EVENT_HANDLED

    return on_key_press


def create_window(options):
    display = pyglet.window.get_platform().get_default_display()
    screens = display.get_screens()
    for index, screen in enumerate(screens):
        log.info('Screen {0}: {1.width}x{1.height}'.format(index, screen))
    return pyglet.window.Window(
        fullscreen=options.fullscreen,
        vsync=options.vsync,
        resizable=not options.fullscreen,
        screen=screens[-1],
    )


def main(args):
    options = Options(args) # create_parser().parse_args(sys.argv[1:])
    camera = GameItem(
        position=Vector(0, 0, 10),
        look_at=Vector.origin,
        update = Interpolate(WobblyOrbit(
            center=Vector.origin,
            radius=3,
            axis=Vector(2, -3, 1),
            angular_velocity=0.8,
            wobble_size=0.0,
            wobble_freq=0.01,
        ),
    ))
    world = World()
    window = create_window(options)
    window.push_handlers(create_keyhandler(Controller(world, camera)))
    mainloop(world, window, options, camera)


if __name__ == '__main__':
    main(sys.argv)

