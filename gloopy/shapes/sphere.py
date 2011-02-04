from __future__ import division

from .shape import Shape


def add_vertex(vertices, vert):
    vertices.append(vert)
    return len(vertices) - 1


def Subdivided(original):
    """
    Subdivides all triangular faces of original shape into 4 smaller triangles.
    Barfs if any face is not triangular. Returns a new Shape.
    """
    vertices = original.vertices[:]
    faces = []
    colors = []

    for face in original.faces:
        assert len(face.indices) == 3

        # original vertices
        v0 = vertices[face[0]]
        v1 = vertices[face[1]]
        v2 = vertices[face[2]]

        # new vertices at the edge midpoints
        ma = (v0 + v1) / 2
        mb = (v1 + v2) / 2
        mc = (v2 + v0) / 2

        # indices of new vertices
        ia = add_vertex(vertices, ma)
        ib = add_vertex(vertices, mb)
        ic = add_vertex(vertices, mc)

        for indexlist in [
            [face[0], ia, ic],
            [ia, face[1], ib],
            [ic, ib, face[2]],
            [ic, ia, ib],
        ]:
            faces.append(indexlist)
            colors.append( face.color )

    return Shape(vertices, faces, colors)


def Normalize(original, length=1):
    """
    Normalizes the length of every vertex position to equal 'size', squishing
    the shape to become roughly spherical. Acts on the given Shape.
    """
    original.vertices = [
        v.normalized(length) for v in original.vertices
    ]
    for face in original.faces:
        face.normal = face.get_normal()
    return original

