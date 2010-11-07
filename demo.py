#! /usr/bin/env python
from __future__ import division

from euclid import Quaternion

from gloopy import Gloopy
from gloopy.model.item.gameitem import GameItem
from gloopy.model.cube import Cube
from gloopy.util.color import Color
from gloopy.util.vectors import (
    orientation_random, vec3_random, x_axis, y_axis, z_axis,
)
from gloopy.model.move import Newtonian


def main():
    gloopy = Gloopy()
    gloopy.init()
    gloopy.world.background_color = Color.Random()
    try:
        for _ in range(100):

            position = vec3_random(10)
            gloopy.world.add(
                GameItem(
                    shape=Cube(1, Color.Random().tinted(Color.White, .9)),
                    position=position*2,
                    velocity=-position,
                    acceleration=position/5,
                    orientation=orientation_random(),
                    angular_velocity=Quaternion.new_rotate_axis(
                        100, vec3_random(1).normalize()
                    ),
                    update=Newtonian(),
                )
            )

        gloopy.start()
    finally:
        gloopy.stop()


if __name__ == '__main__':
    main()

