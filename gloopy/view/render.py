import logging

from OpenGL.GL.ARB.vertex_array_object import glBindVertexArray

import pyglet
from pyglet.event import EVENT_HANDLED
from pyglet import gl

from .modelview import ModelView
from .projection import Projection
from .shader import Shader
from ..shapes.shape import shape_to_glyph


log = logging.getLogger(__name__)


def log_opengl_version():
    log.info('\n    '.join([
        'opengl:',
        gl.gl_info.get_vendor(),
        gl.gl_info.get_renderer(),
        gl.gl_info.get_version(),
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
        gl.glEnable(gl.GL_DEPTH_TEST)
        gl.glEnable(gl.GL_POLYGON_SMOOTH)
        gl.glEnable(gl.GL_BLEND)
        gl.glBlendFunc(gl.GL_SRC_ALPHA, gl.GL_ONE_MINUS_SRC_ALPHA)
        gl.glHint(gl.GL_POLYGON_SMOOTH_HINT, gl.GL_NICEST)

        gl.glCullFace(gl.GL_BACK)
        gl.glEnable(gl.GL_CULL_FACE)

        self.shader = Shader(
            'lighting.vert', 'lighting.frag',
            attribs=['position', 'color', 'normal']
        )


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
                    item.glyph = shape_to_glyph(item.shape, self.shader)
                else:
                    continue
            yield item


    def clear_window(self, color):
        r, g, b = color.as_floats()[:3]
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

        with self.shader:

            for item in items:
                gl.glPushMatrix()

                if item.position:
                    gl.glTranslatef(*item.position)
                if item.orientation:
                    gl.glMultMatrixf(item.orientation.matrix)

                glBindVertexArray(item.glyph.vao)

                gl.glDrawElements(
                    gl.GL_TRIANGLES,
                    len(item.glyph.glindices),
                    item.glyph.index_type,
                    item.glyph.glindices
                )

                gl.glPopMatrix()

            glBindVertexArray(0)


    def draw_hud(self):
        self.projection.set_screen()
        self.modelview.set_identity()
        gl.glEnableClientState(gl.GL_VERTEX_ARRAY)
        gl.glEnableClientState(gl.GL_COLOR_ARRAY)

        self.clock_display.draw()

        gl.glDisableClientState(gl.GL_VERTEX_ARRAY)
        gl.glDisableClientState(gl.GL_COLOR_ARRAY)

