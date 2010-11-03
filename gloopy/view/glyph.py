
from itertools import chain, repeat

from pyglet.gl import gl

from ..util.color import Color


def glarray(gltype, seq, length):
    '''
    Convert a list of lists into a flattened ctypes array, eg:
    [ (1, 2, 3), (4, 5, 6) ] -> (GLfloat*6)(1, 2, 3, 4, 5, 6)
    '''
    arraytype = gltype * length
    return arraytype(*seq)


def tessellate(indices):
    '''
    Return the indices of the given face tesselated into a list of triangles,
    expressed as integer indices. The triangles will be wound in the
    same direction as the original poly. Does not work for concave faces.
    e.g. Face(verts, [0, 1, 2, 3, 4]) -> [[0, 1, 2], [0, 2, 3], [0, 3, 4]]
    '''
    return (
        [indices[0], indices[index], indices[index + 1]]
        for index in xrange(1, len(indices) - 1)
    )


class Glyph(object):

    DIMENSIONS = 3

    @staticmethod
    def FromShape(shape):
        glyph = Glyph()
        vertices = list(shape.vertices)
        faces = list(shape.faces)
        glyph.glvertices = glyph.get_glvertices(vertices, faces)
        glyph.glindices = glyph.get_glindices(faces)
        glyph.glcolors = glyph.get_glcolors(faces)
        glyph.glnormals = glyph.get_glnormals(vertices, faces)
        return glyph


    def __init__(self):
        self.num_glvertices = None
        self.glvertices = None
        self.glindex_type = None
        self.glindices = None
        self.glcolors = None
        self.glnormals = None


    def __repr__(self):
        return '<Glyph %d verts>' % (self.num_glvertices,)

    def get_num_glvertices(_, faces):
        return len(list(chain(*faces)))


    def get_glvertices(self, vertices, faces):
        glverts = chain.from_iterable(
            vertices[index]
            for face in faces
            for index in face
        )
        self.num_glvertices = self.get_num_glvertices(faces)
        array_length = self.num_glvertices * Glyph.DIMENSIONS
        return glarray(gl.GLfloat, glverts, array_length)


    def get_glindex_type(self):
        '''
        The type of the glindices array depends on how many vertices there are
        '''
        if self.num_glvertices < 256:
            index_type = gl.GLubyte
        elif self.num_glvertices < 65536:
            index_type = gl.GLushort
        else:
            index_type = gl.GLuint
        return index_type


    def get_glindices(self, faces):
        glindices = []
        face_offset = 0
        for face in faces:
            indices = xrange(face_offset, face_offset + len(face))
            glindices.extend(chain(*tessellate(indices)))
            face_offset += len(face)
        self.glindex_type = self.get_glindex_type()
        return glarray(self.glindex_type, glindices, len(glindices))


    def get_glcolors(self, faces):
        glcolors = chain.from_iterable(
            repeat(face.color, len(face))
            for face in faces
        )
        return glarray(
            gl.GLubyte,
            chain(*glcolors),
            self.num_glvertices * Color.NUM_COMPONENTS) 


    def get_glnormals(self, vertices, faces):
        glnormals = chain.from_iterable(
            repeat(face.normal, len(face))
            for face in faces
        )
        array_length = self.num_glvertices * Glyph.DIMENSIONS
        return glarray(gl.GLfloat, chain(*glnormals), array_length)

