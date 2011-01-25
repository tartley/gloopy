
from math import pi, degrees
from random import uniform

from OpenGL import GL

from .vector import Vector, neg_y_axis, neg_z_axis, origin, y_axis, z_axis
from .matrix import Matrix



EPSILON = 1e-15
matrix_type = GL.GLfloat * 16


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
        'forward' and 'up' should be Vector or 3-part tuple.
        If 'up' is omitted, a sensible default up vector is chosen.
        '''
        if forward is None:
            forward = neg_z_axis
        elif not isinstance(forward, Vector):
            forward = Vector(*forward)
        self._forward = forward.normalized()

        if up is None:
            up = self._get_default_up()
        elif not isinstance(up, Vector):
            up = Vector(*up)
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
        fwd = Vector.RandomCube(1)
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


    def _get_default_up(self):
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
        flat = Vector(self.forward.x, 0, self.forward.z)
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


    def rotate(self, axis, angle):
        self.forward = self.forward.rotate(axis, angle)
        self.up = self.up.rotate(axis, angle)
        self.right = self._get_right()


    @property
    def matrix(self):
        '''
        The matrix that the OpenGL modelview matrix should be multiplied by
        to represent this orientation.
        '''
        if self._matrix is None:
            self._matrix = matrix_type( *Matrix(origin, self) )
        return self._matrix


identity = Orientation()

