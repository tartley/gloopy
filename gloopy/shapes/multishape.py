
from .shape import Face
from ..geom.matrix import Matrix


class MultiShape(object):
    '''
    A composite of multiple Shapes. This allows many shapes to be stuck
    together and converted into a single Glyph, which means they are rendered
    as a single call to glDrawElements.
    '''
    def __init__(self):
        self.vertices = []
        self.faces = []


    def add(self, shape, position=None, orientation=None):
        matrix = Matrix(position, orientation)
        child_offset = len(self.vertices)
        self.vertices.extend(self.child_vertices(shape, matrix))
        self.faces.extend(self.child_faces(shape, child_offset))


    def child_vertices(self, child, matrix):
        return (
            matrix.transform(vertex)
            for vertex in child.vertices
        )


    def child_faces(self, child, child_offset):
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

