from __future__ import division
from math import cos, sin, pi

from euclid import Vector3

# TOOD:
# default for angular velocity
# default for axis (create 'util.quaternions module with default orientations)
# center should be either a location or a gameitem

class Orbit(object):
    '''
    Move position in a circular locus around the given center point,
    with the given axis, radius and angular_velocity.
    '''
    def __init__(self, center, radius, axis, angular_velocity=1, phase=0):
        self.center = center
        self.radius = radius
        self.axis = axis
        self.angular_velocity = angular_velocity
        self.phase = phase
        self.gameitem = None

    def __call__(self, time, _):
        bearing = self.phase + time * self.angular_velocity
        x = self.radius * sin(bearing)
        z = self.radius * cos(bearing)
        self.gameitem.position = Vector3(x, 0, z)

