#! /usr/bin/env python
from __future__ import division

from euclid import Quaternion

from gloopy import Gloopy
from gloopy.model.item.gameitem import GameItem
from gloopy.model.cube import Cube
from gloopy.util.color import Color
from gloopy.util.vectors import origin, x_axis


def main():
    gloopy = Gloopy()
    gloopy.init()
    gloopy.world.background_color = Color.Random()
    try:
        gloopy.world.add(
            GameItem(
                shape=Cube(1, Color.White),
                position=origin,
                velocity=(.1, .2, .3),
                acceleration=(-.1, -.3, -.2),
                angular_velocity=Quaternion.new_rotate_axis(100, x_axis),
                orientation=Quaternion(),
            )
        )
        gloopy.start()
    finally:
        gloopy.stop()


if __name__ == '__main__':
    main()

