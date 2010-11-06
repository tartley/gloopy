
from euclid import Vector3

from ..util.color import Orange
from ..util.event import Event


class World(object):
    '''
    A collection of all the GameItems.
    '''
    def __init__(self):
        self.items = {}
        self.item_added = Event()
        self.item_removed = Event()
        self.background_color = Orange

    def __iter__(self):
        return self.items.itervalues()

    def add(self, item, position=None):
        if position is not None:
            if not isinstance(position, Vector3):
                position = Vector3(*position)
            item.position = position
        self.items[item.id] = item
        self.item_added.fire(item)

    def remove(self, item):
        del self.items[item.id]
        self.item_removed.fire(item)
        item.position = None

    def move(self, item, dt):
        '''
        Newtonian movement and spin
        '''
        if item.velocity is not None and item.acceleration is not None:
            item.velocity += item.acceleration * dt
        if item.position is not None and item.velocity is not None:
            item.position += item.velocity * dt
        if item.angular_velocity:
            speed, axis = item.angular_velocity.get_angle_axis()
            item.orientation.rotate_axis(speed * dt, axis)

    def update(self, t, dt):
        for item in self:
            self.move(item, dt)
            if item.update:
                item.update(t, dt)

