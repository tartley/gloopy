import logging

log = logging.getLogger(__name__)

class Options(object):

    def __init__(self, argv):
        self.vsync = '--vsync' in argv
        self.fullscreen = '--window' not in argv and '-w' not in argv
        self.display_fps = '--fps' in argv
        log.info(self)

    def __str__(self):
        return 'Options:\n' + '\n'.join(
            '    %s = %s' % (attr, value)
            for attr, value in self.__dict__.items()
        )

