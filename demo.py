#! /usr/bin/env python
from __future__ import division

from gloopy import Gloopy
from gloopy.model.item.gameitem import GameItem
from gloopy.model.cube import Cube
from gloopy.model import move
from gloopy.util.color import Color
from gloopy.util.vectors import origin


def main():
    gloopy = Gloopy()
    gloopy.init()
    gloopy.world.background_color = Color.Random()
    try:
        gloopy.world.add(
            GameItem(
                shape=Cube(1, Color.White),
                position=origin,
                velocity=(0.01, 0.02, 0.03),
                acceleration=(-0.0001, -0.0002, -0.0003),
                update=move.Linear(),
            )
        )
        gloopy.start()
    finally:
        gloopy.stop()


if __name__ == '__main__':
    main()

