from ctypes import c_void_p, sizeof

from OpenGL import GL
from OpenGL.arrays import vbo

from ..color import Color
from ..geom.vector import Vector
from . import gl_wrap


type_to_enum = {
    GL.GLubyte: GL.GL_UNSIGNED_BYTE,
    GL.GLushort: GL.GL_UNSIGNED_SHORT,
    GL.GLuint: GL.GL_UNSIGNED_INT,
}


def get_index_type(num_verts):
    '''
    Return the unsigned integer data type required to store the given number.
    e.g. 255 can be stored in a GLubyte, whereas 256 rrequires a GLushort.
    '''
    if num_verts < 256:
        return GL.GLubyte
    elif num_verts < 65536:
        return GL.GLushort
    else:
        return GL.GLuint


def glarray(gltype, seq):
    '''
    Puts the given sequence into a ctypes array of gltypes.
    [ 1, 2, 3, 4, 5, 6 ] -> (GLfloat*6)(1, 2, 3, 4, 5, 6)
    '''
    # construct and populate [:] is faster than construct with *seq
    carray = (gltype * len(seq))()
    carray[:] = seq
    return carray


class Glyph(object):
    '''
    Converts lists of vertices and indices into OpenGL vertex arrays stored
    in a VBO. Creates a VAO that can be used to bind them for rendering.

    .. function:: __init__(vertices, indices)

        :param vertices: each tuple contains attributes of one vertex
        :type vertices: list of tuples of numbers
        :param indices: order in which vertices should be drawn
        :type indices: list of integers

        The `vertex` list should be structured as follows (only the first
        vertex is shown)::

            vertices=[
                pos.x, pos.y, pos.z,
                color.r, color.g, color.b, color.a,
                normal.x, normal.y, normal.z,
                ...
            ]
    '''
    def __init__(self, vertices, indices, shader):
        FLOATS_PER_VERTEX = 10 # (x, y, z,  r, g, b, a,  nx, ny, nz)

        self.vbo = vbo.VBO(
            glarray(GL.GLfloat, vertices),
            usage='GL_STATIC_DRAW'
        )
        index_type = get_index_type(len(vertices) / FLOATS_PER_VERTEX)
        self.glindices = glarray(index_type, indices)
        self.index_type = type_to_enum[index_type]
        self.shader = shader

        self.vao = gl_wrap.glGenVertexArray()
        gl_wrap.glBindVertexArray(self.vao)
        try:
            self.vbo.bind()

            GL.glEnableVertexAttribArray(self.shader.attrib['position'])
            GL.glEnableVertexAttribArray(self.shader.attrib['color'])
            GL.glEnableVertexAttribArray(self.shader.attrib['normal'])

            STRIDE = FLOATS_PER_VERTEX * sizeof(GL.GLfloat)
            GL.glVertexAttribPointer( 
                self.shader.attrib['position'], len(Vector._fields), GL.GL_FLOAT,
                False, STRIDE, c_void_p(0)
            )
            GL.glVertexAttribPointer( 
                self.shader.attrib['color'], len(Color._fields), GL.GL_FLOAT,
                False, STRIDE, c_void_p(12)
            )
            GL.glVertexAttribPointer( 
                self.shader.attrib['normal'], len(Vector._fields), GL.GL_FLOAT,
                False, STRIDE, c_void_p(28)
            )
        finally:
            gl_wrap.glBindVertexArray(0)

