
from .vec3 import Vec3


class Matrix4(object):

    def __init__(self, position, orientation=None):
        self.position = p = position
        self.orientation = o = orientation
        self.elements = [
              o.right.x,    o.right.y,    o.right.z, 0,
                 o.up.x,       o.up.y,       o.up.z, 0,
           -o.forward.x, -o.forward.y, -o.forward.z, 0,
                    p.x,          p.y,          p.z, 1,
        ]


    def transform(self, vert):
        '''
        return the product of the given vertex by self, to give the vertex
        rotated by our orientation and translated by our position.
        '''
        if self.orientation:
            e = self.elements
            return Vec3(
                vert.x * e[0] + vert.y * e[1] + vert.z * e[2]   + e[12],
                vert.x * e[4] + vert.y * e[5] + vert.z * e[6]   + e[13],
                vert.x * e[8] + vert.y * e[9] + vert.z * e[10]  + e[14],
            )
        else:
            if self.position:
                return Vec3(
                    vert.x + self.position.x,
                    vert.y + self.position.y,
                    vert.z + self.position.z)
            else:
                return vert

