
use_pyglet_bindings = True
if use_pyglet_bindings:
    from pyglet.gl import gl
    from pyglet.gl import glu
else:
    import OpenGL
    OpenGL.ERROR_CHECKING = __debug__
    OpenGL.ERROR_ON_COPY = __debug__

    LOGGING = False
    OpenGL.ERROR_LOGGING = LOGGING
    OpenGL.FULL_LOGGING = LOGGING
    
    from OpenGL import GL as gl
    from OpenGL import GLU as glu

