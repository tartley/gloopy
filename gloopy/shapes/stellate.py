from __future__ import division

from .shape import Face, add_vertex
from ..geom.vector import origin


def stellate_face(shape, height, face_index):
    '''
    Stellate face 'face_index' of the given shape.
    '''
    face = shape.faces[face_index]
    verts = [shape.vertices[i] for i in face]
    
    # new vertex at the face centroid
    # note: This isn't a good formula for the centroid,
    #       it only works for regular polygons
    vc = sum(verts, origin) / len(verts)
    # offset the new vertex out of the plane of the face
    vc += face.normal * (vc - verts[0]).length * height
    # index of the new vertex
    ic = add_vertex(shape.vertices, vc)

    # create new faces and their colors
    new_faces = []
    source = '%s.%s' % (face.source, 'stellate')
    for i in xrange(len(face)):
        indices = [face[i], face[i+1], ic]
        new_faces.append( Face(indices, face.color, shape, source) )

    # replace the face being stellated with one of our new faces
    shape.faces[face_index] = new_faces.pop()
    # and append our remaining new faces to the shape
    while new_faces:
        shape.faces.append( new_faces.pop() )


def stellate(shape, height, faces=None):
    '''
    Stellate the faces of the given shape.
    By 'stellate' I mean add a new vertex in the middle of the face, raised
    by 'height' out of the plane of the face, and replace the original face by
    an n-sided pyramid connecting this new vertex to each of the original
    face's edges.
    By default, all faces are opertated on, but this can be overidden by
    specifying 'faces' as an iterable of integer face indices.
    Operates in-place on the given shape.
    '''
    if faces is None:
        faces = xrange(len(shape.faces))
    for face in faces:
        stellate_face(shape, height, face)

