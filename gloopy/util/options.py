
class Options(object):

    def __init__(self, argv):
        self.vsync = '--vsync' in argv
        self.fullscreen = '--window' not in argv and '-w' not in argv
        self.print_fps = '--print-fps' in argv
        self.display_fps = '--fps' in argv

