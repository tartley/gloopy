'''
Wrap any OpenGL functions which are fiddly to access via the raw bindings.
'''
import platform

from OpenGL import GL

if platform.system() == 'Darwin':

    from OpenGL.GL.APPLE import vertex_array_object

    def glGenVertexArray():
        '''
        Return the integer ID of the created vertex object array
        '''
        vao_id = GL.GLuint(0)
        vertex_array_object.glGenVertexArraysAPPLE(1, vao_id)
        return vao_id.value


else:

    from OpenGL.GL.ARB import vertex_array_object

    def glGenVertexArray():
        '''
        Return the integer ID of the created vertex object array
        '''
        return vertex_array_object.glGenVertexArrays(1)

