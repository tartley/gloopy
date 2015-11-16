
from __future__ import division
from math import sqrt

from .shape import Shape
from .multishape import MultiShape
from .stellate import stellate
from .subdivide import subdivide
from ..color import Color
from ..geom.orientation import Orientation
from ..geom.vector import Vector

def Tetrahedron(radius, face_colors=None):
    '''
    Return a new Shape, a regular triangular-based pyramid, or d4.
    One of the platonic solids.
    Vertices are at `radius` from the center.

    `colors` may be either an instance of Color, or a sequence of colors,
    one for each face.
    '''
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
    '''
    Return a new Shape, like two interpenetrating Tetrahedrons.
    Vertices are at `radius` from the center. One color is used
    for each of the tetrahedrons.
    '''
    if color1 is None:
        color1 = Color.Random()
    if color2 is None:
        color2 = color1.inverted()
    shape = MultiShape()
    shape.add( Tetrahedron(radius, color1) )
    inverted = Orientation(Vector.x_axis)
    shape.add( Tetrahedron(radius, color2), orientation=inverted)
    return shape

