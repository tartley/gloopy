
from math import pi, degrees
from random import uniform

from OpenGL import GL

from .vector import Vector
from .matrix import Matrix



EPSILON = 1e-15
matrix_type = GL.GLfloat * 16


class Orientation(object):
    '''
    Defines an orientation by maintaining a `forward` and `up` vector (and a
    derived `right`, orthogonal to both.)

    .. function:: __init__(forward=None, up=None)
    
        Constructs an orientation looking along the `forward` vector. If none
        is given then defaul to the negative Z axis.

        If `up` is specified, it must lie at right angles to `forward`. If none
        is given then a default is chosen, the vector at right angles to forward
        which lies closest to the positive Y axis.

    Orientation.Identity, which results in zero rotation, is with forward
    pointing along the negative Z axis, up along the positive Y axis (and
    hence right along the positive X axis.)
    '''
    def __init__(self, forward=None, up=None):
        '''
        'forward' and 'up' should be Vector or 3-part tuple.
        If 'up' is omitted, a sensible default up vector is chosen.
        '''
        if forward is None:
            forward = Vector.ZNegAxis
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
        '''
        Return a new random Orientation
        '''
        fwd = Vector.RandomSphere(1)
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
        if self.forward == Vector.YAxis:
            return Vector.ZAxis
        elif self.forward == Vector.YNegAxis:
            return Vector.ZNegAxis

        # project 'forward' onto y=0 plane
        flat = Vector(self.forward.x, 0, self.forward.z)
        # find 'axis', a vector in the y=0 plane at right angles to 'flat'
        axis = flat.cross(Vector.YAxis)
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
        Rotate about the 'forward' axis (ie. +ve angle rolls to the right.)
        '''
        self.up = self.up.rotate(self.forward, -angle).normalized()
        self.right = self._get_right()


    def yaw(self, angle):
        '''
        Rotate about the 'down' axis (ie. +ve angle yaws to the right.)
        '''
        self.forward = self.forward.rotate(self.up, angle).normalized()
        self.right = self._get_right()


    def pitch(self, angle):
        '''
        Rotate about the 'right' axis (ie. +ve angle pitches up.)
        '''
        self.forward = self.forward.rotate(self.right, -angle).normalized()
        self.up = self.up.rotate(self.right, -angle).normalized()


    def rotate(self, axis, angle):
        '''
        Rotate about the given axis by the given angle.
        '''
        self.forward = self.forward.rotate(axis, angle)
        self.up = self.up.rotate(axis, angle)
        self.right = self._get_right()


    # This method is an ugly performance hack. Orientation shouldn't need
    # to import matrix, nor to know about ctypes. One day this will be
    # replaced by replacing every gameitem's position and orientation
    # attributes with a single attribute which stores position and
    # orientation stored natively as a ctypes matrix suitable for passing 
    # directly to glMultMatrix or shader uniforms.
    @property
    def matrix(self):
        '''
        The matrix that the OpenGL modelview matrix should be multiplied by
        to represent this orientation. It's likely that this method will
        disappear in later releases of Gloopy.
        '''
        if self._matrix is None:
            self._matrix = matrix_type( *Matrix(Vector.Origin, self) )
        return self._matrix


Orientation.Identity = Orientation()

# ugly hack to prevent cyclic imports
Matrix._zero_rotation = Orientation.Identity

