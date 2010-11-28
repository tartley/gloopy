
from itertools import chain

from ..util.color import Color
from ..util.gl import gl


type_to_enum = {
    gl.GLubyte: gl.GL_UNSIGNED_BYTE,
    gl.GLushort: gl.GL_UNSIGNED_SHORT,
    gl.GLuint: gl.GL_UNSIGNED_INT,
}

def get_index_type(num_verts):
    '''
    The type of the glindices array depends on how many vertices there are
    '''
    if num_verts < 256:
        return gl.GLubyte
    elif num_verts < 65536:
        return gl.GLushort
    else:
        return gl.GLuint


def glarray(gltype, seq, length):
    '''
    Convert a list of lists into a flattened ctypes array, eg:
    [ (1, 2, 3), (4, 5, 6) ] -> (GLfloat*6)(1, 2, 3, 4, 5, 6)
    '''
    arraytype = gltype * length
    return arraytype(*seq)


class Glyph(object):

    DIMENSIONS = 3

    def __init__(self, num_verts, verts, indices, colors, normals):
        self.num_glverts = num_verts
        self.glverts = glarray(
            gl.GLfloat,
            verts,
            num_verts * Glyph.DIMENSIONS
        )
        index_type = get_index_type(num_verts)
        self.glindices = glarray(index_type, indices, len(indices))
        self.index_type = type_to_enum[index_type]
        self.glcolors = glarray(
            gl.GLubyte,
            chain(*colors),
            num_verts * Color.COMPONENTS) 

        array_length = num_verts * Glyph.DIMENSIONS
        self.glnormals = glarray(gl.GLfloat, chain(*normals), array_length)

    def __repr__(self):
        return '<Glyph %d verts>' % (self.num_glverts,)

