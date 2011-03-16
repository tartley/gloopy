
from OpenGL import GL
from OpenGL.GL.shaders import compileShader, compileProgram


class Shader(object):
    '''
    Wraps PyOpenGL's shader compile and link functions

    .. function:: __init__(vertex, fragment, attributes)

        `vertex`: filename of vertex shader source code

        `fragment`: filename of fragment shader source code

        `attribs`: a list of attribute names

        Compiles and links the shader. For each attribute_name in
        `attribs`, looks up the attribute location, and stores it
        in self.attrib[attribute_name].

    Can be bound and unbound by use as a context-manager::

        shader = Shader('vert.glsl', 'frag.glsl', [])
        with shader:
            # draw calls
    '''

    def __init__(self, vert_src, frag_src, attribs):

        self.program = compileProgram(
            compileShader(vert_src, GL.GL_VERTEX_SHADER),
            compileShader(frag_src, GL.GL_FRAGMENT_SHADER)
        )

        self.attrib = {}
        for attrib in attribs:
            self.attrib[attrib] = GL.glGetAttribLocation(self.program, attrib)


    def __enter__( self ):
        """Start use of the program at start of a with block"""
        GL.glUseProgram( self.program )

    def __exit__( self, typ, val, tb ):
        """Stop use of the program at end of a with block"""
        GL.glUseProgram( 0 )

    def use(self):
        """Use the linked shader program"""
        GL.glUseProgram(self.program)

