from glob import glob
import os
from os.path import join
from pprint import pprint
import sys


NAME = 'gloopy'
module = __import__(NAME)
VERSION= module.VERSION
RELEASE = module.RELEASE
SCRIPT = None
CONSOLE = False


def read_description(filename):
    '''
    Read given textfile and return (first_para, rest_of_document)
    '''
    with open(filename) as fp:
        text = fp.read()

    paras = text.split('\n\n')
    return paras[0], '\n\n'.join(paras[1:])


def get_package_data(topdir, excluded=set()):
    retval = []
    for dirname, subdirs, files in os.walk(join(NAME, topdir)):
        for x in excluded:
            if x in subdirs:
                subdirs.remove(x)
        retval.append(join(dirname[len(NAME)+1:], '*.*'))
    return retval


def main():
    # these imports inside main() so that we can import this file cheaply
    # to get at its module-level constants like NAME
    
    # use_setuptools must be called before the setuptools import
    from distribute_setup import use_setuptools
    use_setuptools()
    from setuptools import find_packages, setup

    description, long_description = read_description('README.txt')

    config = dict(
        name=NAME,
        version=RELEASE,
        description=description,
        long_description=long_description,
        url='http://bitbucket.org/tartley/gloopy',
        license='New BSD',
        author='Jonathan Hartley',
        author_email='tartley@tartley.com',
        keywords='opengl 3d graphics games',
        packages=find_packages(exclude=('*.tests',)),
        data_files=[
            ('share/doc/gloopy', glob('docs/html/*.*')),
            ('share/doc/gloopy/_images', glob('docs/html/_images/*.*')),
            ('share/doc/gloopy/_modules', glob('docs/html/_modules/*.*')),
            ('share/doc/gloopy/_modules/gloopy', glob('docs/html/_modules/gloopy/*.*')),
            ('share/doc/gloopy/_modules/gloopy/geom', glob('docs/html/_modules/gloopy/geom/*.*')),
            ('share/doc/gloopy/_modules/gloopy/move', glob('docs/html/_modules/gloopy/move/*.*')),
            ('share/doc/gloopy/_modules/gloopy/shapes', glob('docs/html/_modules/gloopy/shapes/*.*')),
            ('share/doc/gloopy/_modules/gloopy/util', glob('docs/html/_modules/gloopy/util/*.*')),
            ('share/doc/gloopy/_modules/gloopy/view', glob('docs/html/_modules/gloopy/view/*.*')),
            ('share/doc/gloopy/_sources', glob('docs/html/_sources/*.*')),
            ('share/doc/gloopy/_sources/api', glob('docs/html/_sources/api/*.*')),
            ('share/doc/gloopy/_static', glob('docs/html/_static/*.*')),
            ('share/doc/gloopy/api', glob('docs/html/api/*.*')),
        ],
        package_data={
            NAME:
                get_package_data('data') +
                ['examples/*.py']
        },
        classifiers=[
            'Development Status :: 3 - Alpha',
            'Intended Audience :: Developers',
            'License :: OSI Approved :: BSD License',
            'Operating System :: Microsoft :: Windows',
            'Programming Language :: Python :: 2.7',
        ],    
        # see classifiers http://pypi.python.org/pypi?:action=list_classifiers
    )

    if '--verbose' in sys.argv:
        pprint(config)
    if '--dry-run' in sys.argv:
        return

    setup(**config)


if __name__ == '__main__':
    main()

