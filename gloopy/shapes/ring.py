from math import cos, pi, sin

from .shape import MultiShape
from ..geom.orientation import Orientation
from ..geom.vector import Vector


def Ring(basic_shape, radius, number):
    multi = MultiShape()

    angle = 0
    orientation = Orientation()
    delta_angle = 2 * pi / number
    while angle < 2 * pi:
        angle += delta_angle
        pos = Vector(
            0,
            radius * sin(angle),
            radius * cos(angle),
        )
        orientation.pitch(delta_angle)
        multi.add(basic_shape, pos, orientation)
    return multi

