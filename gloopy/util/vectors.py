
from ..geom.vec3 import origin, x_axis, y_axis


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

