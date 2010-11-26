
from .vec3 import Vec3


class Matrix4(object):

    def __init__(self, position, orientation=None):
        self.position = position
        self.orientation = orientation
        if orientation:
            self.elements = orientation.matrix
        if orientation and position:
            self.elements[3] = position.x
            self.elements[7] = position.y
            self.elements[11] = position.z


    def transform(self, vert):
        '''
        return the product of the given vertex by self, to give the vertex
        rotated by our orientation and translated by our position.
        '''
        if self.orientation:
            e = self.elements
            return Vec3(
                vert.x * e[0] + vert.y * e[1] + vert.z * e[2]   + e[3],
                vert.x * e[4] + vert.y * e[5] + vert.z * e[6]   + e[7],
                vert.x * e[8] + vert.y * e[9] + vert.z * e[10]  + e[11],
            )
        else:
            if self.position:
                return Vec3(
                    vert.x + self.position.x,
                    vert.y + self.position.y,
                    vert.z + self.position.z)
            else:
                return vert

