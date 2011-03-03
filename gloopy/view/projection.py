from __future__ import division

from OpenGL import GL as gl, GLU as glu
from pyglet.event import EVENT_HANDLED


class Projection(object):

    def __init__(self, window):
        window.on_resize = self.resize_window
        self.width = window.width
        self.height = window.height


    def resize_window(self, width, height):
        '''
        Handler for window resize events
        '''
        self.width = width
        self.height = height
        gl.glViewport(0, 0, width, height)
        return EVENT_HANDLED


    def set_ortho(self, zoom):
        '''
        Screen's shortest dimension (usually height) will show exactly
        self.zoom of the world from the center of the screen to each edge,
        regardless of screen resolution, window size.
        '''

        def ortho_bounds(self, zoom, aspect):
            left = bottom = -zoom
            right = top = zoom
            if self.width > self.height:
                # landscape mode window
                bottom /= aspect
                top /= aspect
            elif self.width < self.height:
                # portrait mode window
                left *= aspect
                right *= aspect
            return left, right, bottom, top

        aspect = self.width / self.height
        gl.glMatrixMode(gl.GL_PROJECTION)
        gl.glLoadIdentity()
        glu.gluOrtho2D(*ortho_bounds(zoom, aspect))


    def set_perspective(self, fovy):
        '''
        Set perspective projection
        '''
        aspect = self.width / self.height
        zNear = 0.1
        zFar = 3000.0
        gl.glMatrixMode(gl.GL_PROJECTION)
        gl.glLoadIdentity()
        glu.gluPerspective(fovy, aspect, zNear, zFar);


    def set_screen(self):
        '''
        Set ortho projection, showing world space coords 0 <= x < WIDTH,
        and 0 <= y < HEIGHT.
        '''
        gl.glMatrixMode(gl.GL_PROJECTION)
        gl.glLoadIdentity()
        glu.gluOrtho2D(0, self.width - 1, 0, self.height - 1)

