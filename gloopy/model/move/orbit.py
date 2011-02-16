from __future__ import division
from math import sin

from ...geom.vector import Vector
from ...model.item.gameitem import position_or_gameitem


class Orbit(object):
    '''
    Move position in a circular locus around the given center point,
    with the given axis, radius and angular_velocity.
    '''
    def __init__(self, center, radius, axis=None, angular_velocity=1, phase=0):
        if hasattr(center, 'position') or isinstance(center, Vector):
            self.center = center
        else:
            self.center = Vector(center)
        self.radius = radius
        if axis is None:
            axis = Vector.YAxis
        else:
            axis = axis.normalized()
        self.axis = axis
        self.angular_velocity = angular_velocity
        self.phase = phase
        self.unit_offset = axis.any_orthogonal()


    def __call__(self, item, time, dt):
        item.position = (
            position_or_gameitem(self.center) +
            self.radius * self.unit_offset.rotate(
                self.axis,
                self.phase + self.angular_velocity * time
            )
        )


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

    def __call__(self, item, time, dt):
        if self.wobble_size != 0:
            self.radius = self.mean_radius * (
                1 + sin(time * self.wobble_freq) * self.wobble_size
            )
        Orbit.__call__(self, item, time, dt)

