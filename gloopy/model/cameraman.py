
from math import cos, sin


class CameraMan(object):

    def __init__(self, look_at_item, amplitude, frequency=0.2):
        self.look_at_item = look_at_item
        self.amplitude = amplitude
        self.frequency = frequency
        self.center = None
        self.last_position = (999,999,999)


    def __call__(self, item, dt, time):
        if item.position != self.last_position:
            self.center = item.position
        offset = (
            sin(time * self.frequency) * self.amplitude[0],
            cos(time * self.frequency) * self.amplitude[1],
            0)
        self.last_position = item.position = self.center + offset

        if self.look_at_item.position:
            item.look_at = self.look_at_item.position

