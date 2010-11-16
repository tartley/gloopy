from ctypes import (
    byref, c_char, c_char_p, c_int, cast, create_string_buffer, pointer,
    POINTER
)
from OpenGL import GL


class ShaderError(Exception): pass
class CompileError(ShaderError): pass
class LinkError(ShaderError): pass


shader_errors = {
    GL.GL_INVALID_VALUE: 'GL_INVALID_VALUE (bad 1st arg)',
    GL.GL_INVALID_OPERATION: 'GL_INVALID_OPERATION '
        '(bad id or immediate mode drawing in progress)',
    GL.GL_INVALID_ENUM: 'GL_INVALID_ENUM (bad 2nd arg)',
}


def load_source(fname):
    with open(fname) as fp:
        src = fp.read()
    return src


class _Shader(object):

    shader_type = None

    def __init__(self, files):
        if isinstance(files, basestring):
            self.files = [files]
        else:
            self.files = files
        self.sources = None
        self.id = None
        
        
    def _get(self, paramId):
        outvalue = c_int(0)
        GL.glGetShaderiv(self.id, paramId, byref(outvalue))
        value = outvalue.value
        if value in shader_errors.keys():
            msg = '%s from glGetShader(%s, %s, &value)'
            raise ValueError(msg % (shader_errors[value], self.id, paramId))
        return value


    def get_compile_status(self):
        return bool(self._get(GL.GL_COMPILE_STATUS))


    def get_info_log_length(self):
        return self._get(GL.GL_INFO_LOG_LENGTH)


    def get_info_log(self):
        length = self.get_info_log_length()
        if length == 0:
            return ''
        buffer = create_string_buffer(length)
        return GL.glGetShaderInfoLog(self.id)


    def _sources_to_array(self):
        num = len(self.sources)
        all_source = (c_char_p * num)(*self.sources)
        return num, cast(pointer(all_source), POINTER(POINTER(c_char)))
        

    def _load_sources(self):
        return [load_source(fname) for fname in self.files]


    def compile(self):
        self.id = GL.glCreateShader(self.shader_type)

        self.sources = self._load_sources()
        num, src = self._sources_to_array()
        GL.glShaderSource(self.id, '\n'.join(self.sources))
        
        GL.glCompileShader(self.id)

        if not self.get_compile_status():
            raise CompileError(self.get_info_log())



class VertexShader(_Shader):
    shader_type = GL.GL_VERTEX_SHADER


class FragmentShader(_Shader):
    shader_type = GL.GL_FRAGMENT_SHADER



class ShaderProgram(object):

    def __init__(self, *shaders):
        self.shaders = list(shaders)
        self.id = None

    
    def _get(self, paramId):
        outvalue = c_int(0)
        GL.glGetProgramiv(self.id, paramId, byref(outvalue))
        value = outvalue.value
        if value in shader_errors.keys():
            msg = '%s from glGetProgram(%s, %s, &value)'
            raise ValueError(msg % (shader_errors[value], self.id, paramId))
        return value
        
        
    def get_link_status(self):
        return bool(self._get(GL.GL_LINK_STATUS))


    def get_info_log_length(self):
        return self._get(GL.GL_INFO_LOG_LENGTH)


    def get_info_log(self):
        length = self.get_info_log_length()
        if length == 0:
            return ''
        buffer = create_string_buffer(length)
        return GL.glGetProgramInfoLog(self.id)
        

    def _get_message(self):
        messages = []
        for shader in self.shaders:
            log = shader.get_info_log()
            if log:
                messages.append(log)
        log = self.get_info_log()
        if log:
            messages.append(log)
        return '\n'.join(messages)

        
    def compile(self):
        self.id = GL.glCreateProgram()
        
        for shader in self.shaders:
            shader.compile()
            GL.glAttachShader(self.id, shader.id)

        GL.glLinkProgram(self.id)

        message = self._get_message()
        if not self.get_link_status():
            raise LinkError(message)
        return message


    def use(self):
        return GL.glUseProgram(self.id)

