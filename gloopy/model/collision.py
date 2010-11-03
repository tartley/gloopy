
from euclid import Vector3

from ..util.vectors import tuple_of_ints


class Collision(object):
    '''
    detects if any objects in the world collide
    '''

    def __init__(self, world):
        world.item_added += self.world_add_item
        world.item_removed += self.world_remove_item
        self.occupied = {}

    def world_add_item(self, item):
        if hasattr(item, 'bounds'):
            position = (0, 0, 0)
            if hasattr(item, 'position'):
                position = item.position
            self.add_item(position, item)

    def world_remove_item(self, item):
        if hasattr(item, 'bounds'):
            position = (0, 0, 0)
            if hasattr(item, 'position'):
                position = item.position
            self.remove_item(position, item)


    def get_items(self, location):
        if location is None:
            return set()
        if isinstance(location, Vector3):
            location = tuple_of_ints(location)
        return self.occupied.get(location, set())


    def add_item(self, location, item):
        if isinstance(location, Vector3):
            location = tuple_of_ints(location)
        existing = self.occupied.get(location, set())
        existing.add(item)
        self.occupied[location] = existing


    def remove_item(self, location, item):
        if isinstance(location, Vector3):
            location = tuple_of_ints(location)
        existing = self.occupied.get(location, set())
        existing.remove(item)
        self.occupied[location] = existing


    def can_move_to(self, location):
        return not [ 
            item for item in self.get_items(location)
            if hasattr(item, 'collide') and item.collide
        ]


