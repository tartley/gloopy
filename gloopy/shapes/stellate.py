from __future__ import division

from .shape import Face, add_vertex


def stellate_face(shape, face_index, height):
    '''
    Stellate face 'face_index' of the given shape.
    '''
    face = shape.faces[face_index]
    
    # new vertex at the face centroid offset out of the plane of the face
    vc = face.centroid
    vc += face.normal * (vc - shape.vertices[face[0]]).length * height
    # index of the new vertex
    ic = add_vertex(shape.vertices, vc)

    # create new faces and their colors
    new_faces = []
    source = '%s.%s' % (face.source, 'stellate')
    for i in xrange(len(face)):
        indices = [face[i], face[i+1], ic]
        new_faces.append( Face(indices, face.color, shape, source) )

    shape.replace_face(face_index, new_faces)


def stellate(shape, faces=None, height=0):
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
        stellate_face(shape, face, height)

