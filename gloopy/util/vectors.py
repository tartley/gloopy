
from euclid import Vector3


EPSILON = 1e-7
EPSILON2 = EPSILON ** 2

origin = Vector3(0, 0, 0)
x_axis = Vector3(1, 0, 0)
y_axis = Vector3(0, 1, 0)
z_axis = Vector3(0, 0, 1)
neg_x_axis = Vector3(-1, 0, 0)
neg_y_axis = Vector3(0, -1, 0)
neg_z_axis = Vector3(0, 0, -1)


def tuple_of_ints(vec3):
    return (
        int(round(vec3.x)),
        int(round(vec3.y)),
        int(round(vec3.z)),
    )


def dist2_from_int_ords(vector):
    return (vector - tuple_of_ints(vector)).magnitude_squared()

