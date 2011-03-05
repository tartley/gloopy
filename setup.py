import os
from os.path import isfile, join
from pprint import pprint
import sys


NAME = 'gloopy'
VERSION= __import__(NAME).VERSION
RELEASE = __import__(NAME).RELEASE
SCRIPT = None
CONSOLE = False


def first_existing(*possibles):
    '''
    Given a list of filenames, return the first one that actually exists
    '''
    for fname in possibles:
        if isfile(fname):
            return fname
    sys.exit("Can't find any of " + ', '.join(possibles))


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
    # these imports inside main() because we want to be able to import this
    # module cheaply to get at the name
    
    # use_setuptools must be called before the setuptools import
    from distribute_setup import use_setuptools
    use_setuptools()
    from setuptools import find_packages, setup

    description, long_description = read_description(
        first_existing('README', 'README.txt', 'README.rst')
    )

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
        packages=find_packages(),
        package_data={
            NAME: 
                get_package_data('data') +
                get_package_data('docs/html', excluded={'.doctrees'}) +
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

