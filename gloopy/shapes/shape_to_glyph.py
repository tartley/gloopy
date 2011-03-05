
from ..view.glyph import Glyph
from .shape import add_vertex


def shape_to_glyph(shape):
    vertices = []
    colors = []
    normals = []
    indices = []

    for face in shape.faces:
        new_indices = {}
        for old_index in _tessellate(face):
            if old_index not in new_indices:
                new_indices[old_index] = add_vertex(
                    vertices, shape.vertices[old_index]
                )
                colors.append(face.color)
                normals.append(face.normal)
            indices.append(new_indices[old_index])

    return Glyph(
        len(vertices),
        vertices,
        colors,
        normals,
        indices
    )


def _tessellate(indices):
    '''
    Return the indices of the given face tesselated into a list of triangles,
    expressed as integer indices. The triangles will be wound in the
    same direction as the original poly. Does not work for concave faces.
    e.g. [0, 1, 2, 3, 4] -> [[0, 1, 2], [0, 2, 3], [0, 3, 4]]
    '''
    for index in xrange(1, len(indices) - 1):
        yield indices[0]
        yield indices[index]
        yield indices[index + 1]
    
