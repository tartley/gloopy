
import logging
from os.path import isfile

from pyglet import image


log = logging.getLogger(__name__)

image_no = 0


def get_filename():
    return 'screenshot%02d.png' % (image_no,)


def screenshot():
    global image_no

    while isfile(get_filename()):
        image_no += 1

    log.info('screenshot: %s' % (get_filename(),))
    image.get_buffer_manager().get_color_buffer().save(get_filename())

    image_no += 1
    return get_filename()

