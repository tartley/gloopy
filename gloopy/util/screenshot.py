from os.path import isfile

from pyglet import image


image_no = 0


def _get_next():
    global image_no
    while isfile(_get_filename(image_no)):
        image_no += 1
    return image_no


def _get_filename(number):
    return 'screenshot%02d.png' % (image_no,)


def screenshot():
    '''
    save a screenshot to the current directory, named 'screenshotXX.png',
    where XX is successive integers.
    '''
    number = _get_next()
    image.get_buffer_manager().get_color_buffer().save(_get_filename(number))
    return _get_filename(number)

