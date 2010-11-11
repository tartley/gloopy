from math import pi
from random import uniform

from ..lib.euclid import Quaternion, Vector3


origin = Vector3(0, 0, 0)
x_axis = Vector3(1, 0, 0)
y_axis = Vector3(0, 1, 0)
z_axis = Vector3(0, 0, 1)
neg_x_axis = Vector3(-1, 0, 0)
neg_y_axis = Vector3(0, -1, 0)
neg_z_axis = Vector3(0, 0, -1)


def vec3_random(size):
    return Vector3(
        uniform(-size, size),
        uniform(-size, size),
        uniform(-size, size),
    )


def any_orthogonal(orig):
    '''
    return any unit vector at right angles to the given vector
    '''
    # friend = any vector at all, so long as it isn't == orig
    friend = y_axis if orig != y_axis else x_axis
    return orig.cross(friend).normalize()


def orientation_random():
    return Quaternion.new_rotate_axis(
        uniform(0, pi), vec3_random(1)
    )

