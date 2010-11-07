from math import pi
from random import uniform

from euclid import Quaternion, Vector3


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


def orientation_random():
    return Quaternion.new_rotate_axis(
        uniform(0, pi), vec3_random(1)
    )



