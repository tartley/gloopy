from __future__ import division

from .gameitem import GameItem
from .wall import WallShape


def RoomBounds(xsize, ysize, zsize):
    bounds = set()
    bounds = bounds.union( set(
        (x, y, z)
        for x in [-1, xsize]
        for y in xrange(0, ysize)
        for z in xrange(0, zsize)
    ) )
    bounds = bounds.union( set(
        (x, y, z)
        for x in xrange(0, xsize)
        for y in [-1, ysize]
        for z in xrange(0, zsize)
    ) )
    bounds = bounds.union( set(
        (x, y, z)
        for x in xrange(0, xsize)
        for y in xrange(0, ysize)
        for z in [-1, zsize]
    ) )
    return bounds


def Room(xsize, ysize, zsize, color):
    '''
    Interior of room goes from:
        x: 0 to xsize-1
        y: 0 to ysize-1
        z: 0 to zsize-1
    Shape of Room is 0.5 larger than that in every direction, so that
    player (or any other 1.0 sized object) can sit at any location in
    the room and not intersect with the room walls
    '''
    return GameItem(
        shape=WallShape(
            (xsize, ysize, zsize),
            color=color,
            invert=True
        ),
        bounds=RoomBounds(xsize, ysize, zsize),
        collide=True,
    )

