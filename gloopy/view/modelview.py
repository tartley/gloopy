from __future__ import division

from OpenGL import GL as gl, GLU as glu

from ..gameitem import position_or_gameitem


class ModelView(object):
    '''
    Manage modelview matrix.
    
    Presumably this class will go away in future
    releases of Gloopy as we use a more OpenGL3 style.

    .. function:: __init__(camera)

        `camera` must have `.position` and `.look_at` attributes.
        A GameItem instance would make a good camera.
    '''
    def __init__(self, camera):
        self.camera = camera

    def set_identity(self):
        gl.glMatrixMode(gl.GL_MODELVIEW)
        gl.glLoadIdentity()

    def set_world(self):
        '''
        Set the OpenGL modelview matrix to account for the camera's position
        and orientation.
        '''
        gl.glMatrixMode(gl.GL_MODELVIEW)
        gl.glLoadIdentity()
        position = self.camera.position
        look_at = position_or_gameitem(self.camera.look_at)
        glu.gluLookAt(
            position.x, position.y, position.z,
            look_at.x, look_at.y, look_at.z,
            0, 1, 0)

