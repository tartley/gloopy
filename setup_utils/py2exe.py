
from os import walk
from os.path import join, normpath



IGNORE_DIRS = ['.svn']
IGNORE_EXTENSIONS = ['.pyc', '.pyo']


def all_files(directory, source=None):
    retval = []
    if source is None:
        source = directory
    for (root, dirs, files) in walk(normpath(source)):
        dirs = filter(lambda d: d not in IGNORE_DIRS, dirs)
        files = filter(
            lambda f: not any(f.endswith(ext) for ext in IGNORE_EXTENSIONS),
            files)
        if files:
            retval.append(
                (directory, [join(root, filename) for filename in files])
            )
    return retval



def get_py2exe_config(name, version, script, console):
    return {
        'console' if console else 'windows': [
            dict(
                script=script,
                # icon_resources=[(1, 'data\%s.ico' % (name,))],
            )
        ],
        'data_files':
            all_files('Microsoft.VC90.CRT', '..\lib\Microsoft.VC90.CRT') + 
            all_files('data'),
        'options':dict(
            py2exe=dict(
                ascii=True, # breaks unicode
                bundle_files=1, # breaks C extensions loaded at runtime
                dist_dir='dist/%s-%s-windows' % (name, version),
                dll_excludes=[
                    # Can we exclude these? Dunno
                    # "pywintypes26.dll",
                    # "pywintypes27.dll",
                ],
                optimize=2,
                excludes=[
                    # silence warnings of missing modules
                    '_imaging_gif',
                    '_scproxy',
                    'clr',
                    'dummy.Process',
                    'email',
                    'email.base64mime',
                    'email.utils',
                    'email.Utils',
                    'ICCProfile',
                    'Image',
                    'IronPythonConsole',
                    'modes.editingmodes',
                    'startup',
                    'System',
                    'System.Windows.Forms.Clipboard',

                    # filter unused .pyd files
                    '_hashlib',
                    '_imaging',
                    '_multiprocessing',
                    '_ssl',
                    '_socket',
                    'bz2',
                    'pyexpat',
                    'pyreadline',
                    'select',
                    'win32api',
                    'win32pipe',

                    # filter unused .pyo files in library.zip
                    'calendar',
                    'cookielib',
                    'difflib',
                    'doctest',
                    'locale',
                    'optparse',
                    'pdb',
                    'pickle',
                    'pyglet.window.xlib',
                    'pyglet.window.carbon',
                    'pyglet.window.carbon.constants',
                    'pyglet.window.carbon.types',
                    'subprocess',
                    'tarfile',
                    'threading',
                    'unittest',
                    'urllib',
                    'urllib2',
                    'win32con',
                    'zipfile',
                ],
            ),
        ),
        'zipfile': None,
    }

