from __future__ import division

from .shape import add_vertex, Face


def extrude_face(shape, face_index, offset, new_category):
    '''
    Modify the given shape in-place, by extruding the specified face 'offset'.

    Doesn't work on Multishapes. This should get fixed in a future release.
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
    for i in range(len(face)):
        next_i = (i + 1) % len(face)
        indices = [face[i], face[next_i], new_indices[next_i], new_indices[i]]
        new_faces.append(
            Face(indices, face.color.inverted(), shape, face.category)
        )

    # new face on end of extrusion
    new_faces.append( Face(new_indices, face.color, shape, new_category) )

    shape.replace_face(face_index, new_faces)

    
def extrude(shape, faces=None, offset=0):
    """
    Modify the given shape in-place, by extruding the specified faces by
    `offset`.

    `faces` is an iterable of integer face indices upon which to operate. If
    omitted, it defaults to all faces.

    Doesn't work on Multishapes. This should get fixed in a future release.
    """
    if faces is None:
        faces = range(len(shape.faces))
    new_category = shape.next_category()
    for face in faces:
        extrude_face(shape, face, offset, new_category)

