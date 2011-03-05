from itertools import chain

from ..view.glyph import Glyph
from .shape import add_vertex


def shape_to_glyph(shape):
    '''
    Return a new :class:`~gloopy.view.glyph.Glyph`, which contains the geometry
    of the given shape converted into an indexed vertex array stored in a VBO,
    ready for rendering in OpenGL as a single draw call.
    '''
    vertices = []
    indices = []

    for face in shape.faces:
        new_indices = {}
        color = face.color.as_floats()
        for old_index in _tessellate(face):
            if old_index not in new_indices:
                vertex = list(chain(
                    shape.vertices[old_index], color, face.normal)
                )
                new_indices[old_index] = add_vertex(vertices, vertex)
            indices.append(new_indices[old_index])

    return Glyph(vertices, indices)


def _tessellate(indices):
    '''
    Return the indices of the given face tesselated into triangles The
    triangles will be wound in the same direction as the original poly. Does
    not work for concave faces.

    e.g. [0, 1, 2, 3, 4] -> [0, 1, 2,  0, 2, 3,  0, 3, 4]
    '''
    for index in xrange(1, len(indices) - 1):
        yield indices[0]
        yield indices[index]
        yield indices[index + 1]
    
