
from __future__ import division
from math import pi

# allow this script to import gloopy from the parent directory, so we can
# run from the 'examples' dir, even if gloopy isn't installed.
import sys
from os.path import abspath, dirname, join
sys.path.insert(0, abspath(join(dirname(__file__), '..')))

from gloopy import Gloopy
from gloopy.geom.vector import origin, Vector
from gloopy.model.cube import Cube
from gloopy.model.item.gameitem import GameItem
from gloopy.model.move import WobblyOrbit
from gloopy.util.color import Color


def main():
    gloopy = Gloopy()
    gloopy.init()
    gloopy.world.background_color = Color.Periwinkle
    gloopy.camera.update=WobblyOrbit(
        center=origin,
        radius=5,
        axis=Vector(2, 3, 1),
        wobble_size=0.5,
        wobble_freq=pi/10,
    )

    item = GameItem(
        shape=Cube(1, Color.Yellow),
    )
    gloopy.world.add(item)

    gloopy.start()
    gloopy.stop()


if __name__ == '__main__':
    main()

