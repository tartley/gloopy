from __future__ import division

from OpenGL import GL as gl, GLU as glu
from pyglet.event import EVENT_HANDLED


class Projection(object):
    '''
    Manage projection matrix.
    
    Presumably this class will go away, or be severely modified, in some future
    release of Gloopy which may use a more OpenGL3 style.
    '''
    def __init__(self, window):
        window.on_resize = self.resize_window
        self.width = window.width
        self.height = window.height


    def resize_window(self, width, height):
        '''
        Handler for window resize events
        TODO: do we also need to set clipping?
        '''
        self.width = width
        self.height = height
        gl.glViewport(0, 0, width, height)
        return EVENT_HANDLED


    def set_perspective(self, fovy):
        '''
        Set OpenGL projection matrix to a 3D perspective projection, with the
        given field of view, in degrees.
        '''
        aspect = self.width / self.height
        zNear = 0.1
        zFar = 3000.0
        gl.glMatrixMode(gl.GL_PROJECTION)
        gl.glLoadIdentity()
        glu.gluPerspective(fovy, aspect, zNear, zFar);


    def set_ortho(self, scale):
        '''
        Set OpenGL projection matrix to Ortho2D, such that the screen's
        shortest dimension (height on a landscape monitor or window) will show
        exactly `scale` of the world from the center of the screen to each
        edge, regardless of screen resolution or window size.
        '''
        def ortho_bounds(self, scale, aspect):
            left = bottom = -scale
            right = top = scale
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
        glu.gluOrtho2D(*ortho_bounds(scale, aspect))


    def set_screen(self):
        '''
        Set OpenGL projection matrix to Ortho2D, showing world space coords
        0 <= x < WIDTH, and 0 <= y < HEIGHT.
        '''
        gl.glMatrixMode(gl.GL_PROJECTION)
        gl.glLoadIdentity()
        glu.gluOrtho2D(0, self.width - 1, 0, self.height - 1)

