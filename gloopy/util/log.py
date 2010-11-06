'''
Other modules may use module-level variable to record logfile messages::

    from .util.log import log
    log.info('hello')

If modules import 'log' before 'init_log' is called, they will just get None.
Hence call init_log before anything else attempts to import this module.
'''
import logging
from os.path import basename, splitext
import sys

log = None

def init_log():
    global log
    app_name = splitext(basename(sys.argv[0]))[0]
    logging.basicConfig(
        filename='%s-debug.log' % (app_name,),
        filemode='w',
        level=logging.DEBUG,
    )
    log = logging.getLogger('gloopy')

