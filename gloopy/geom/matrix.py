
from .vector import Vector, origin


class Matrix(object):

    # ugly hack: orientation.py populates this to prevent cyclic imports
    zero_rotation = None

    def __init__(self, position=None, orientation=None):
        print position, orientation
        if position is None:
            position = origin
        if orientation is None:
            orientation = Matrix.zero_rotation
        self.position = p = position
        self.orientation = o = orientation
        self.elements = [
              o.right.x,    o.right.y,    o.right.z, 0,
                 o.up.x,       o.up.y,       o.up.z, 0,
           -o.forward.x, -o.forward.y, -o.forward.z, 0,
                    p.x,          p.y,          p.z, 1,
        ]

    def __iter__(self):
        return self.elements.__iter__()

    def transform(self, vert):
        '''
        return the product of the given vertex by self, to give the vertex
        rotated by our orientation and translated by our position.
        '''
        if self.orientation:
            e = self.elements
            return Vector(
                vert.x * e[0] + vert.y * e[1] + vert.z * e[2]   + e[12],
                vert.x * e[4] + vert.y * e[5] + vert.z * e[6]   + e[13],
                vert.x * e[8] + vert.y * e[9] + vert.z * e[10]  + e[14],
            )
        else:
            if self.position:
                return Vector(
                    vert.x + self.position.x,
                    vert.y + self.position.y,
                    vert.z + self.position.z)
            else:
                return vert

