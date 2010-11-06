
from euclid import Vector3

from ..util.color import Orange
from ..util.event import Event


class World(object):
    '''
    World is a collection of all the GameItems.
    
    Most of these GameItems are visible objects within
    the world, such as rooms or walls or the player. Some, such as the camera,
    have no shape attribute, hence are not visible, but they still get moved
    or otherwise updated as part of the world.update() method.

    The World, like the whole model package, should not know about
    whatever's doing the rendering, so we fire events whenever Gameitems are
    added or removed, so that our renderer (and whoever else is interested)
    can react accordingly.
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

