from __future__ import division


def normalize(original, length=1):
    """
    Normalizes the length of every vertex position to equal 'size', squishing
    the shape to become roughly spherical. Acts on the given Shape.
    """
    original.vertices = [
        v.normalized(length) for v in original.vertices
    ]
    # after moving vertices, we need to recalc the face normals
    for face in original.faces:
        face.normal = face.get_normal()
    return original

