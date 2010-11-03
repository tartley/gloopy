
from ...util.color import white
from ..cube import Cube
from ..move import directed_motion
from .gameitem import GameItem


def Player(world):
    return GameItem(
        shape=Cube(0.99, white),
        update=directed_motion(world),
        bounds=set([(0, 0, 0)]),
        collide=True,
        can_fly=False,
        can_climb=False,
    )

