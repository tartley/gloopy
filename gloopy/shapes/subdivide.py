from __future__ import division

from .shape import Face, add_vertex


def subdivide_face(shape, face_index, edges):
    '''
    Subdivide face 'face_index' of the given shape.
    TODO: internalise edges. Make it reset every time a new shape is passed.
    '''
    face = shape.faces[face_index]

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
        next_i = (i + 1) % len(face)
        start = face[i]
        end = face[next_i]
        midpoints.append( get_index_of_midpoint(start, end) )

    # add new faces at each corner of face
    new_faces = []
    source = '%s.%s' % (face.source, 'subdivide-edge')
    for i in xrange(len(face)):
        prev_i = (i - 1) % len(face)
        indices = [face[i], midpoints[i], midpoints[prev_i]]
        new_faces.append( Face(indices, face.color, shape, source) )

    # add an extra face in the center of face
    source_center = '%s.%s' % (face.source, 'subdivide-center')
    indices = [midpoints[i] for i in xrange(len(face))]
    new_faces.append(
        Face(indices, face.color.inverted(), shape, source_center )
    )

    # TODO, make this a method on shape?
    # replace the face being stellated with one of our new faces
    shape.faces[face_index] = new_faces.pop()
    # and append our remaining new faces to the shape
    while new_faces:
        shape.faces.append( new_faces.pop() )


def subdivide(shape):
    r"""
    Given a shape consisting entirely of triangular faces, subdivide each of
    its faces by cutting the corners off to form new shapes.
                     v0
                     /\       vertices v0-v2 correspond to indices face[0:2]
                    /  \
             mid[0]/----\mid[2]
                  / \  / \
                 /___\/___\
               v1  mid[1]  v2
    """
    edges = {}
    for face in xrange(len(shape.faces)):
        subdivide_face(shape, face, edges)

