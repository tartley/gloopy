from __future__ import division

from itertools import repeat, product
from random import randint

from .shape import MultiShape
from .cube import Cube
from ..color import Color
from ..geom.orientation import Orientation
from ..geom.vector import Vector


def CubeCross(edge, color1, color2):
    multi = MultiShape()

    multi.add(Cube(edge, repeat(color1)))

    for pos in [
        Vector.XAxis, Vector.YAxis, Vector.ZAxis,
        Vector.XNegAxis, Vector.YNegAxis, Vector.ZNegAxis
    ]:
        center = pos * (edge / 2)
        multi.add(
            Cube(1/2, repeat(color2)),
            position=center,
        )
    return multi


def CubeCorners(edge, color1, color2):
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

