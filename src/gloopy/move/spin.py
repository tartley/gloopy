
from math import cos, sin

from gloopy.geom.orientation import Orientation


class Spinner(object):
    '''
    Spin the item's orientation the given axis at the given angular_velocity
    '''
    def __init__(self, axis, speed=1.0, orientation=None):
        self.axis = axis
        self.speed = speed
        if orientation is None:
            orientation = Orientation()
        self.orientation=orientation

    def __call__(self, item, time, dt):
        item.orientation = item.orientation.rotate(self.axis, self.speed * dt)


class WobblySpinner(object):
    '''
    Spin the item's orientation around in a wobbly manner
    '''
    def __init__(self, speed=1.0):
        self.speed = speed

    def __call__(self, item, time, dt):
        orientation = item.orientation.pitch(sin(time) * dt * self.speed)
        item.orientation = orientation.roll(cos(time * 1.5) * dt * self.speed)

