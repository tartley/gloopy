from __future__ import division
from math import sin

from ...lib.euclid import Matrix4, Vector3
from ...util.vectors import any_orthogonal, y_axis


class Orbit(object):
    '''
    Move position in a circular locus around the given center point,
    with the given axis, radius and angular_velocity.
    '''
    def __init__(self, center, radius, axis=None, angular_velocity=1, phase=0):
        if hasattr(center, 'position') or isinstance(center, Vector3):
            self.center = center
        else:
            self.center = Vector3(center)
        self.radius = radius
        if axis is None:
            axis = y_axis
        else:
            axis.normalize()
        self.axis = axis
        self.angular_velocity = angular_velocity
        self.phase = phase

        self.unit_offset = any_orthogonal(axis)


    def __call__(self, item, time, dt):
        m = Matrix4.new_rotate_axis(
            self.phase + self.angular_velocity * time,
            self.axis
        )
        offset = m * self.unit_offset * self.radius
        if isinstance(self.center, Vector3):
            center = self.center
        else:
            center = self.center.position
        item.position = self.center + offset


class WobblyOrbit(Orbit):

    def __init__(
        self, center, radius, axis=None, angular_velocity=1, phase=0,
        wobble_size=0.5, wobble_freq=1
    ):
        super(WobblyOrbit, self).__init__(
            center, radius, axis, angular_velocity, phase)
        self.mean_radius = radius
        self.wobble_freq = wobble_freq
        self.wobble_size = wobble_size
        self.normalised_offset = any_orthogonal(axis)

    def __call__(self, item, time, dt):
        if self.wobble_size != 0:
            self.radius = self.mean_radius * (
                1 + sin(time * self.wobble_freq) * self.wobble_size
            )
        super(WobblyOrbit, self).__call__(item, time, dt)

