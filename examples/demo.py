#! /usr/bin/env python
from __future__ import division
from random import uniform

# allow this script to import gloopy from the parent directory, so we can
# run from the 'examples' dir, even if gloopy isn't installed.
import sys
from os.path import abspath, dirname, join
sys.path.insert(0, abspath(join(dirname(__file__), '..')))

from gloopy import Gloopy
from gloopy.lib.euclid import Quaternion, Vector3
from gloopy.model.item.gameitem import GameItem
from gloopy.model.cube import Cube
from gloopy.util.color import Color
from gloopy.util.vectors import (
    origin, orientation_random, vec3_random, x_axis, y_axis, z_axis,
)
from gloopy.model.move import Newtonian, WobblyOrbit



def add_many_gameitems(world):
    shape=Cube(1, Color.Red)
    for i in range(200):
        world.add(
            GameItem(
                shape=shape,
                position=vec3_random(i/3),
                orientation=orientation_random(),
            )
        )


def main():
    gloopy = Gloopy()
    gloopy.init()
    try:
        gloopy.world.background_color = Color.Random()

        add_many_gameitems(gloopy.world)

        gloopy.camera.update=WobblyOrbit(
            gloopy.world.items[1], 50, Vector3(2, 3, 1),
            wobble_size=0.9, wobble_freq=0.4,
        )
        gloopy.camera.look_at = gloopy.world.items[1]

        gloopy.start()
    finally:
        gloopy.stop()


if __name__ == '__main__':
    main()

