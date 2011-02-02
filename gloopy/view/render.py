from ctypes import c_void_p
import logging
from os.path import join

from OpenGL.GL.shaders import compileShader, compileProgram

import pyglet
from pyglet.event import EVENT_HANDLED
from pyglet import gl

from .glyph import Glyph
from .modelview import ModelView
from .projection import Projection
from ..model.shape import shape_to_glyph
from ..util import path
from ..util.color import Color


log = logging.getLogger(__name__)


def log_opengl_version():
    log.info('\n    '.join([
        'opengl:',
        gl.gl_info.get_vendor(),
        gl.gl_info.get_renderer(),
        gl.gl_info.get_version(),
    ]) )
    

def read_shader(filename):
    with open(join(path.DATA, 'shaders', filename)) as fp:
        return fp.read()


class Render(object):

    def __init__(self, window, camera, options):
        self.window = window
        self.projection = Projection(window)
        self.modelview = ModelView(camera)
        self.options = options
        self.clock_display = pyglet.clock.ClockDisplay()

    def init(self):
        log_opengl_version()
        gl.glEnable(gl.GL_DEPTH_TEST)
        gl.glEnable(gl.GL_POLYGON_SMOOTH)
        gl.glEnable(gl.GL_BLEND)
        gl.glBlendFunc(gl.GL_SRC_ALPHA, gl.GL_ONE_MINUS_SRC_ALPHA)
        gl.glHint(gl.GL_POLYGON_SMOOTH_HINT, gl.GL_NICEST)

        gl.glCullFace(gl.GL_BACK)
        gl.glEnable(gl.GL_CULL_FACE)

        self.shader = compileProgram(
            compileShader(read_shader('lighting.vert'), gl.GL_VERTEX_SHADER),
            compileShader(read_shader('lighting.frag'), gl.GL_FRAGMENT_SHADER)
        )
        self.position_location = gl.glGetAttribLocation( self.shader, 'position' )
        self.color_location = gl.glGetAttribLocation( self.shader, 'color' )
        self.normal_location = gl.glGetAttribLocation( self.shader, 'normal' )


    def drawable_items(self, world):
        '''
        Generator function, returns an iterator over all items in the world
        which have a glyph attribute. If an item doesn't have a glyph, but
        does have a shape, then we generate its glyph and include it in the
        iteration.
        '''
        for item in world:
            if not item.glyph:
                if item.shape:
                    item.glyph = shape_to_glyph(item.shape)
                else:
                    continue
            yield item


    def clear_window(self, color):
        r, g, b = color.as_floats()
        gl.glClearColor(r, g, b, 1.0)
        gl.glClear(gl.GL_COLOR_BUFFER_BIT | gl.GL_DEPTH_BUFFER_BIT)


    def draw(self, world):
        self.clear_window(world.background_color)
        self.draw_items(self.drawable_items(world))
        if self.options.fps:
            self.draw_hud()
        self.window.invalid = False
        return EVENT_HANDLED


    def draw_items(self, items):
        self.projection.set_perspective(45)
        self.modelview.set_world()

        gl.glUseProgram(self.shader)
        gl.glEnableVertexAttribArray( self.position_location )
        gl.glEnableVertexAttribArray( self.color_location )
        gl.glEnableVertexAttribArray( self.normal_location )

        for item in items:
            gl.glPushMatrix()

            if item.position:
                gl.glTranslatef(*item.position)
            if item.orientation:
                gl.glMultMatrixf(item.orientation.matrix)

            item.glyph.vbo.bind()

            gl.glVertexAttribPointer( 
                self.position_location, Glyph.DIMENSIONS, gl.GL_FLOAT, False,
                item.glyph.stride, c_void_p(0)
            )
            gl.glVertexAttribPointer( 
                self.color_location, Color.COMPONENTS, gl.GL_FLOAT, False,
                item.glyph.stride, c_void_p(12)
            )
            gl.glVertexAttribPointer( 
                self.normal_location, 3, gl.GL_FLOAT, False,
                item.glyph.stride, c_void_p(24)
            )

            gl.glDrawElements(
                gl.GL_TRIANGLES,
                len(item.glyph.glindices),
                item.glyph.index_type,
                item.glyph.glindices
            )

            item.glyph.vbo.unbind()
            gl.glPopMatrix()

        gl.glDisableVertexAttribArray( self.position_location )
        gl.glDisableVertexAttribArray( self.color_location )
        gl.glDisableVertexAttribArray( self.normal_location )
        gl.glUseProgram(0)


    def draw_hud(self):
        self.projection.set_screen()
        self.modelview.set_identity()
        gl.glDisableClientState(gl.GL_NORMAL_ARRAY)
        self.clock_display.draw()

