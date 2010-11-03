import logging
import sys
from os.path import join

from euclid import Vector3

from ..util import color
from ..util import path
from .item.exit import Exit
from .item.room import Room
from .item.wall import Wall


LEVEL_DIR = join(path.DATA, 'level')
sys.path.append(LEVEL_DIR)


class Level(object):
    '''
    Populates a given world object from items read from a level file
    '''
    def __init__(self, eventloop):
        self.eventloop = eventloop
        self.number = 0


    def clear(self, world):
        items = world.items.values()
        for item in items:
            world.remove(item)


    def load(self, world, number):
        self.clear(world)

        try:
            level = __import__('level%02d' % (number,))
        except ImportError:
            return False

        room_color = color.white
        if hasattr(level, 'room_color'):
            room_color = level.room_color

        wall_color = color.white
        if hasattr(level, 'wall_color'):
            wall_color = level.wall_color

        blocks = self.get_blocks(level.layout)
        room_size = self.get_room_size(blocks)   
        world.add(Room(*room_size, color=room_color))

        self.add_items(world, blocks, room_color, wall_color)
        self.number = number
        return True


    def get_blocks(self, layout):
        blocks = layout.split('\n~\n')
        return [block.split('\n') for block in blocks]


    def get_room_size(self, blocks):
        height = len(blocks)
        length = max(len(block) for block in blocks)
        width = max(
            len(line)
            for block in blocks
            for line in block
        )
        return (width, height, length)


    def add_items(self, world, blocks, room_color, wall_color):
        for y, block in enumerate(blocks):
            for z, line in enumerate(block):
                for x, char in enumerate(line):
                    position = Vector3(x, y, z)
                    if char in ' ~':
                        pass
                    elif char == '#':
                        world.add(
                            Wall(
                                size=(1, 1, 1),
                                position=position,
                                color=wall_color,
                            )
                        )
                    elif char == 's':
                        self.eventloop.player.position=position
                    elif char == 'e':
                        world.add(Exit(position))
                    elif char == 'c':
                        world.add(
                            self.eventloop.camera,
                            position=position,
                        )
                    else:
                        logging.error('unknown char %c loading level %d' % (
                            char, self.number))

