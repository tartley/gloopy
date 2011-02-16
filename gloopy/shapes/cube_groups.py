from __future__ import division

from itertools import repeat

from .shape import MultiShape
from .cube import Cube
from ..geom.vector import Vector


def CubeCross(edge, color1, color2):
    multi = MultiShape()

    multi.add(Cube(edge, repeat(color1)))

    for pos in [
        Vector.XAxis, Vector.YAxis, Vector.ZAxis,
        Vector.XNegAxis, Vector.YNegAxis, Vector.ZNegAxis
    ]:
        center = pos * (edge / 2)
        multi.add(
            Cube(1/2, repeat(color2)),
            position=center,
        )
    return multi

