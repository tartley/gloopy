
# Add '..' to the path, to allow example scripts to import gloopy from the
# parent directory, so they can be run from the 'examples' dir, even when
# gloopy isn't installed.

import sys
from os.path import abspath, dirname, join
sys.path.insert(0, abspath(join(dirname(__file__), '..')))

