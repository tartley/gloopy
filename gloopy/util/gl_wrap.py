'''
Wrap any OpenGL functions which are fiddly to access via the raw bindings.
'''
from OpenGL.GL.ARB import vertex_array_object

def glGenVertexArray():
    '''
    Return the integer ID of the created vertex object array
    '''
    return vertex_array_object.glGenVertexArrays(1)

