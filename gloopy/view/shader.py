from os.path import join
from ..util import path

from OpenGL import GL
from OpenGL.GL.shaders import compileShader, compileProgram


def read_shader_file(filename):
    with open(join(path.SHADERS, filename)) as fp:
        return fp.read()


class Shader(object):

    def __init__(self, vert_filename, frag_filename, attribs):

        vert_src = read_shader_file(vert_filename)
        frag_src = read_shader_file(frag_filename)

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
        """Use the program"""
        GL.glUseProgram(self.program)

