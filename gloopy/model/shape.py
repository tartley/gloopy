
from itertools import repeat

from ..geom.matrix import Matrix4
from ..geom.vec3 import Vec3
from ..util.color import Color



class Face(object):
    '''
    A single flat face that forms part of a Shape.
    '''
    def __init__(self, indices, color, vertices):
        self.indices = indices
        self.color = color
        self.vertices = vertices
        self.normal = self.get_normal()


    def __getitem__(self, index):
        return self.indices[index]


    def __len__(self):
        return len(self.indices)


    def get_normal(self):
        '''
        Return the unit normal vector (at right angles to) this face.
        Note that the direction of the normal will be reversed if the
        face's winding is reversed.
        '''
        v0 = self.vertices[self.indices[0]]
        v1 = self.vertices[self.indices[1]]
        v2 = self.vertices[self.indices[2]]
        a = v0 - v1
        b = v2 - v1
        normal = b.cross(a).normalized()
        return normal



class Shape(object):
    '''
    Defines a polyhedron, a 3D shape with flat faces and straight edges.
    Each vertex defines a point in 3d space. Each face is a list of integer
    indices into the vertex array, forming a coplanar convex ring defining the
    face's edges. Each face has its own color.

    public interface to a Shape is:
        shape.vertices = [vec3, vec3, vec3...]
        shape.faces = [
            Face(vertices, color1, [1, 2, 3, 4]),
            Face(vertices, color2, [4, 5, 1, 9]),
            ...
        ]
    '''    
    def __init__(self, vertices, faces, colors):

        # sanity checks
        len_verts = len(vertices)
        for face in faces:
            assert len(face) >= 3
            for index in face:
                assert 0 <= index < len_verts

        # convert vertices from tuple to Vec3 if required
        if len(vertices) > 0 and not isinstance(vertices[0], Vec3):
            vertices = [Vec3(*v) for v in vertices]

        # if given one color (or a tuple that looks like a color)
        # instead of a sequence of colors,
        # then construct a sequence if identical colors out of it
        if (
            isinstance(colors, tuple) and
            len(colors) == 4 and
            isinstance(colors[0], int)
        ):
            colors = Color(*colors)
        if isinstance(colors, Color):
            colors = repeat(colors)

        self.vertices = vertices
        self.faces = [
            Face(face, color, vertices)
            for face, color in zip(faces, colors)
        ]

    def __repr__(self):
        return '<Shape %d verts, %d faces>' % (len(self.vertices), len(self.faces),)


class MultiShape(object):
    '''
    A composite of multiple Shapes. This allows many shapes to be stuck
    together in a single MultiShape, which is then attached to a GameItem,
    and is then rendered by Render as a single call to glDrawElements
    (as opposed to many calls, as would be done for a collection of
    individual Shapes)
    '''

    def __init__(self):
        self.vertices = []
        self.faces = []


    def add(self, shape, position=(0, 0, 0), orientation=None):
        matrix = Matrix4(position)
        if orientation is not None:
            matrix *= orientation.get_matrix()

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
            faces.append(Face(new_indices, face.color, self.vertices))

        return faces

