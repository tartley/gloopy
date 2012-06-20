from math import cos, pi, sin

from .multishape import MultiShape
from ..geom.orientation import Orientation
from ..geom.vector import Vector


def Ring(basic_shape, radius, number):
    '''
    Return a new Shape which is composed of `number` of `basic_shape` arranged
    in a ring of `radius`.
    '''
    multi = MultiShape()
    orientation = Orientation()
    delta_angle = 2 * pi / number
    while number > 0:
        number -= 1
        pos = Vector(
            radius * sin(delta_angle * number),
            radius * cos(delta_angle * number),
            0,
        )
        orientation = orientation.roll(delta_angle)
        multi.add(basic_shape, pos, orientation)
    return multi


def TriRings(basic_shape, radius, number):
    '''
    Return a new Shape which is composed of three Rings, one around each
    of the X, Y and Z axes.
    '''
    multi = MultiShape()
    ring = Ring(basic_shape, radius, number)
    multi.add(ring, orientation=Orientation(Vector.x_axis))
    multi.add(ring, orientation=Orientation(Vector.y_axis))
    multi.add(ring, orientation=Orientation(Vector.ZAxis, Vector.x_axis))
    return multi

