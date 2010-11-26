
from math import pi, degrees
from random import uniform

from ..geom.vec3 import Vec3
from ..util.gl import gl
from ..util.vectors import neg_y_axis, neg_z_axis, y_axis, z_axis


EPSILON = 1e-15
matrix_type = gl.GLfloat * 16

class Orientation(object):
    '''
    Define's an orientation by maintaining a forward and up vector (and a
    derived 'right' vector, orthogonal to both) which defines an orientation.
    The identity orientation, which results in zero rotation, is with forward
    pointing along the negative Z axis, up along the positive Y axis, and
    hence right along the positive X axis.
    '''
    def __init__(self, forward=None, up=None):
        '''
        'forward' and 'up' should be Vec3 or 3-part tuple.
        If 'up' is omitted, a sensible default up vector is chosen.
        '''
        if forward is None:
            forward = neg_z_axis
        elif not isinstance(forward, Vec3):
            forward = Vec3(*forward)
        self._forward = forward.normalized()

        if up is None:
            up = self._default_up()
        elif not isinstance(up, Vec3):
            up = Vec3(*up)
            angle_between = forward.angle(up)
            assert abs(angle_between - pi/2) < EPSILON, \
                "up (%s) must be 90deg to forward (%s), actually %f deg" % \
                (up, forward, degrees(angle_between))
        self._up = up.normalized()

        self.right = self._get_right()

        # cached return value for 'matrix' property. Needs reseting to None
        # whenever self.forward or self.up change.
        self._matrix = None


    def __repr__(self):
        return 'Orientation(%s, up=%s)' % (self.forward, self.up)

    def __eq__(self, other):
        return (
            isinstance(other, Orientation) and
            self.forward == other.forward and
            self.up == other.up)

    def __ne__(self, other):
        return not self.__eq__(other)

    __hash__ = None # Orientations are mutable, so do not allow hashing


    @staticmethod
    def Random():
        fwd = Vec3.Random(1)
        orientation = Orientation(fwd)
        orientation.roll(uniform(-pi, +pi))
        return orientation


    def _set_forward(self, new):
        self._forward = new
        self._matrix = None

    forward = property(lambda s: s._forward, _set_forward, None,
            'The forward vector')


    def _set_up(self, new):
        self._up = new
        self._matrix = None

    up = property(lambda s: s._up, _set_up, None,
            'The up vector')


    def _default_up(self):
        '''
        returns a sensible default up vector (ie. orthogonal to forward,
        but pointed as near to the Y axis as possible)
        '''
        # special case for forward is y-axis or negative y-axis
        if self.forward == y_axis:
            return z_axis
        elif self.forward == neg_y_axis:
            return neg_z_axis

        # project 'forward' onto y=0 plane
        flat = Vec3(self.forward.x, 0, self.forward.z)
        # find 'axis', a vector in the y=0 plane at right angles to 'flat'
        axis = flat.cross(y_axis)
        # rotate 'forward' by 90 deg about 'axis'
        up = self.forward.rotate(axis, -pi/2)
        return up.normalized()


    def _get_right(self):
        '''
        value of self.right is always derived from self.forward and self.up
        '''
        return self.forward.cross(self.up)


    def roll(self, angle):
        '''
        rotate about the 'forward' axis (ie. +ve angle rolls to the right)
        '''
        self.up = self.up.rotate(self.forward, -angle).normalized()
        self.right = self._get_right()


    def yaw(self, angle):
        '''
        rotate about the 'down' axis (ie. +ve angle yaws to the right)
        '''
        self.forward = self.forward.rotate(self.up, angle).normalized()
        self.right = self._get_right()


    def pitch(self, angle):
        '''
        rotate about the 'right' axis (ie. +ve angle pitches up)
        '''
        self.forward = self.forward.rotate(self.right, -angle).normalized()
        self.up = self.up.rotate(self.right, -angle).normalized()


    @property
    def matrix(self):
        '''
        The matrix that the OpenGL modelview matrix should be multiplied by
        to represent this orientation.
        TODO - remove this. If we want to obtain the matrix of an orientation,
        then either contruct a new matrix passing the orientation, or else
        store a matrix in the first place instead of an orientation.
        '''
        if self._matrix is None:
            self._matrix = matrix_type(
                self.right.x,    self.right.y,    self.right.z,   0,
                self.up.x,       self.up.y,       self.up.z,      0,
               -self.forward.x, -self.forward.y, -self.forward.z, 0,
                0,               0,               0,              1,
            )
        return self._matrix

