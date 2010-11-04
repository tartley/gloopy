from os.path import join

import pyglet
from pyglet.gl import gl

from ..util import path
from ..util.color import Color
from .glyph import Glyph
from .modelview import ModelView
from .projection import Projection
from .shader import FragmentShader, ShaderProgram, VertexShader


type_to_enum = {
    gl.GLubyte: gl.GL_UNSIGNED_BYTE,
    gl.GLushort: gl.GL_UNSIGNED_SHORT,
    gl.GLuint: gl.GL_UNSIGNED_INT,
}


class Render(object):

    def __init__(self, world, window, camera):
        self.world = world
        self.projection = Projection(window)
        self.modelview = ModelView(camera)
        self.clock_display = pyglet.clock.ClockDisplay()


    def init(self):
        gl.glEnableClientState(gl.GL_VERTEX_ARRAY)
        gl.glEnableClientState(gl.GL_COLOR_ARRAY)
        gl.glEnable(gl.GL_DEPTH_TEST)
        gl.glEnable(gl.GL_POLYGON_SMOOTH)
        gl.glEnable(gl.GL_BLEND)
        gl.glBlendFunc(gl.GL_SRC_ALPHA, gl.GL_ONE_MINUS_SRC_ALPHA)
        gl.glHint(gl.GL_POLYGON_SMOOTH_HINT, gl.GL_NICEST)

        gl.glCullFace(gl.GL_BACK)
        gl.glEnable(gl.GL_CULL_FACE)

        gl.glClearColor(*self.world.sky_color)

        vs_file = join(path.SOURCE, 'view', 'shaders', 'lighting.vert')
        vs = VertexShader(vs_file)
        fs_file = join(path.SOURCE, 'view', 'shaders', 'lighting.frag')
        fs = FragmentShader(fs_file)
        shader = ShaderProgram(vs, fs)
        shader.compile()
        shader.use()

        # create glyphs for every item added to the world before now
        for item in self.world:
            self.world_add_item(item)
        # create glyphs for every item added after this
        self.world.item_added += self.world_add_item


    def world_add_item(self, item):
        '''
        convert the given item's shape into a glyph, for rendering
        '''
        if item.shape and not item.glyph:
            item.glyph = Glyph.FromShape(item.shape)


    def draw_world(self):
        gl.glEnableClientState(gl.GL_NORMAL_ARRAY)
        self.projection.set_perspective(45)
        self.modelview.set_world()
        for item in self.world:
            if not item.glyph:
                continue
            glyph = item.glyph
            gl.glPushMatrix()
            if item.position:
                gl.glTranslatef(*item.position)
            # TODO: item orientation
            gl.glVertexPointer(
                Glyph.DIMENSIONS, gl.GL_FLOAT, 0, glyph.glvertices)
            gl.glColorPointer(
                Color.NUM_COMPONENTS, gl.GL_UNSIGNED_BYTE, 0, glyph.glcolors)
            gl.glNormalPointer(gl.GL_FLOAT, 0, glyph.glnormals)
            gl.glDrawElements(
                gl.GL_TRIANGLES,
                len(glyph.glindices),
                type_to_enum[glyph.glindex_type],
                glyph.glindices)
            gl.glPopMatrix()


    def draw_hud(self):
        self.projection.set_screen()
        self.modelview.set_identity()
        gl.glDisableClientState(gl.GL_NORMAL_ARRAY)
        self.clock_display.draw()

