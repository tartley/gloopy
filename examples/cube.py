
from __future__ import division
from math import pi

# let this script run within the 'examples' dir, even if Gloopy is not installed
import fixpath; fixpath

from gloopy import Gloopy
from gloopy.color import Color
from gloopy.geom.vector import Vector
from gloopy.model.item.gameitem import GameItem
from gloopy.model.move import WobblyOrbit
from gloopy.shapes.cube import Cube


def main():
    gloopy = Gloopy()
    gloopy.init()
    gloopy.world.background_color = Color.Periwinkle
    gloopy.camera.update=WobblyOrbit(
        center=Vector.Origin,
        radius=5,
        axis=Vector(2, 3, 1),
        wobble_size=0.5,
        wobble_freq=pi/10,
    )

    item = GameItem(
        shape=Cube(1, Color.Yellow),
    )
    gloopy.world.add(item)

    gloopy.run()


if __name__ == '__main__':
    main()

