from __future__ import division
from collections import namedtuple
from math import acos, cos, sin, sqrt
from random import randint, uniform


EPSILON = 1e-7


class Vector(namedtuple('VectorBase', 'x y z')):
    '''
    3-component named tuple: (x, y, z), with some methods, including value
    type equality semantics.

    .. function:: __init__(x, y, z)

    Arithmetic operators are supported:

    .. function:: __neg__(): unary minus to invert direction
    .. function:: __add__(other): addition of vector or 3-tuple
    .. function:: __sub__(other): subtraction of vector or 3-tuple
    .. function:: __mul__(float): scale a vector
    .. function:: __div__(float): scale a vector (truediv also supported)
    '''

    __slots__ = []

    COMPONENTS = 3

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

    def __hash__(self):
        return hash(self.x) ^ hash(self.y) ^ hash(self.z)

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

    __div__ = __truediv__


    @staticmethod
    def RandomCube(size, ints=False):
        '''
        A new random Vector, evenly distributed within a cube of `size` sides.
        '''
        rand = randint if ints else uniform
        return Vector(
            rand(-size/2, +size/2),
            rand(-size/2, +size/2),
            rand(-size/2, +size/2),
        )

    @staticmethod
    def RandomSphere(radius):
        '''
        A new random Vector, evenly distributed within a sphere of `radius`.
        '''
        while True:
            p = Vector.RandomCube(radius)
            if p.length2 < radius ** 2:
                return p

    @staticmethod
    def RandomShell(radius):
        '''
        A new random Vector, evenly distributed on surface a sphere of `radius`.
        '''
        while True:
            p = Vector.RandomCube(radius)
            if p.length2 < radius ** 2:
                return p.normalized() * radius

    @property
    def length(self):
        return sqrt(self.x * self.x + self.y * self.y + self.z * self.z)

    @property
    def length2(self):
        '''
        Length squared. Cheaper to calculate.
        '''
        return self.x ** 2 + self.y ** 2 + self.z ** 2

    def normalized(self, length=1):
        '''
        Return a new vector in the same direction, but given length (default 1)
        '''
        factor = length / self.length
        return Vector(self.x * factor, self.y * factor, self.z * factor)

    def cross(self, other):
        '''
        Return a new vector, the cross product.
        a x b = (a2b3 - a3b2, a3b1 - a1b3, a1b2 - a2b1)
        This will be at right angles to both self and other, with a length:
            len(self) * len(other) * sin(angle_between_them)
        http://en.wikipedia.org/wiki/Cross_product
        '''
        return Vector(
            self.y * other.z - self.z * other.y,
            self.z * other.x - self.x * other.z,
            self.x * other.y - self.y * other.x
        )

    def dot(self, other):
        '''
        Return the scalar dot product
        '''
        return self[0] * other[0] + self[1] * other[1] + self[2] * other[2]

    def angle(self, other):
        '''
        return the angle between this vector and the given one
        '''
        return acos(self.dot(other) / (self.length * other.length))


    def rotateX(self, angle):
        '''
        return a new vector, rotated `angle` radians about the X axis
        '''
        sina = sin(angle)
        cosa = cos(angle)
        return Vector(
            self.x,
            self.y * cosa + self.z * sina,
            -self.y * sina + self.z * cosa)

    def rotateY(self, angle):
        '''
        return a new vector, rotated `angle` radians about the Y axis
        '''
        sina = sin(angle)
        cosa = cos(angle)
        return Vector(
            self.x * cosa - self.z * sina,
            self.y,
            self.x * sina + self.z * cosa)

    def rotateZ(self, angle):
        '''
        return a new vector, rotated `angle` radians about the Z axis
        '''
        sina = sin(angle)
        cosa = cos(angle)
        return Vector(
            self.x * cosa + self.y * sina,
            -self.x * sina + self.y * cosa,
            self.z
        )


    def rotate(self, axis, angle):
        '''
        Return a new vector, rotated about the given axis

        If rotating many verts around the same axis, consider creating a
        Matrix to represent the rotation instead, and calling m*v
        on each vertex, which might be faster.
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

       
    def any_orthogonal(self):
        '''
        Return any unit vector at right angles to the given vector
        '''
        assert self != Vector.Origin
        # friend = any vector at all, so long as it isn't parallel to orig
        if abs(self.x) < abs(self.y):
            friend = Vector.XAxis
        else:
            friend = Vector.YAxis
        return self.cross(friend).normalized()


Vector.Origin = Vector(0, 0, 0)
Vector.XAxis = Vector(1, 0, 0)
Vector.YAxis = Vector(0, 1, 0)
Vector.ZAxis = Vector(0, 0, 1)
Vector.XNegAxis = Vector(-1,  0,  0)
Vector.YNegAxis = Vector( 0, -1,  0)
Vector.ZNegAxis = Vector( 0,  0, -1)

