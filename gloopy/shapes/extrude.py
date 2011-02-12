from __future__ import division

from .shape import add_vertex, Face


def extrude_face(shape, face_index, offset):
    '''
    Extrude the specified face of the given face by 'offset'
    '''
    face = shape.faces[face_index]

    offset = face.normal * offset

    # new vertices
    new_indices = []
    for index in face:
        new_indices.append(
            add_vertex(shape.vertices, shape.vertices[index] + offset)
        )

    # new faces for edges of extrusion
    new_faces = []
    source = '%s.%s' % (face.source, 'extrude-side')
    for i in xrange(len(face)):
        next_i = (i + 1) % len(face)
        indices = [face[i], face[next_i], new_indices[next_i], new_indices[i]]
        new_faces.append( Face(indices, face.color.inverted(), shape, source) )

    # new face on end of extrusion
    source = '%s.%s' % (face.source, 'extrude-end')
    new_faces.append( Face(new_indices, face.color, shape, source) )

    shape.replace_face(face_index, new_faces)

    
def extrude(shape, faces=None, offset=0):
    """
    Extrude the specified faces of the given Shape, by 'offset'.
    Faces is an iterable of integer face indices upon which to operate.
    Defaults to all faces.
    """
    if faces is None:
        faces = xrange(len(shape.faces))
    for face in faces:
        extrude_face(shape, face, offset)

