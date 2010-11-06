'''
Creates a log file. After init_log() has been called, other modules should send
log messages using::

    import logger
    log = logger.getLogger(__name__)
    log.info('message')

See http://docs.python.org/library/logging.html
'''
import logging
from os.path import basename, splitext
import sys

def init_log():
    # TODO, should create log file in application's scratch space, not in cwd
    app_name = splitext(basename(sys.argv[0]))[0]
    logging.basicConfig(
        filename='%s-debug.log' % (app_name,),
        filemode='w',
        level=logging.DEBUG,
    )

