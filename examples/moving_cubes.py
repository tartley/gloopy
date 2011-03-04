
from math import cos

# make sure we can find gloopy in '..', so that we can run from within
# 'examples' dir, even if Gloopy isn't installed.
import sys
from os.path import abspath, dirname, join
sys.path.insert(0, abspath(join(dirname(__file__), '..')))

from gloopy import Gloopy
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

gloopy.run()

