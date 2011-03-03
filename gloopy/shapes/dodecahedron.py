from math import sqrt

from .shape import Shape


def Dodecahedron(radius, face_colors=None):
    '''
    Return a new Shape.
    One of the platonic solids.
    Verts are at the given `radius`.

    `face_colors` may either be a Color which is applied to every face, or
    a sequence of colors, one for each face.
    '''

    phi = (1 + sqrt(5)) / 2
    size = radius / sqrt(3) * phi
    b = size / phi
    c = size * (2 - phi)
    vertices = [
        (    0,  size,     c), # 0
        (    0,  size,    -c), # 1
        (    0, -size,     c), # 2
        (    0, -size,    -c), # 3

        ( size,     c,     0), # 4
        ( size,    -c,     0), # 5

        (    b,     b,     b), # 6
        (    b,     b, -   b), # 7
        (    b, -   b,     b), # 8
        (    b, -   b, -   b), # 9

        (    c,     0,  size), # 10
        (    c,     0, -size), # 11

        (-size,     c,     0), # 12
        (-size,    -c,     0), # 13

        (   -b,     b,     b), # 14
        (   -b,     b,    -b), # 15
        (   -b,    -b,     b), # 16
        (   -b,    -b,    -b), # 17

        (   -c,     0,  size), # 18
        (   -c,     0, -size), # 19
    ]
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
    return Shape(vertices, faces, face_colors, 'Dodecahedron')

