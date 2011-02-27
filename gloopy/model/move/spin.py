
from math import cos, sin

from ...geom.orientation import Orientation


class Spinner(object):

    def __init__(self, orientation=None, speed=1.0):
        if orientation is None:
            orientation = Orientation()
        self.speed = speed
        self.orientation = orientation

    def __call__(self, item, time, dt):
        self.orientation.pitch(sin(time) * dt * self.speed)
        self.orientation.roll(cos(time * 1.5) * dt * self.speed)
        item.orientation = self.orientation

