from math import sqrt

from .shape import Shape
from ..geom.vector import Vector


def Dodecahedron(size, face_colors=None):
    '''
    size doesn't correspond well to a particular dimension of the resulting
    shape. Edges are size * (sqrt(5) - 1). Verts are at radius size * sqrt(3)
    '''
    phi = (1 + sqrt(5)) / 2
    b = 1 / phi
    c = 2 - phi
    vertices = [
        ( 0,  1,  c), # 0
        ( 0,  1, -c), # 1
        ( 0, -1,  c), # 2
        ( 0, -1, -c), # 3

        ( 1,  c,  0), # 4
        ( 1, -c,  0), # 5

        ( b,  b,  b), # 6
        ( b,  b, -b), # 7
        ( b, -b,  b), # 8
        ( b, -b, -b), # 9

        ( c,  0,  1), # 10
        ( c,  0, -1), # 11

        (-1,  c,  0), # 12
        (-1, -c,  0), # 13

        (-b,  b,  b), # 14
        (-b,  b, -b), # 15
        (-b, -b,  b), # 16
        (-b, -b, -b), # 17

        (-c,  0,  1), # 18
        (-c,  0, -1), # 19
    ]
    vertices = [Vector(*v) * size for v in vertices]
    faces = [
        [ 6,  0, 14, 18, 10],
        [16,  2,  8, 10, 18],
        [ 9,  3, 17, 19, 11],
        [15,  1,  7, 11, 19],
        [ 1,  0,  6,  4,  7],
        [ 0,  1, 15, 12, 14],
        [ 3,  2, 16, 13, 17],
        [ 2,  3,  9,  5,  8],
        [ 6, 10,  8,  5,  4],
        [ 9, 11,  7,  4,  5],
        [15, 19, 17, 13, 12],
        [16, 18, 14, 12, 13],
    ]
    return Shape(vertices, faces, face_colors)

