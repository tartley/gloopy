
# let this script run within the 'examples' dir, even if Gloopy is not installed
import fixpath

from gloopy import Gloopy
from gloopy.color import Color
from gloopy.geom.vector import Vector
from gloopy.model.item.gameitem import GameItem
from gloopy.shapes.cube import Cube


gloopy = Gloopy()
gloopy.init()

item = GameItem( shape=Cube(1, Color.Green) )
gloopy.world.add(item)

gloopy.camera.position = Vector(1, 2, 3)

gloopy.run()

