
# make sure we can find gloopy in '..', so that we can run from within
# 'examples' dir, even if Gloopy isn't installed.
import sys
from os.path import abspath, dirname, join
sys.path.insert(0, abspath(join(dirname(__file__), '..', '..')))

