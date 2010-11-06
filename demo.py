#! /usr/bin/env python

from gloopy import Gloopy
from gloopy.model.item.gameitem import GameItem
from gloopy.model.cube import Cube
from gloopy.util.color import Color


def main():
    gloopy = Gloopy()
    gloopy.init()
    gloopy.world.background_color = Color.Random()
    try:
        gloopy.world.add(
            GameItem( shape=Cube(1, Color.White) )
        )
        gloopy.start()
    finally:
        gloopy.stop()


if __name__ == '__main__':
    main()

