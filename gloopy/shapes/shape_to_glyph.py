
from itertools import chain, repeat
from ..view.glyph import Glyph


def shape_to_glyph(shape):
    vertices = list(shape.vertices)
    faces = list(shape.faces)
    num_glverts = _get_num_verts(faces)
    return Glyph(
        num_glverts,
        _get_verts(vertices, faces, num_glverts),
        _get_indices(faces, num_glverts),
        _get_colors(faces, num_glverts),
        _get_normals(vertices, faces, num_glverts),
    )


def _get_num_verts(faces):
    return len(list(chain(*faces)))


def _get_verts(vertices, faces, num_glverts):
    return (
        vertices[index]
        for face in faces
        for index in face
    )


def _tessellate(indices):
    '''
    Return the indices of the given face tesselated into a list of triangles,
    expressed as integer indices. The triangles will be wound in the
    same direction as the original poly. Does not work for concave faces.
    e.g. [0, 1, 2, 3, 4] -> [[0, 1, 2], [0, 2, 3], [0, 3, 4]]
    '''
    return (
        [indices[0], indices[index], indices[index + 1]]
        for index in xrange(1, len(indices) - 1)
    )


def _get_indices(faces, num_glverts):
    indices = []
    face_offset = 0
    for face in faces:
        face_indices = xrange(face_offset, face_offset + len(face))
        indices.extend(chain(*_tessellate(face_indices)))
        face_offset += len(face)
    return indices


def _get_colors(faces, num_glverts):
    return chain.from_iterable(
        repeat(face.color, len(face))
        for face in faces
    )


def _get_normals(vertices, faces, num_glverts):
    return chain.from_iterable(
        repeat(face.normal, len(face))
        for face in faces
    )

