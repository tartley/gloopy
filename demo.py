#! /usr/bin/env python

from gloopy import Gloopy
from gloopy.model.item.gameitem import GameItem
from gloopy.model.cube import Cube
from gloopy.util.color import Color, white


def main():
    gloopy = Gloopy('demo')
    gloopy.init()
    gloopy.world.background_color = Color.Random()
    try:
        gloopy.world.add(
            GameItem( shape=Cube(1, white) )
        )
        gloopy.run()
    finally:
        gloopy.end()


if __name__ == '__main__':
    main()

