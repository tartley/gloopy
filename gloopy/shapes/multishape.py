
from .shape import Face
from ..geom.matrix import Matrix


class MultiShape(object):
    '''
    A composite of multiple Shapes. This allows many shapes to be stuck
    together and converted into a single Glyph, which means they are rendered
    as a single call to glDrawElements.

    This Multishape provides attributes that make it accessible like a normal
    shape:

    `vertices`: a sequence of all the vertices in all the child shapes, each
    one offset and oriented by that child shape's position and orientation.

    `faces`: a collection of all the Face instances of all the child shapes.

    .. function:: __init__()
    '''
    def __init__(self):
        self.vertices = []
        self.faces = []


    def add(self, shape, position=None, orientation=None):
        '''
        Add `shape` to this MultiShape's collection of children.
        The shape will be offset by `position` from the center of the
        MultiShape, and oriented by `orientation`.
        '''
        matrix = Matrix(position, orientation)
        child_offset = len(self.vertices)
        self.vertices.extend(self._child_vertices(shape, matrix))
        self.faces.extend(self._child_faces(shape, child_offset))


    def _child_vertices(self, child, matrix):
        return (
            matrix.transform(vertex)
            for vertex in child.vertices
        )


    def _child_faces(self, child, child_offset):
        faces = []

        for face in child.faces:
            new_indices = [
                index + child_offset
                for index in face.indices
            ]
            faces.append(
                Face( new_indices, face.color, self )
            )
        return faces

