
from euclid import Vector3

from ..util.color import Color
from ..util.event import Event

from .collision import Collision


class World(object):
    '''
    World is a container for all of the model state.
    
    Specifically, it's just a collection of all the GameItems that are
    currently in existence. Most of these GameItems are visible objects within
    the world, such as rooms or walls or the player. Some, such as the camera,
    have no shape attribute, hence are not visible, but they still get moved or
    otherwise updated as part of the world.update() method.

    The World, and everything else in the model package should not know about
    the view package, so we fire events when items are added or removed from
    the world, so that the view can react accordingly.
    '''
    sky_color = Color(0.0, 0.1, 0.3, 1.0)

    def __init__(self):
        self.items = {}
        self.item_added = Event()
        self.item_removed = Event()
        self.collision = Collision(self)

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

