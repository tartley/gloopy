from ..gameitem import GameItem
from ..geom.vector import Vector


class Interpolate(object):

    def __init__(self, mover, rate=3):
        self.mover = mover
        self.rate = rate
        self.target = GameItem(position=Vector.origin)

    def __call__(self, item, time, dt):
        self.mover(self.target, time, dt)
        item.position += (self.target.position - item.position) * dt * self.rate

