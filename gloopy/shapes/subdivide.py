from __future__ import division

from .shape import Shape, add_vertex
from ..color import Color

def get_edges(shape):
    '''
    Return a set of pairs, each pair represents indices that start and end
    an edge. Contents of each pair is sorted. e.g Tetrahedron:
    { (0, 1), (1, 2), (0, 2), (0, 3), (1, 3), (2, 3), }
    '''
    edges = set()
    for face in shape.faces:
        for i in xrange(len(face)):
            next_i = (i + 1) % len(face)
            edges.add( tuple(sorted((face[i], face[next_i]))) )
    return edges


def subdivided(original):
    r"""
    Given a shape consisting entirely of triangular faces, returns a new Shape
    instance, copied from the given original but with each face subdivided into
    four triangles:  v0
                     /\                 v0-v2 correspond to indices i0-i2
                    /  \                ma-mc correspond to indices ia-ic
          edge0  ma/----\mc  edge2
                  / \  / \
                 /___\/___\
                v1   mb   v2

                    edge1
    """
    vertices = original.vertices[:]
    faces = []
    colors = []

    # map edges of the original: (start, end)
    # to index of the new vertex inserted at that edge's midpoint
    edges = {}

    for face in original.faces:
        assert len(face.indices) == 3

        # original indices
        i0 = face[0]
        i1 = face[1]
        i2 = face[2]

        # original vertices
        v0 = vertices[i0]
        v1 = vertices[i1]
        v2 = vertices[i2]

        # new vertices at the edge midpoints and their indices
        edge0 = tuple(sorted((i0, i1)))
        if edge0 not in edges:
            ma = (v0 + v1) / 2
            edges[edge0] = add_vertex(vertices, ma)
        ia = edges[edge0]

        edge1 = tuple(sorted((i1, i2)))
        if edge1 not in edges:
            mb = (v1 + v2) / 2
            edges[edge1] = add_vertex(vertices, mb)
        ib = edges[edge1]

        edge2 = tuple(sorted((i2, i0)))
        if edge2 not in edges:
            mc = (v2 + v0) / 2
            edges[edge2] = add_vertex(vertices, mc)
        ic = edges[edge2]

        color2 = face.color.inverted()
        for indexlist, color in [
            ([i0, ia, ic], face.color),
            ([ia, i1, ib], face.color),
            ([ic, ib, i2], face.color),
            ([ic, ia, ib], color2),
        ]:
            faces.append(indexlist)
            colors.append(color)

    return Shape(vertices, faces, colors)
