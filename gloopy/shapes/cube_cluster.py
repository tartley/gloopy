
from .cube import Cube
from .multishape import MultiShape


def CubeCluster(locations):
    multi = MultiShape()
    for location, color in locations.iteritems():
        multi.add(
            Cube(edge=1, colors=color),
            position=location,
        )
    return multi

