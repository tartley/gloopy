
from .shape import Shape
from ..util.color import Color


def AxisPlanes(size):
    verts = [
        # x=0
        (0, -size, -size),
        (0, -size, +size),
        (0, +size, +size),
        (0, +size, -size),
        # y=0
        (-size, 0, -size),
        (-size, 0, +size),
        (+size, 0, +size),
        (+size, 0, -size),
        # z=0
        (-size, -size, 0),
        (-size, +size, 0),
        (+size, +size, 0),
        (+size, -size, 0),
    ]
    faces = [
        [0, 1, 2, 3],
        [3, 2, 1, 0],

        [4, 5, 6, 7],
        [7, 6, 5, 4],

        [8, 9, 10, 11],
        [11, 10, 9, 8],
    ]
    colors = [
        Color.Red,
        Color.Red,
        Color.Blue,
        Color.Blue,
        Color.Green,
        Color.Green,
    ]
    return Shape(verts, faces, colors)

