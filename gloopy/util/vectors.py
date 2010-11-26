from random import randint, uniform

from ..geom.vec3 import Vec3


origin = Vec3(0, 0, 0)
x_axis = Vec3(1, 0, 0)
y_axis = Vec3(0, 1, 0)
z_axis = Vec3(0, 0, 1)
neg_x_axis = Vec3(-1, 0, 0)
neg_y_axis = Vec3(0, -1, 0)
neg_z_axis = Vec3(0, 0, -1)



def position_or_gameitem(position):
    if isinstance(position, Vec3):
        return position
    else:
        return position.position


def vec3_random_cube(size, ints=False):
    if ints:
        return Vec3(
            randint(-size/2, +size/2),
            randint(-size/2, +size/2),
            randint(-size/2, +size/2)
        ) 
    else:
        return Vec3(
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
    return orig.cross(friend).normalized()


