
from __future__ import division
from math import sqrt

from .shape import Shape, MultiShape
from ..color import Color
from ..geom.orientation import Orientation
from ..geom.vector import x_axis


def Tetrahedron(radius, face_colors=None):
    size = sqrt(3 * radius * radius) / 3
    vertices = [
        (+size, +size, +size),
        (-size, -size, +size),
        (-size, +size, -size),
        (+size, -size, -size), 
    ]
    faces = [ [0, 2, 1], [1, 3, 0], [2, 3, 1], [0, 3, 2] ]
    return Shape(vertices, faces, face_colors)


def DualTetrahedron(radius, color1=None, color2=None):
    if color1 is None:
        color1 = Color.Random()
    if color2 is None:
        color2 = color1.inverted()
    m = MultiShape()
    m.add( Tetrahedron(radius, color1.variations()) )
    inverted = Orientation(x_axis)
    m.add( Tetrahedron(radius, color2.variations()), orientation=inverted)
    return m

