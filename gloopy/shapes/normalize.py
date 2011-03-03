from __future__ import division


def normalize(shape, length=1):
    """
    Modifies the given shape in-place, by normalizing the position of every
    vertex to lie at `length` distance from the center. This squishes the shape
    to make it roughly spherical.

    If the shape contains edges which have one face on one side, but more than
    one face on the other side, then normalizing will result in ugly split
    seams, through which the interior of the object will be visible.

    Doesn't work on Multishapes. This should get fixed in a future release.
    """
    shape.vertices = [
        v.normalized(length) for v in shape.vertices
    ]
    # after moving vertices, we need to recalc the face normals
    for face in shape.faces:
        face.normal = face.get_normal()
    return shape

