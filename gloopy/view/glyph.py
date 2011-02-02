
from ctypes import c_void_p
from itertools import chain

from OpenGL import GL
from OpenGL.arrays import vbo
from OpenGL.GL.ARB.vertex_array_object import (
    glGenVertexArrays, glBindVertexArray
)
from OpenGLContext.arrays import array

from ..color import Color


type_to_enum = {
    GL.GLubyte: GL.GL_UNSIGNED_BYTE,
    GL.GLushort: GL.GL_UNSIGNED_SHORT,
    GL.GLuint: GL.GL_UNSIGNED_INT,
}


def get_index_type(num_verts):
    '''
    The type of the glindices array depends on how many vertices there are
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
    arraytype = gltype * length
    return arraytype(*seq)


class Glyph(object):

    DIMENSIONS = 3

    def __init__(self, render, num_verts, verts, indices, colors, normals):
        self.render = render
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

        vao_id = GL.GLuint(0)
        glGenVertexArrays(1, vao_id)
        self.vao = vao_id.value

        glBindVertexArray(self.vao)
        try:
            self.vbo.bind()

            GL.glEnableVertexAttribArray( self.render.position_location )
            GL.glEnableVertexAttribArray( self.render.color_location )
            GL.glEnableVertexAttribArray( self.render.normal_location )

            STRIDE = 36
            GL.glVertexAttribPointer( 
                self.render.position_location, Glyph.DIMENSIONS, GL.GL_FLOAT,
                False, STRIDE, c_void_p(0)
            )
            GL.glVertexAttribPointer( 
                self.render.color_location, Color.COMPONENTS, GL.GL_FLOAT,
                False, STRIDE, c_void_p(12)
            )
            GL.glVertexAttribPointer( 
                self.render.normal_location, 3, GL.GL_FLOAT,
                False, STRIDE, c_void_p(24)
            )
        finally:
            glBindVertexArray(0)


    def __repr__(self):
        return '<Glyph %d verts>' % (self.num_glverts,)

