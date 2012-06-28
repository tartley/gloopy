from __future__ import division

from .shape import Face, add_vertex
from ..color import Color


def subdivide_face(shape, face_index, edges, color2, new_category):
    '''
    Modify the given `shape` in-place. Subdivides the single face at position
    `face_index`.

    `edges` should be a dictionary, which starts empty, but is filled by
    subdivide face for it's own internal bookkeeping. Pass in the same dict
    object for every call to subdivide_face on the same shape. See `subdivide`
    for an example of this.
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
    for i in xrange(len(face)):
        prev_i = (i - 1) % len(face)
        indices = [face[i], midpoints[i], midpoints[prev_i]]
        new_faces.append( Face(indices, face.color, shape, new_category) )

    # a new face in the center of 'face'
    indices = [midpoints[i] for i in xrange(len(face))]
    new_faces.append(
        Face(indices, color2, shape, face.category)
    )

    shape.replace_face(face_index, new_faces)


def subdivide(shape, faces=None, color=None):
    r'''
    Modify the given `shape` in-place. Subdivides each of its faces into
    new, smaller faces, by cutting off the corners::

                     v0
                     /\       
                    /  \
             mid[0]/----\mid[2]
                  / \  / \
                 /___\/___\
               v1  mid[1]  v2

    By default, all faces are operated on, but this can be overidden by
    specifying 'faces' as an iterable of integer face indices.
    '''
    if faces is None:
        faces = xrange(len(shape.faces))
    if color is None:
        color = Color.Random()

    edges = {}
    new_category = shape.next_category()
    for face in faces:
        subdivide_face(shape, face, edges, color, new_category)

