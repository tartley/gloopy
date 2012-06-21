'''
Factory functions that return a single MultiShape instance formed by
composing several cubes
'''
from __future__ import division

from itertools import repeat, product
from os.path import join
from random import randint

from pyglet import image

from .cube import Cube
from .multishape import MultiShape
from ..color import Color
from ..geom.orientation import Orientation
from ..geom.vector import Vector
from ..util import path


def CubeCross(edge, color1, color2):
    '''
    Return a new Shape, consisting of a single large cube, and six smaller
    ones sticking out of each of its faces.
    '''
    multi = MultiShape()

    multi.add(Cube(edge, repeat(color1)))

    for pos in [
        Vector.x_axis, Vector.y_axis, Vector.z_axis,
        Vector.neg_x_axis, Vector.neg_y_axis, Vector.neg_z_axis
    ]:
        center = pos * (edge / 2)
        multi.add(
            Cube(edge/2, repeat(color2)),
            position=center,
        )
    return multi


def CubeCorners(edge, color1, color2):
    '''
    Return a new Shape, consisting of a single, large cube, and eight smaller
    ones at each of its corners.
    '''
    multi = MultiShape()
    multi.add(
        Cube(edge, repeat(color1)),
        position=Vector.origin,
    )
    for pos in list(product(*repeat([-1, +1], 3))):
        multi.add(
            Cube(edge/2, repeat(color2)),
            position=Vector(*pos) * (edge / 2),
        )
    return multi


def CubeGlob(size, radius, number, colors):
    '''
    Return a new Shape consisting of a random glob of cubes arranged in a
    spherical shell.
    '''
    glob = MultiShape()
    cube = Cube(size, colors)
    for _ in xrange(number):
        glob.add(
            cube,
            position=Vector.RandomShell(radius),
            orientation=Orientation.Random()
        )
    return glob


def RgbCubeCluster(edge, cube_count, scale=1, hole=0):
    '''
    Return a new Shape consisting of a random array of cubes arranged within
    a large cube-shaped volume. The small cubes are colored by their position
    in RGB space.

    `edge`: the edge of a small cube

    `cluster_edge`: the edge of the large volume

    `cube_count`: the number of cubes to generate within the volume

    `hole`: if >0, leave an empty hole of this radius in the middle of the
        volume.
    '''
    locations = {}
    
    SIZE = 256
    for _ in xrange(cube_count):
        while True:
            r = randint(0, SIZE - 1) - SIZE / 2
            g = randint(0, SIZE - 1) - SIZE / 2
            b = randint(0, SIZE - 1) - SIZE / 2
            pos = Vector(r, g, b)
            # accept this entry if it isn't in the hole
            if pos.length > hole:
                locations[pos * scale] = Color(
                    r / SIZE * Color.CHANNEL_MAX,
                    g / SIZE * Color.CHANNEL_MAX,
                    b / SIZE * Color.CHANNEL_MAX,
                )
                break
    return CubeCluster(locations, edge=edge)


def CubeCluster(locations, edge=1):
    '''
    Returns a new shape, consisting of a cluster of cubes.

    :param locations: maps location of cubes to their color.
    :type locations: dict

    In future could be optimised to remove faces of cubes which are never
    visible due to abutting a neighbour.
    '''
    multi = MultiShape()
    for location, color in locations.iteritems():
        multi.add(
            Cube(edge=edge, colors=color),
            position=Vector(*location),
        )
    return multi


def BitmapAsDict(filename, edge=1):
    img = image.load(join(path.DATA, 'images', filename))
    rawdata = img.get_image_data()
    channels = 'RGBA'
    pitch = rawdata.width * len(channels)
    pixels = rawdata.get_data(rawdata.format, rawdata.pitch)
    locations = {}
    for x in xrange(img.width):
        for y in xrange(img.height):
            index = x * len(channels) + y * pitch
            r, g, b, a = map(
                lambda x: x / 255.0 * Color.CHANNEL_MAX,
                pixels[index:index+4]
            )
            if a > 0.1:
                cubex = x - img.width / 2 + 0.5
                cubey = img.height / 2 - y
                locations[cubex * edge, cubey * edge, 0] = Color(r, g, b, a)
    return locations


def BitmapCubeCluster(filename, edge=1):
    return CubeCluster( BitmapAsDict(filename, edge), edge=edge )

