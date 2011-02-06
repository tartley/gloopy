from __future__ import division
from itertools import product
from math import sqrt

from .shape import Shape


def Cube(radius, colors=None):
    size = sqrt(3 * radius * radius) / 1.5
    return Cuboid(size, size, size, colors)


def Cuboid(x, y, z, colors=None):
    verts = list(product((-x/2, +x/2), (-y/2, +y/2), (-z/2, +z/2)))
    faces = [
        [0, 1, 3, 2], # left
        [4, 6, 7, 5], # right
        [7, 3, 1, 5], # front
        [0, 2, 6, 4], # back
        [3, 7, 6, 2], # +y top
        [1, 0, 4, 5], # -y bottom
    ]
    return Shape(verts, faces, colors)

