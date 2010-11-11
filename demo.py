#! /usr/bin/env python
from __future__ import division
from random import uniform

from gloopy import Gloopy
from gloopy.lib.euclid import Quaternion, Vector3
from gloopy.model.item.gameitem import GameItem
from gloopy.model.cube import Cube
from gloopy.util.color import Color
from gloopy.util.vectors import (
    origin, orientation_random, vec3_random, x_axis, y_axis, z_axis,
)
from gloopy.model.move import Newtonian, WobblyOrbit



def main():
    gloopy = Gloopy()
    gloopy.init()
    try:
        gloopy.world.background_color = Color.Random()
        for _ in range(200):
            position = vec3_random(10)
            gloopy.world.add(
                GameItem(
                    shape=Cube(1, Color.Random().tinted(Color.Red, .5)),
                    position=position*2,
                    velocity=-position * uniform(0, 1),
                    acceleration=position/10,
                    orientation=orientation_random(),
                    angular_velocity=Quaternion.new_rotate_axis(
                        100, vec3_random(1).normalize()
                    ),
                    update=Newtonian(),
                )
            )    
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

