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



def position_or_gameitem(position):
    if isinstance(position, Vector3):
        return position
    else:
        return position.position


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
    assert orig != origin
    # friend = any vector at all, so long as it isn't parallel to orig
    if abs(orig.x) < abs(orig.y):
        friend = x_axis
    else:
        friend = y_axis
    return orig.cross(friend).normalize()


def orientation_random(size=None):
    if size is None:
        size = uniform(0, pi)
    return Quaternion.new_rotate_axis( size, vec3_random(1) )

