#!/usr/bin/env python

from math import cos

# find gloopy in '../..', so we can run even if Gloopy is not installed
import fixpath

from gloopy.mainloop import mainloop
from gloopy.color import Color
from gloopy.geom.vector import Vector
from gloopy.gameitem import GameItem
from gloopy.shapes.cube import Cube


gloopy = Gloopy()
gloopy.init()

def move_around(item, time, dt):
    item.position += Vector(cos(time*2)/300, cos(time*3)/400, 0)

item = GameItem(
    shape=Cube(1, Color.Blue),
    update=move_around,
)

gloopy.world.add(item)

gloopy.camera.position = Vector(1, 2, 3)

mainloop(world, window, options, camera)

