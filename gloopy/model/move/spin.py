
from math import cos, sin

from ...geom.orientation import Orientation
from ...geom.vector import Vector


class Spinner(object):

    def __init__(self, speed=1.0):
        self.speed = speed
        self.orientation = Orientation(Vector.XAxis)

    def __call__(self, item, time, dt):
        self.orientation.pitch(sin(time) * dt * self.speed)
        self.orientation.roll(cos(time * 1.5) * dt * self.speed)
        item.orientation = self.orientation

