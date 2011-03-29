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


def get_data_files(dest, source):
    retval = []
    for dirname, subdirs, files in os.walk(source):
        retval.append(
            (join(dest, dirname[len(source)+1:]), glob(join(dirname, '*.*')))
        )
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
        data_files=get_data_files('share/doc/gloopy', 'docs/html'),
        package_data={
            NAME:
                get_package_data('data') +
                ['examples/*.py']
        },
        # see classifiers http://pypi.python.org/pypi?:action=list_classifiers
        classifiers=[
            'Development Status :: 3 - Alpha',
            'Intended Audience :: Developers',
            'License :: OSI Approved :: BSD License',
            'Operating System :: Microsoft :: Windows',
            'Programming Language :: Python :: 2.7',
        ],    
    )

    if '--verbose' in sys.argv:
        pprint(config)
    if '--dry-run' in sys.argv:
        return

    setup(**config)


if __name__ == '__main__':
    main()

