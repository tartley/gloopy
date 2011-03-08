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
        Vector.XAxis, Vector.YAxis, Vector.ZAxis,
        Vector.XNegAxis, Vector.YNegAxis, Vector.ZNegAxis
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
        position=Vector.Origin,
    )
    for pos in list(product(*repeat([-1, +1], 3))):
        multi.add(
            Cube(edge/2, repeat(color2)),
            position=Vector(*pos) * (edge / 2),
        )
    return multi


def CubeGlob(radius, number, colors):
    '''
    Return a new Shape consisting of a random glob of cubes arranged in a
    spherical shell.
    '''
    GAP = 20
    glob = MultiShape()
    cube = Cube(1, colors)
    for _ in xrange(number):
        pos = Vector.RandomSphere(radius - GAP)
        gap = pos.normalized() * GAP
        pos = pos + gap
        glob.add(
            cube,
            position=pos,
            orientation=Orientation(pos) )
    return glob


def RgbCubeCluster(edge, cluster_edge, cube_count, hole=0):
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
    cluster = MultiShape()
    for _ in xrange(cube_count):
        while True:
            pos = Vector(
                randint(-cluster_edge, +cluster_edge),
                randint(-cluster_edge, +cluster_edge),
                randint(-cluster_edge, +cluster_edge),
            )
            color = Color(
                int((pos.x + cluster_edge) / cluster_edge / 2 * 255),
                int((pos.y + cluster_edge) / cluster_edge / 2 * 255),
                int((pos.z + cluster_edge) / cluster_edge / 2 * 255),
            )
            # make a hole in the center
            if pos.length > hole:
                break
        cluster.add(
            Cube(edge, repeat(color)),
            position=pos
        )
    return cluster


def CubeCluster(locations):
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
            Cube(edge=1, colors=color),
            position=Vector(*location),
        )
    return multi


def BitmapCubeCluster(filename):
    img = image.load(join(path.DATA, 'images', filename))
    rawdata = img.get_image_data()
    channels = 'RGBA'
    pitch = rawdata.width * len(channels)
    pixels = rawdata.get_data(rawdata.format, rawdata.pitch)
    locations = {}
    for x in xrange(img.width):
        for y in xrange(img.height):
            index = x * 4 + y * pitch
            r, g, b, a = map(ord, pixels[index:index+4])
            if a > 0:
                cubex = x - img.width / 2
                cubey = img.height / 2 - y
                locations[cubex, cubey, 0] = Color(r, g, b)
    return CubeCluster(locations)

