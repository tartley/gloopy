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
        orientation = orientation.pitch(delta_angle)
        multi.add(basic_shape, pos, orientation)
    return multi


def TriRings(basic_shape, radius, number):
    '''
    Return a new Shape which is composed of three Rings, one around each
    of the X, Y and Z axes.
    '''
    multi = MultiShape()
    c1 = Ring(basic_shape, radius, number)
    multi.add(c1, orientation=Orientation(Vector.XAxis))
    multi.add(c1, orientation=Orientation(Vector.YAxis))
    multi.add(c1, orientation=Orientation(Vector.ZAxis, Vector.XAxis))
    return multi

