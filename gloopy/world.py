
from .color import Color
from .geom.vector import Vector
from .util.event import Event


class World(object):
    '''
    A collection of all the GameItems to be updated and rendered.
    Supports iteration through all added items, and indexing by item.id
    to get a particular item.
    
    Attributes:
    
    ``self.items``: a dict of all items that have been added, keyed by their
        shape.id attribute.

    ``self.item_added``: event which is fired after an item is added.

    ``self.item_removed``: event which is fired after an item is removed.

    ``self.update``: event which is fired on every update. Items or
        application code might want to register for this event if they want to
        do some work every frame that doesn't fit well within the 'update'
        method of an item.

    ``self.background_color``: color used to clear the screen before render
    '''
    def __init__(self):
        self.items = {}
        self.item_added = Event()
        self.item_removed = Event()
        self.update = Event()
        self.background_color = Color.Orange

    def __iter__(self):
        return self.items.itervalues()

    def __getitem__(self, itemid):
        return self.items[itemid]

    def add(self, item, position=None):
        '''
        add given item to the world. If position is not given, the item's
        existing position attribute is used.

        Fires the self.item_added event.
        '''
        if position is not None:
            if not isinstance(position, Vector):
                position = Vector(*position)
            item.position = position
        self.items[item.id] = item
        self.item_added.fire(item)

    def remove(self, item):
        '''
        remove the given item from the world.

        Fires the self.item_removed event.
        '''
        del self.items[item.id]
        self.item_removed.fire(item)
        item.position = None

    def update_all(self, t, dt):
        '''
        Calls item.update() on each item that has a populated update attribute.

        Fires the self.update event.
        '''
        self.update.fire(t, dt)
        for item in self:
            if item.update:
                item.update(item, t, dt)

