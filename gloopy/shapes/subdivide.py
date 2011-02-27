from __future__ import division

from .shape import Face, add_vertex
from ..color import Color


def subdivide_face(shape, face_index, edges, color2=None):
    '''
    Subdivide face 'face_index' of the given shape.
    TODO: internalise edges. Make it reset every time a new shape is passed.
    '''
    face = shape.faces[face_index]
    if color2 is None:
        color2 = Color.Grey

    def get_index_of_midpoint(start, end):
        '''
        Given an edge of shape, specified by indices of the start and end verts
        Calculate the midpoint of this edge, add it to shape.vertices, and
        then return the index of this newly-added point.
        Return values are cached in 'edges', to prevent adding a midpoint to
        the same edge more than once.
        '''
        edge = tuple(sorted((start, end)))
        if edge not in edges:
            midpoint = (shape.vertices[start] + shape.vertices[end]) / 2
            edges[edge] = add_vertex(shape.vertices, midpoint)
        return edges[edge]

    # verts at the midpoint of each edge
    midpoints = []
    for i in xrange(len(face)):
        midpoints.append( get_index_of_midpoint(face[i], face[i+1]) )

    # new faces at each corner of 'face'
    new_faces = []
    source = '%s.%s' % (face.source, 'subdivide-corner')
    for i in xrange(len(face)):
        prev_i = (i - 1) % len(face)
        indices = [face[i], midpoints[i], midpoints[prev_i]]
        new_faces.append( Face(indices, face.color, shape, source) )

    # a new face in the center of 'face'
    source_center = '%s.%s' % (face.source, 'subdivide-center')
    indices = [midpoints[i] for i in xrange(len(face))]
    new_faces.append(
        Face(indices, color2, shape, source_center )
    )

    shape.replace_face(face_index, new_faces)


def subdivide(shape, faces=None, color=None):
    r"""
    Subdivide the faces of the given shape.
    Subdivision forms new, smaller faces by cutting the corners off a face.
                     v0
                     /\       vertices v0-v2 correspond to indices face[0:2]
                    /  \
             mid[0]/----\mid[2]
                  / \  / \
                 /___\/___\
               v1  mid[1]  v2
    By default, all faces are operated on, but this can be overidden by
    specifying 'faces' as an iterable of integer face indices.
    Operates in-place on the given shape.
    """
    if faces is None:
        faces = xrange(len(shape.faces))
    edges = {}
    if color is None:
        color = Color.Random()
    for face in faces:
        subdivide_face(shape, face, edges, color)

