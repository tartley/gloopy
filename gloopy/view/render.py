import logging

from OpenGL.GL.ARB.vertex_array_object import glBindVertexArray

import pyglet
from pyglet.event import EVENT_HANDLED
from pyglet import gl

from .modelview import ModelView
from .projection import Projection
from .shape_to_glyph import shape_to_glyph
from ..geom.vector import Vector
from ..geom.orientation import Orientation


log = logging.getLogger(__name__)


def log_opengl_version():
    '''
    Send OpenGL version and driver info to logfile
    '''
    log.info('\n    '.join([
        'opengl:',
        gl.gl_info.get_vendor(),
        gl.gl_info.get_renderer(),
        gl.gl_info.get_version(),
    ]) )
    


class Render(object):
    '''
    Render class does all the OpenGL rendering

    .. function:: __init__(window, camera, options)
    
        `world`: instance of :class:`~gloopy.world.World`.

        `window`: instance of pyglet Window class

        `camera`: gloopy camera (might be a GameItem instance)

        `options`: instance of :class:`~gloopy.util.options.Options`.
    '''
    def __init__(self, world, window, camera, options):
        self.world = world
        self.window = window
        self.projection = Projection(window)
        self.modelview = ModelView(camera)
        self.options = options
        self._bind_shape_to_glyph()
        self.clock_display = pyglet.clock.ClockDisplay()


    def _bind_shape_to_glyph(self):
        # adding items to the world should convert their shapes to a glyph
        def convert_item_shape_to_glyph(item):
            if item.shape:
                if isinstance(item.shape, list):
                    shapes = item.shape
                else:
                    shapes = [item.shape]
                item.glyph = [ shape_to_glyph(shape) for shape in shapes ]
                if not hasattr(item, 'frame') or item.frame is None:
                    item.frame = 0
        self.world.item_added += convert_item_shape_to_glyph


    def init(self):
        '''
        Set all initial OpenGL state, such as enabling DEPTH_TEST.
        '''
        log_opengl_version()
        gl.glEnable(gl.GL_DEPTH_TEST)
        gl.glEnable(gl.GL_POLYGON_SMOOTH)
        gl.glEnable(gl.GL_BLEND)
        gl.glBlendFunc(gl.GL_SRC_ALPHA, gl.GL_ONE_MINUS_SRC_ALPHA)
        gl.glHint(gl.GL_POLYGON_SMOOTH_HINT, gl.GL_NICEST)

        self.backface_culling = True



    def _set_backface_culling(self, value):
        self._backface_culling = value
        if self._backface_culling:
            gl.glCullFace(gl.GL_BACK)
            gl.glEnable(gl.GL_CULL_FACE)
        else:
            gl.glDisable(gl.GL_CULL_FACE)

    backface_culling = property(
        lambda s: s._backface_culling, _set_backface_culling, None,
        "Boolean property to get or set backface culling."
    )


    def clear_window(self, color):
        '''
        Clear window color and depth buffers, using the given color
        '''
        r, g, b, _ = color
        gl.glClearColor(r, g, b, 1.0)
        gl.glClear(gl.GL_COLOR_BUFFER_BIT | gl.GL_DEPTH_BUFFER_BIT)


    def draw_window(self):
        '''
        Redraw the whole window
        '''
        self.clear_window(self.world.background_color)
        self.projection.set_perspective(45)
        self.modelview.set_world()
        self.draw_world_items()
        if self.options.fps:
            self.draw_hud()
        self.window.invalid = False
        return EVENT_HANDLED


    def draw_world_items(self):
        '''
        Draw all items that have been added to the world
        '''
        shader = None
        for item in self.world:

            if not item.glyph:
                continue

            gl.glPushMatrix()

            if item.position != Vector.Origin:
                gl.glTranslatef(*item.position)
            if item.orientation != Orientation.Identity:
                gl.glMultMatrixf(item.orientation.matrix)

            glyph = item.glyph[item.frame]
            if glyph.shader is not shader:
                shader = glyph.shader
                shader.use()

            glBindVertexArray(glyph.vao)

            gl.glDrawElements(
                gl.GL_TRIANGLES,
                len(glyph.glindices),
                glyph.index_type,
                glyph.glindices
            )

            gl.glPopMatrix()

        glBindVertexArray(0)
        gl.glUseProgram(0)


    def draw_hud(self):
        '''
        Draw any display items overlaid on the world, such as FPS counter
        '''
        self.projection.set_screen()
        self.modelview.set_identity()
        gl.glEnableClientState(gl.GL_VERTEX_ARRAY)
        gl.glEnableClientState(gl.GL_COLOR_ARRAY)

        self.clock_display.draw()

        gl.glDisableClientState(gl.GL_VERTEX_ARRAY)
        gl.glDisableClientState(gl.GL_COLOR_ARRAY)

