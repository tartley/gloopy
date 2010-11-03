
from ...util.color import white
from ..cube import Cube
from .gameitem import GameItem


def Player(world):
    return GameItem(
        shape=Cube(0.99, white),
        bounds=set([(0, 0, 0)]),
        collide=True,
        can_fly=False,
        can_climb=False,
    )

