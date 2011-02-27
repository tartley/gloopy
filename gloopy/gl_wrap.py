
from OpenGL import GL
from OpenGL.GL.ARB import vertex_array_object

def glGenVertexArrays(count):
    vao_id = GL.GLuint(0)
    vertex_array_object.glGenVertexArrays(1, vao_id)
    return vao_id.value

