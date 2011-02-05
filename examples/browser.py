#! /usr/bin/env python
from __future__ import division
import logging

import fixpath; fixpath

from pyglet.event import EVENT_HANDLED
from pyglet.window import key

from gloopy import Gloopy
from gloopy.color import Color
from gloopy.geom.vector import origin, Vector
from gloopy.model.item.gameitem import GameItem
from gloopy.model.move import WobblyOrbit
from gloopy.shapes.cube import Cube, Cuboid
from gloopy.shapes.dodecahedron import Dodecahedron
from gloopy.shapes.icosahedron import Icosahedron
from gloopy.shapes.octahedron import Octahedron
from gloopy.shapes.tetrahedron import Tetrahedron, DualTetrahedron
from gloopy.shapes.sphere import subdivided, normalize, nest
from gloopy.shapes.stellate import stellate


log = logging.getLogger(__name__)

bestiary = {
    key._1: Cube(1, Color.Blue),
    key._2: Cuboid(0.5, 2.5, 3, Color.Periwinkle),
    key._3: Tetrahedron(2.0, Color.Blue.variations(Color.Cyan)),
    key._4: DualTetrahedron(2.0),
    key._5: normalize(
            nest(subdivided, 0)(
                Tetrahedron(1.0, Color.Random())
            )
        ),
    key._6: normalize(
            nest(subdivided, 1)(
                Tetrahedron(1.0, Color.Random())
            )
        ),
    key._7: normalize(
            nest(subdivided, 2)(
                Tetrahedron(1.0, Color.Random())
            )
        ),
    key._8: normalize(
            nest(subdivided, 3)(
                Tetrahedron(1.0, Color.Random())
            )
        ),
    key._9: normalize(
            nest(subdivided, 4)(
                Tetrahedron(1.0, Color.Random())
            )
        ),
    key._0: normalize(
            nest(subdivided, 5)(
                Tetrahedron(1.0, Color.Random())
            )
        ),
    key.Q: normalize(
            nest(subdivided, 0)(
                Octahedron(1.0, Color.Random())
            )
        ),
    key.W: normalize(
            nest(subdivided, 1)(
                Octahedron(1.0, Color.Random())
            )
        ),
    key.E: normalize(
            nest(subdivided, 2)(
                Octahedron(1.0, Color.Random())
            )
        ),
    key.R: normalize(
            nest(subdivided, 3)(
                Octahedron(1.0, Color.Random())
            )
        ),
    key.T: normalize(
            nest(subdivided, 4)(
                Octahedron(1.0, Color.Random())
            )
        ),
    key.Y: normalize(
            nest(subdivided, 5)(
                Octahedron(1.0, Color.Random())
            )
        ),
    key.U: Dodecahedron(1.0, Color.Purple),
    key.I: Icosahedron(1, Color.Green),

    key.A: stellate( Tetrahedron(1, Color.Random()), 2.0 ),
    key.S: stellate( Tetrahedron(2, Color.Random()), -0.25 ),
    key.D: stellate( Cube(0.5, Color.Random()), 2.5 ),
    key.F: stellate( Cube(1, Color.Random()), -0.25 ),
    key.G: stellate( Octahedron(0.5, Color.Random()), 2.5 ),
    key.H: stellate( Octahedron(1, Color.Random()), -0.25 ),
    key.J: stellate( Dodecahedron(0.5, Color.Random()), 1.5 ),
    key.K: stellate( Dodecahedron(1, Color.Random()), -0.25 ),
    key.L: stellate( Icosahedron(0.5, Color.Random()), 1.5 ),
    key.M: stellate( Icosahedron(1, Color.Random()), -0.25 ),
}


class Application(object):

    def __init__(self):
        self.gloopy = None

    def run(self):
        self.gloopy = Gloopy()
        self.gloopy.init()
        self.gloopy.world.background_color = Color.Orange

        self.gloopy.eventloop.window.push_handlers(
            on_key_press=self.on_key_press
        )
        self.gloopy.camera.update=WobblyOrbit(
            center=origin,
            radius=3,
            axis=Vector(2, -3, 1),
            angular_velocity=0.2,
            wobble_size=0.0,
            wobble_freq=1,
        )
        self.gloopy.camera.look_at = Vector(0, 0, 0)
        try:
            self.gloopy.start()
        finally:
            self.gloopy.stop()


    def remove_items(self, symbol):
        to_remove = [
            item
            for item in self.gloopy.world
            if item.key == symbol
        ]
        for item in to_remove:
            self.gloopy.world.remove(item)


    def on_key_press(self, symbol, modifiers):

        if symbol in bestiary:
            if modifiers & key.MOD_SHIFT:
                self.remove_items( symbol )
            else:
                self.gloopy.world.add(
                    GameItem(
                        shape=bestiary[symbol],
                        key=symbol,
                    )
                )
        else:
            return

        return EVENT_HANDLED


if __name__ == '__main__':
    Application().run()

