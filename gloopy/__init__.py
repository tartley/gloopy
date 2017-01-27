'''
Gloopy's top level package.
'''
import logging
import sys

from .version import RELEASE, VERSION

logging.basicConfig(stream=sys.stderr, level=logging.INFO)

