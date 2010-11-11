
from ..lib.euclid import Vector3
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

    def update(self, t, dt):
        for item in self:
            if item.update:
                item.update(t, dt)

