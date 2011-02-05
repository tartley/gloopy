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
from gloopy.shapes.octahedron import Octahedron
from gloopy.shapes.tetrahedron import Tetrahedron, DualTetrahedron
from gloopy.shapes.sphere import Subdivided, Normalize, nest


log = logging.getLogger(__name__)


bestiary = {
    key._1: Cube(1, Color.Blue),
    key._2: Cuboid(0.5, 2.5, 3, Color.Periwinkle),
    key._3: Tetrahedron(2.0, Color.Blue.variations(Color.Cyan)),
    key._4: DualTetrahedron(2.0),
    key._5: Normalize(
            nest(Subdivided, 0)(
                Tetrahedron(1.0, Color.White)
            )
        ),
    key._6: Normalize(
            nest(Subdivided, 1)(
                Tetrahedron(1.0, Color.White)
            )
        ),
    key._7: Normalize(
            nest(Subdivided, 2)(
                Tetrahedron(1.0, Color.White)
            )
        ),
    key._8: Normalize(
            nest(Subdivided, 3)(
                Tetrahedron(1.0, Color.White)
            )
        ),
    key._9: Normalize(
            nest(Subdivided, 4)(
                Tetrahedron(1.0, Color.White)
            )
        ),
    key._0: Normalize(
            nest(Subdivided, 5)(
                Tetrahedron(1.0, Color.White)
            )
        ),
    key.Q: Normalize(
            nest(Subdivided, 0)(
                Octahedron(1.0, Color.White)
            )
        ),
    key.W: Normalize(
            nest(Subdivided, 1)(
                Octahedron(1.0, Color.White)
            )
        ),
    key.E: Normalize(
            nest(Subdivided, 2)(
                Octahedron(1.0, Color.White)
            )
        ),
    key.R: Normalize(
            nest(Subdivided, 3)(
                Octahedron(1.0, Color.White)
            )
        ),
    key.T: Normalize(
            nest(Subdivided, 4)(
                Octahedron(1.0, Color.White)
            )
        ),
    key.Y: Normalize(
            nest(Subdivided, 5)(
                Octahedron(1.0, Color.White)
            )
        ),
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
            radius=4,
            axis=Vector(2, 3, 1),
            angular_velocity=1,
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

