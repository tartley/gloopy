from __future__ import division

from .shape import Shape
from ..geom.vector import origin


def add_vertex(vertices, vert):
    '''
    Add a vertex to the given list of vertices, and return the index number
    which should be used to refer to the new vertex. Modifies vertices in-place.
    '''
    vertices.append(vert)
    return len(vertices) - 1


def stellate(original, height):
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
        
        # new vertex at the face centroid
        # note: This isn't a good formula for the centroid,
        #       it only works for regular polygons
        vc = sum(orig_verts, origin) / len(orig_verts)
        # offset the new vertex out of the plane of the face
        vc += face.normal * (vc - orig_verts[0]).length * height
        # index of the new vertex
        ic = add_vertex(vertices, vc)

        for index in xrange(len(face)):
            index2 = (index + 1) % len(face)
            faces.append( [face[index], face[index2], ic] )
            colors.append( face.color )

    return Shape(vertices, faces, colors)

