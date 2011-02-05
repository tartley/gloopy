from __future__ import division

from .shape import Shape
from ..geom.vector import origin
from ..color import Color


def add_vertex(vertices, vert):
    '''
    Add a vertex to the given list of vertices, and return the index number
    which should be used to refer to the new vertex. Modifies vertices in-place.
    '''
    vertices.append(vert)
    return len(vertices) - 1


def nest(func, depth):
    '''
    Return the a new function which invokes the given function 'depth' times,
    passing in the return value from the previous invocation.
    '''
    def inner(arg):
        for _ in xrange(depth):
            arg = func(arg)
        return arg
    return inner


def subdivided(original):
    """
    Returns a new shape instance, copied from the given original but with
    each face subdivided into four triangles:
          /  \
         /____\
        / \  / \
       /___\/___\

    Requires that the original faces are all triangles to begin with.
    """
    vertices = original.vertices[:]
    faces = []
    colors = []

    color2 = original.faces[0].color.tinted(Color.Random(), 0.5)
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

        for indexlist, color in [
            ([face[0], ia, ic], face.color),
            ([ia, face[1], ib], face.color),
            ([ic, ib, face[2]], face.color),
            ([ic, ia, ib], color2),
        ]:
            faces.append(indexlist)
            colors.append(color)

    return Shape(vertices, faces, colors)


def subdivided_center(original):
    '''
    Returns a new Shape instance, copied from the given original but with each
    face subdivided into a fan of triangles with the fan nexus at the shape's
    centroid. Works on faces with any number of sides.
    '''
    vertices = original.vertices[:]
    faces = []
    colors = []

    for face in original.faces:
        
        # original vertices
        orig_verts = [vertices[f] for f in face]
        
        # new vertex at the face centroid, and its index
        # note: This isn't a good formula for the centroid,
        #       it only works for regular polygons
        vc = sum(orig_verts, origin) / len(orig_verts)
        ic = add_vertex(vertices, vc)

        for index in xrange(len(face)):
            index2 = (index + 1) % len(face)
            faces.append( [face[index], face[index2], ic] )
            colors.append( face.color )

    return Shape(vertices, faces, colors)


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

