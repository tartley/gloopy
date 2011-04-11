import logging

from ..version import NAME


def init_log():
    '''
    Initialise stdlib logging.
    '''
    # TODO, should create log file in application's scratch space, not in cwd
    logging.basicConfig(
        filename='%s-debug.log' % (NAME,),
        filemode='w',
        level=logging.DEBUG,
    )

