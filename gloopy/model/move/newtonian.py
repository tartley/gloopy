
from ...geom.orientation import Orientation


class Newtonian(object):
    '''
    Modify locus if item.position by adding item.velocity to it.
    Similarly add item.velocity to item.acceleration, and add angular_velocity
    to item.orientation.
    '''
    def __call__(self, item, _, dt):
        if item.velocity is not None and item.acceleration is not None:
            item.velocity += item.acceleration * dt
        if item.position is not None and item.velocity is not None:
            item.position += item.velocity * dt 
        if item.angular_velocity:
            if item.orientation is None:
                item.orientation = Orientation()
            axis, speed = item.angular_velocity
            item.orientation.rotate(axis, speed * dt)

