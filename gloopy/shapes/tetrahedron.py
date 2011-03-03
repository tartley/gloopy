
from __future__ import division
from math import sqrt

from .shape import Shape
from .stellate import stellate
from .subdivide import subdivide
from ..color import Color


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
    return Shape(vertices, faces, face_colors, 'Tetrahedron')


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
    shape = Tetrahedron(radius, color1)
    subdivide(shape)
    center_faces = [
        i for i, face in enumerate(shape.faces)
        if face.source.endswith('subdivide-center')
    ]
    stellate(shape, center_faces, sqrt(2))
    return shape

