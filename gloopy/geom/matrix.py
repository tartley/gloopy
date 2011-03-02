
from .vector import Vector


class Matrix(object):
    '''
    4x4 matrix. Supports iteration over elements.

    .. function:: __init__(self, position=None, orientation=None)

        Creates a matrix representing the given orientation and offset.
    '''

    # ugly hack: orientation.py populates this to prevent cyclic imports
    _zero_rotation = None

    def __init__(self, position=None, orientation=None):
        if position is None:
            position = Vector.Origin
        if orientation is None:
            orientation = Matrix._zero_rotation
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
        Return a new Vector equal to `vert` transformed by this matrix
        (i.e. rotated by our orientation and translated by our position.)
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

