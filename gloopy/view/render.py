from ctypes import c_void_p
import logging
from os.path import join

import pyglet
from pyglet.event import EVENT_HANDLED
from pyglet.gl import gl_info

from pyglet import gl

from .glyph import Glyph
from .modelview import ModelView
from .projection import Projection
from .shader import FragmentShader, ShaderProgram, VertexShader
from ..model.shape import shape_to_glyph
from ..util import path
from ..util.color import Color


log = logging.getLogger(__name__)


def log_opengl_version():
    log.info('\n    '.join([
        'opengl:',
        gl_info.get_vendor(),
        gl_info.get_renderer(),
        gl_info.get_version(),
    ]) )
    

class Render(object):

    def __init__(self, window, camera, options):
        self.window = window
        self.projection = Projection(window)
        self.modelview = ModelView(camera)
        self.options = options
        self.clock_display = pyglet.clock.ClockDisplay()

    def init(self):
        log_opengl_version()
        gl.glEnableClientState(gl.GL_VERTEX_ARRAY)
        gl.glEnableClientState(gl.GL_COLOR_ARRAY)
        gl.glEnable(gl.GL_DEPTH_TEST)
        gl.glEnable(gl.GL_POLYGON_SMOOTH)
        gl.glEnable(gl.GL_BLEND)
        gl.glBlendFunc(gl.GL_SRC_ALPHA, gl.GL_ONE_MINUS_SRC_ALPHA)
        gl.glHint(gl.GL_POLYGON_SMOOTH_HINT, gl.GL_NICEST)

        gl.glCullFace(gl.GL_BACK)
        gl.glEnable(gl.GL_CULL_FACE)

        shader = ShaderProgram(
            VertexShader(join(path.DATA, 'shaders', 'lighting.vert')),
            FragmentShader(join(path.DATA, 'shaders', 'lighting.frag')),
        )
        shader.compile()
        shader.use()


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

        gl.glEnableClientState(gl.GL_NORMAL_ARRAY)

        for item in items:
            gl.glPushMatrix()

            if item.position:
                gl.glTranslatef(*item.position)
            if item.orientation:
                gl.glMultMatrixf(item.orientation.matrix)

            item.glyph.vbo.bind()

            gl.glVertexPointer(
                Glyph.DIMENSIONS, gl.GL_FLOAT, item.glyph.stride, c_void_p( 0 )
            )
            gl.glColorPointer(
                Color.COMPONENTS, gl.GL_FLOAT, item.glyph.stride, c_void_p( 12 )
            )
            gl.glNormalPointer(
                gl.GL_FLOAT, item.glyph.stride, c_void_p( 24 )
            )

            gl.glDrawElements(
                gl.GL_TRIANGLES,
                len(item.glyph.glindices),
                item.glyph.index_type,
                item.glyph.glindices
            )
            item.glyph.vbo.unbind()
            gl.glPopMatrix()


    def draw_hud(self):
        self.projection.set_screen()
        self.modelview.set_identity()
        gl.glDisableClientState(gl.GL_NORMAL_ARRAY)
        self.clock_display.draw()

