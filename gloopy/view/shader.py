from ctypes import (
    byref, c_char, c_char_p, c_int, cast, create_string_buffer, pointer,
    POINTER
)
from pyglet import gl


class ShaderError(Exception): pass
class CompileError(ShaderError): pass
class LinkError(ShaderError): pass


shader_errors = {
    gl.GL_INVALID_VALUE: 'GL_INVALID_VALUE (bad 1st arg)',
    gl.GL_INVALID_OPERATION: 'GL_INVALID_OPERATION '
        '(bad id or immediate mode drawing in progress)',
    gl.GL_INVALID_ENUM: 'GL_INVALID_ENUM (bad 2nd arg)',
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
        gl.glGetShaderiv(self.id, paramId, byref(outvalue))
        value = outvalue.value
        if value in shader_errors.keys():
            msg = '%s from glGetShader(%s, %s, &value)'
            raise ValueError(msg % (shader_errors[value], self.id, paramId))
        return value


    def get_compile_status(self):
        return bool(self._get(gl.GL_COMPILE_STATUS))


    def get_info_log_length(self):
        return self._get(gl.GL_INFO_LOG_LENGTH)


    def get_info_log(self):
        length = self.get_info_log_length()
        if length == 0:
            return ''
        buffer = create_string_buffer(length)
        gl.glGetShaderInfoLog(self.id, length, None, buffer)
        return buffer.value


    def _sources_to_array(self):
        num = len(self.sources)
        all_source = (c_char_p * num)(*self.sources)
        return num, cast(pointer(all_source), POINTER(POINTER(c_char)))
        

    def _load_sources(self):
        return [load_source(fname) for fname in self.files]


    def compile(self):
        self.id = gl.glCreateShader(self.shader_type)

        self.sources = self._load_sources()
        num, src = self._sources_to_array()
        gl.glShaderSource(self.id, num, src, None)
        
        gl.glCompileShader(self.id)

        if not self.get_compile_status():
            raise CompileError(self.get_info_log())



class VertexShader(_Shader):
    shader_type = gl.GL_VERTEX_SHADER


class FragmentShader(_Shader):
    shader_type = gl.GL_FRAGMENT_SHADER



class ShaderProgram(object):

    def __init__(self, *shaders):
        self.shaders = list(shaders)
        self.id = None

    
    def _get(self, paramId):
        outvalue = c_int(0)
        gl.glGetProgramiv(self.id, paramId, byref(outvalue))
        value = outvalue.value
        if value in shader_errors.keys():
            msg = '%s from glGetProgram(%s, %s, &value)'
            raise ValueError(msg % (shader_errors[value], self.id, paramId))
        return value
        
        
    def get_link_status(self):
        return bool(self._get(gl.GL_LINK_STATUS))


    def get_info_log_length(self):
        return self._get(gl.GL_INFO_LOG_LENGTH)


    def get_info_log(self):
        length = self.get_info_log_length()
        if length == 0:
            return ''
        buffer = create_string_buffer(length)
        gl.glGetProgramInfoLog(self.id, length, None, buffer)
        return buffer.value
        

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
        self.id = gl.glCreateProgram()
        
        for shader in self.shaders:
            shader.compile()
            gl.glAttachShader(self.id, shader.id)

        gl.glLinkProgram(self.id)

        message = self._get_message()
        if not self.get_link_status():
            raise LinkError(message)
        return message


    def use(self):
        return gl.glUseProgram(self.id)

