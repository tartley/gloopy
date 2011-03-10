
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
        self._children = []
        self._vertices = None
        self._faces = None


    def add(self, shape, position=None, orientation=None):
        '''
        Add `shape` to this MultiShape's collection of children.
        The shape will be offset by `position` from the center of the
        MultiShape, and oriented by `orientation`.
        '''
        matrix = Matrix(position, orientation)
        self._children.append((shape, matrix))


    @property
    def children(self):
        for shape, transform in self._children:
            if isinstance(shape, MultiShape):
                for subshape, subtransform in shape.children:
                    yield subshape, transform * subtransform
            else:
                yield shape, transform 


    @property
    def vertices(self):
        if self._vertices is None:
            self._vertices = [
                transform * vertex
                for child, transform in self.children
                for vertex in child.vertices
            ]
        return self._vertices


    @property
    def faces(self):
        child_offset = 0
        for child, _ in self.children:
            for face in child.faces:
                new_indices = [
                    index + child_offset
                    for index in face.indices
                ]
                yield Face( new_indices, face.color, self )
            child_offset += len(child.vertices)

