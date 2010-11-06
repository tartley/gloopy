import logging
from os.path import join

import pyglet
from pyglet.event import EVENT_HANDLED
from pyglet.gl import gl
from pyglet.gl import gl_info

from .glyph import Glyph
from .modelview import ModelView
from .projection import Projection
from .shader import FragmentShader, ShaderProgram, VertexShader
from ..util import path
from ..util.color import Color


log = logging.getLogger(__name__)


type_to_enum = {
    gl.GLubyte: gl.GL_UNSIGNED_BYTE,
    gl.GLushort: gl.GL_UNSIGNED_SHORT,
    gl.GLuint: gl.GL_UNSIGNED_INT,
}


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
                    item.glyph = Glyph.FromShape(item.shape)
                else:
                    continue
            yield item


    def draw(self, world):
        gl.glClearColor(*world.background_color.as_floats())
        self.window.clear()
        self.draw_items(self.drawable_items(world))
        if self.options.display_fps:
            self.draw_hud()
        self.window.invalid = False
        return EVENT_HANDLED


    def draw_items(self, items):
        gl.glEnableClientState(gl.GL_NORMAL_ARRAY)
        self.projection.set_perspective(45)
        self.modelview.set_world()
        for item in items:
            gl.glPushMatrix()
            if item.position:
                gl.glTranslatef(*item.position)
            # TODO: item orientation
            gl.glVertexPointer(
                Glyph.DIMENSIONS,
                gl.GL_FLOAT,
                0,
                item.glyph.glvertices
            )
            gl.glColorPointer(
                Color.NUM_COMPONENTS,
                gl.GL_UNSIGNED_BYTE,
                0,
                item.glyph.glcolors
            )
            gl.glNormalPointer(gl.GL_FLOAT, 0, item.glyph.glnormals)
            gl.glDrawElements(
                gl.GL_TRIANGLES,
                len(item.glyph.glindices),
                type_to_enum[item.glyph.glindex_type],
                item.glyph.glindices
            )
            gl.glPopMatrix()

        gl.glDisableClientState(gl.GL_NORMAL_ARRAY)


    def draw_hud(self):
        self.projection.set_screen()
        self.modelview.set_identity()
        self.clock_display.draw()

