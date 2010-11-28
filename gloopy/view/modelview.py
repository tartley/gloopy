from __future__ import division

from OpenGL import GL as gl, GLU as glu

from ..model.item.gameitem import position_or_gameitem


class ModelView(object):
    '''
    Manage modelview matrix
    '''
    def __init__(self, camera):
        self.camera = camera

    def set_identity(self):
        gl.glMatrixMode(gl.GL_MODELVIEW)
        gl.glLoadIdentity()

    def set_world(self):
        gl.glMatrixMode(gl.GL_MODELVIEW)
        gl.glLoadIdentity()
        position = self.camera.position
        look_at = position_or_gameitem(self.camera.look_at)
        glu.gluLookAt(
            position.x, position.y, position.z,
            look_at.x, look_at.y, look_at.z,
            0, 1, 0)

