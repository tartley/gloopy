
from __future__ import division
from collections import namedtuple
from math import acos, cos, sin, sqrt
from random import randint, uniform


EPSILON = 1e-7


class Vector(namedtuple('VectorBase', 'x y z')):

    __slots__ = []

    def __repr__(self):
        return 'Vector(%.2g, %.2g, %.2g)' % (self.x, self.y, self.z)

    def __eq__(self, other):
        return (
            isinstance(other, tuple) and
            abs(self[0] - other[0]) < EPSILON and
            abs(self[1] - other[1]) < EPSILON and
            abs(self[2] - other[2]) < EPSILON
        )

    # __neq__ as 'not __eq__' seems to be inherited from tuple

    __hash__ = None # Vector are mutable, so do not allow hashing

    def __neg__(self):
        return Vector(-self.x, -self.y, -self.z)

    def __add__(self, other):
        ox, oy, oz = other
        return Vector(
            self.x + ox,
            self.y + oy,
            self.z + oz,
        )

    def __radd__(self, other):
        return self.__add__(other)

    def __sub__(self, other):
        return Vector(
            self.x - other[0],
            self.y - other[1],
            self.z - other[2],
        )

    def __rsub__(self, other):
        return Vector(*other).__sub__(self)

    def __mul__(self, scalar):
        return Vector(self.x * scalar, self.y * scalar, self.z * scalar)

    def __rmul__(self, scalar):
        return self.__mul__(scalar)

    def __truediv__(self, scalar):
        return Vector(self.x / scalar, self.y / scalar, self.z / scalar)

    @staticmethod
    def RandomCube(size, ints=False):
        rand = randint if ints else uniform
        return Vector(
            rand(-size, +size),
            rand(-size, +size),
            rand(-size, +size),
        )

    @staticmethod
    def RandomSphere(radius):
        while True:
            p = Vector.RandomCube(radius)
            if p.length2 < radius ** 2:
                break
        return p

    @property
    def length(self):
        '''
        the length
        '''
        return sqrt(self.x * self.x + self.y * self.y + self.z * self.z)

    @property
    def length2(self):
        '''
        the length squared
        '''
        return self.x ** 2 + self.y ** 2 + self.z ** 2

    def normalized(self):
        '''
        return a new vector in the same direction, but of length 1
        '''
        length = self.length
        return Vector(self.x / length, self.y / length, self.z / length)

    def cross(self, other):
        '''
        return a new vector, the cross product
        a x b = (a2b3 - a3b2, a3b1 - a1b3, a1b2 - a2b1)
        http://en.wikipedia.org/wiki/Cross_product
        '''
        return Vector(
            self.y * other.z - self.z * other.y,
            self.z * other.x - self.x * other.z,
            self.x * other.y - self.y * other.x)

    def dot(self, other):
        '''
        return the scalar dot product
        '''
        return self[0] * other[0] + self[1] * other[1] + self[2] * other[2]

    def angle(self, other):
        '''
        return the angle between this vector and the given one
        '''
        return acos(self.dot(other) / (self.length * other.length))

    def rotate(self, axis, angle):
        '''
        return a new vector, rotated about the given axis
        TODO: move this into matrix
        '''
        c = cos(-angle)
        t = 1 - c
        s = sin(-angle)

        # Matrix 'M' rotates about axis
        d11 = t * axis.x ** 2 + c
        d12 = t * axis.x * axis.y - s * axis.z 
        d13 = t * axis.x * axis.z + s * axis.y
        d21 = t * axis.x * axis.y + s * axis.z 
        d22 = t * axis.y ** 2 + c
        d23 = t * axis.y * axis.z - s * axis.x 
        d31 = t * axis.x * axis.z - s * axis.y
        d32 = t * axis.y * axis.z + s * axis.x 
        d33 = t * axis.z ** 2 + c

        # multiply M * self
        return Vector(
            d11 * self.x + d12 * self.y + d13 * self.z,
            d21 * self.x + d22 * self.y + d23 * self.z,
            d31 * self.x + d32 * self.y + d33 * self.z,
        )

origin = Vector(0, 0, 0)
x_axis = Vector(1, 0, 0)
y_axis = Vector(0, 1, 0)
z_axis = Vector(0, 0, 1)
neg_x_axis = Vector(-1,  0,  0)
neg_y_axis = Vector( 0, -1,  0)
neg_z_axis = Vector( 0,  0, -1)

