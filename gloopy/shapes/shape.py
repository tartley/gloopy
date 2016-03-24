
from itertools import repeat

from ..geom.vector import Vector
from ..color import Color



def add_vertex(vertices, new_vert):
    '''
    Modifies `vertices` in-place by appending the given `new_vert`.
    Returns the index number of the new vertex.
    
    Loads of Shape-modifying algorithms seem to need this function. Can't make
    it a method because they often haven't constructed the shape instance yet.
    '''
    vertices.append(new_vert)
    return len(vertices) - 1


class Face(object):
    '''
    A single flat face that forms part of a Shape. Attributes are the params
    to the constructor below, plus:

        `normal`: A Vector, perpendicular to the face

    .. function:: __init__(indices, color, shape)

        `indices`: a list of int indices into the parent shape's vertex list

        `color`: an instance of Color

        `shape`: a reference to the parent Shape

    .. function:: __getitem__(n)

        Return the nth index, as an integer.

    .. function:: __iter__()

        Iterate through `indices`

    .. function:: __len__()

        Return the length of `indices`
    '''
    def __init__(self, indices, color, shape, category=0):
        self.indices = indices
        self.color = color
        self.shape = shape
        self.category = category # used when selecting which faces to operate on
        self.normal = self.get_normal()

    def __getitem__(self, index):
        return self.indices[index % len(self.indices)]

    def __iter__(self):
        return self.indices.__iter__()

    def __len__(self):
        return len(self.indices)

    def get_normal(self):
        '''
        Return the unit normal vector at right angles to this face.

        Note that the direction of the normal will be reversed if the
        face's winding is reversed.
        '''
        v0 = self.shape.vertices[self.indices[0]]
        v1 = self.shape.vertices[self.indices[1]]
        v2 = self.shape.vertices[self.indices[2]]
        a = v0 - v1
        b = v2 - v1
        return b.cross(a).normalized()

    @property
    def centroid(self):
        '''
        Warning: Not an accurate centroid, just the mean vertex position
        '''
        return sum(
            [self.shape.vertices[i] for i in self], Vector.origin
        ) / len(self.indices)


class Shape(object):
    '''
    Defines a polyhedron, a 3D shape with flat faces and straight edges.

    .. function:: __init__(vertices, faces, colors)

        `vertices`: a list of Vector points in 3D space, relative to the
        shape's center point.

        `faces`: a list of faces, where each face is a list of integer indices
        into the vertices list. The referenced vertices of a single
        face must form a coplanar ring defining the face's edges. Duplicate
        indices do not have to be given at the start and end of each face,
        the closed loop is implied.

        `colors`: a single Color which is applied to every face, or a sequence
        of colors, one for each face.

        See the source for factory functions like
        :func:`~gloopy.shapes.cube.Cube` for examples of constructing Shapes.
    '''    
    def __init__(self, vertices, faces, colors):

        # sanity checks
        len_verts = len(vertices)
        for face in faces:
            assert len(face) >= 3
            for index in face:
                assert 0 <= index < len_verts

        # convert vertices from tuple to Vector if required
        if len(vertices) > 0 and not isinstance(vertices[0], Vector):
            vertices = [Vector(*v) for v in vertices]

        # if color is a single color, then convert it to a sequence of
        # identical colors, one for each face
        if isinstance(colors, Color):
            colors = repeat(colors)

        self.vertices = vertices
        self.faces = [
            Face(face, color, self)
            for face, color in zip(faces, colors)
        ]

    def __repr__(self):
        return '<Shape %d verts, %d faces>' % (
            len(self.vertices), len(self.faces),
        )

    def get_edges(self):
        '''
        Return a set of pairs, each pair represents indices that start and end
        an edge. Contents of each pair is sorted. e.g Tetrahedron:
        { (0, 1), (1, 2), (0, 2), (0, 3), (1, 3), (2, 3), }
        '''
        edges = set()
        for face in self.faces:
            for i in range(len(face)):
                edges.add( tuple(sorted((face[i], face[i+1]))) )
        return edges


    def replace_face(self, index, new_faces):
        '''
        Replace the face at position 'index' in self.faces with the list of
        Face instances in 'new_faces'
        '''
        self.faces[index] = new_faces.pop()
        while new_faces:
            self.faces.append( new_faces.pop() )


    def next_category(self):
        '''
        Faces have integer 'categories', used when selecting particular
        faces to operate on. This method returns the lowest positive integer
        that isn't used by any faces, handy for assigning integers to
        new faces.
        '''
        used_categories = {face.category for face in self.faces}
        category = 0
        while category in used_categories:
            category += 1
        return category

