from __future__ import division
from itertools import chain, product, repeat
from math import sqrt

from .shape import add_vertex, Face, Shape
from ..geom.vector import Vector
from ..color import Color


def Cube(radius, colors=None):
    size = sqrt(3 * radius * radius) / 1.5
    return Cuboid(size, size, size, colors, source='Cube')


def Cuboid(x, y, z, colors=None, source='Cuboid'):
    verts = list(product((-x/2, +x/2), (-y/2, +y/2), (-z/2, +z/2)))
    faces = [
        [0, 1, 3, 2], # left
        [4, 6, 7, 5], # right
        [7, 3, 1, 5], # front
        [0, 2, 6, 4], # back
        [3, 7, 6, 2], # +y top
        [1, 0, 4, 5], # -y bottom
    ]
    return Shape(verts, faces, colors, source)


def TruncatedCube(edge, truncation=0.67, color1=None, color2=None):
    if color1 is None:
        color1 = Color.Random()
    if color2 is None:
        color2 = color1.inverted()
    e2 = edge / 2
    verts = [
        (-e2 + e2 * truncation, -e2, -e2),
        (-e2, -e2 + e2 * truncation, -e2),
        (-e2, -e2, -e2 + e2 * truncation),

        (-e2 + e2 * truncation, -e2, +e2),
        (-e2, -e2 + e2 * truncation, +e2),
        (-e2, -e2, +e2 - e2 * truncation),

        (-e2 + e2 * truncation, +e2, -e2),
        (-e2, +e2 - e2 * truncation, -e2),
        (-e2, +e2, -e2 + e2 * truncation),

        (-e2 + e2 * truncation, +e2, +e2),
        (-e2, +e2 - e2 * truncation, +e2),
        (-e2, +e2, +e2 - e2 * truncation),

        (+e2 - e2 * truncation, -e2, -e2),
        (+e2, -e2 + e2 * truncation, -e2),
        (+e2, -e2, -e2 + e2 * truncation),

        (+e2 - e2 * truncation, -e2, +e2),
        (+e2, -e2 + e2 * truncation, +e2),
        (+e2, -e2, +e2 - e2 * truncation),

        (+e2 - e2 * truncation, +e2, -e2),
        (+e2, +e2 - e2 * truncation, -e2),
        (+e2, +e2, -e2 + e2 * truncation),

        (+e2 - e2 * truncation, +e2, +e2),
        (+e2, +e2 - e2 * truncation, +e2),
        (+e2, +e2, +e2 - e2 * truncation),
    ]
    faces = [
        [ 1,  2,  5,  4, 10, 11,  8,  7], # left
        [14, 13, 19, 20, 23, 22, 16, 17], # right
        [22, 21,  9, 10,  4,  3, 15, 16], # front
        [ 0,  1,  7,  6, 18, 19, 13, 12], # back
        [11,  9, 21, 23, 20, 18, 6,  8], # top
        [ 3,  5,  2,  0, 12, 14, 17, 15], # bottom

        [0, 2, 1],
        [3, 4, 5],
        [6, 7, 8],
        [9, 11, 10],
        [12, 13, 14],
        [15, 17, 16],
        [18, 20, 19],
        [21, 22, 23],
    ]
    face_colors = chain(
        repeat(color1, 6),
        repeat(color2, 8),
    )
    return Shape(verts, faces, face_colors)


def SpaceStation(edge):

    color = Color.Grey.tinted(Color.Cyan)
    shape = TruncatedCube(edge, 0.999, color, color)

    # add the door
    e2 = edge / 2
    HEIGHT = 0.075
    WIDTH = 0.25
    indices = [
        add_vertex(shape.vertices, v)
        for v in [
            Vector(+e2 * 1.001, -e2 * HEIGHT, +e2 * WIDTH),
            Vector(+e2 * 1.001, -e2 * HEIGHT, -e2 * WIDTH),
            Vector(+e2 * 1.001, +e2 * HEIGHT, -e2 * WIDTH),
            Vector(+e2 * 1.001, +e2 * HEIGHT, +e2 * WIDTH),
        ]
    ]
    shape.faces.append( Face(indices, Color.Black, shape) )

    return shape

