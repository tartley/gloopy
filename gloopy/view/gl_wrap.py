'''
Wrap any OpenGL functions which are fiddly to access via the raw bindings.
'''
import platform

from OpenGL import GL


def glGenVertexArray():
    return GL.ARB.vertex_array_object.glGenVertexArrays(1)

glBindVertexArray = GL.ARB.vertex_array_object.glBindVertexArray


if platform.system() == 'Darwin':
    from OpenGL.GL.APPLE import vertex_array_object

    def glGenVertexArray_apple():
        vao_id = GL.GLuint(0)
        vertex_array_object.glGenVertexArraysAPPLE(1, vao_id)
        return vao_id.value

    glGenVertexArray = glGenVertexArray_apple
    glBindVertexArray = vertex_array_object.glBindVertexArrayAPPLE

