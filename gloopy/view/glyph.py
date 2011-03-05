
from ctypes import c_void_p
from itertools import chain

from OpenGL import GL
from OpenGL.arrays import vbo
from OpenGL.GL.ARB.vertex_array_object import glBindVertexArray
from OpenGLContext.arrays import array

from ..color import Color
from ..util.gl_wrap import glGenVertexArray
from ..geom.vector import Vector


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


def glarray(gltype, seq, length):
    '''
    Convert a list of lists into a flattened ctypes array, eg:
    [ (1, 2, 3), (4, 5, 6) ] -> (GLfloat*6)(1, 2, 3, 4, 5, 6)
    '''
    carray = (gltype * length)()
    carray[:] = seq
    return carray



class Glyph(object):
    '''
    Passed iterables of vertex positions, colors, normals and indices,
    converts them into ctypes arrays, stores them in a VBO, and then
    creates a VAO that can be used to bind them later for rendering.

    .. function:: __init__(num_verts, verts, colors, normals, indices)
    '''

    # currently we only support a single shader used to render the 
    # whole scene
    shader = None

    def __init__(self, num_verts, verts, colors, normals, indices):
        self.num_glverts = num_verts
        self.vbo = vbo.VBO(
            array(
                list(
                    list(chain(v, c.as_floats(), n))
                    for v, c, n in zip(verts, colors, normals)
                ),
                'f'
            ),
            usage='GL_STATIC_DRAW'
        )
        index_type = get_index_type(num_verts)
        self.glindices = glarray(index_type, indices, len(indices))
        self.index_type = type_to_enum[index_type]

        self.vao = glGenVertexArray()
        glBindVertexArray(self.vao)
        try:
            self.vbo.bind()

            GL.glEnableVertexAttribArray(self.shader.attrib['position'])
            GL.glEnableVertexAttribArray(self.shader.attrib['color'])
            GL.glEnableVertexAttribArray(self.shader.attrib['normal'])

            STRIDE = 40
            GL.glVertexAttribPointer( 
                Glyph.shader.attrib['position'], Vector.COMPONENTS, GL.GL_FLOAT,
                False, STRIDE, c_void_p(0)
            )
            GL.glVertexAttribPointer( 
                Glyph.shader.attrib['color'], Color.COMPONENTS, GL.GL_FLOAT,
                False, STRIDE, c_void_p(12)
            )
            GL.glVertexAttribPointer( 
                Glyph.shader.attrib['normal'], Vector.COMPONENTS, GL.GL_FLOAT,
                False, STRIDE, c_void_p(28)
            )
        finally:
            glBindVertexArray(0)

