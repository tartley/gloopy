from __future__ import division

from euclid import Matrix4

from ...util.vectors import any_orthogonal, y_axis


class Orbit(object):
    '''
    Move position in a circular locus around the given center point,
    with the given axis, radius and angular_velocity.
    '''
    def __init__(self, center, radius, axis=None, angular_velocity=1, phase=0):
        self.center = center
        self.radius = radius
        if axis is None:
            axis = y_axis
        else:
            axis.normalize()
        self.axis = axis
        self.angular_velocity = angular_velocity
        self.phase = phase

        self.offset = any_orthogonal(axis) * radius

        self.gameitem = None


    def __call__(self, _, dt):
        m = Matrix4.new_rotate_axis(self.angular_velocity * dt, self.axis)
        self.offset = m * self.offset
        self.gameitem.position = self.center + self.offset
        
