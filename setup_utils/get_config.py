from os.path import abspath, dirname, isfile, join
from pprint import pprint
import sys

from .py2exe import get_py2exe_config


def read_description():
    here = abspath(join(dirname(__file__), '..'))

    def first_existing(*possibles):
        for possible in possibles:
            filename = join(here, possible)
            if isfile(filename):
                return filename
        sys.exit("Can't find any of " + ', '.join(possibles))

    filename = first_existing('README', 'README.txt', 'README.rst')

    with open(filename) as fp:
        text = fp.read()

    # return (first_para, rest_of_document)
    paras = text.split('\n\n')
    return paras[0], '\n'.join(paras[1:])


def get_sdist_config(name, version, script):
    description, long_description = read_description()
    return dict(
        name=name,
        version=version,
        description=description,
        long_description=long_description,
        keywords='',
        packages=[name],
        scripts=[script],
        #data_files=[('package', ['files'])],
        classifiers=[
            'Development Status :: 1 - Planning',
            'Intended Audience :: Developers',
            'License :: OSI Approved :: BSD License',
            'Operating System :: Microsoft :: Windows',
            'Programming Language :: Python :: 2.7',
        ],    
        # see classifiers http://pypi.python.org/pypi?:action=list_classifiers
    )


def get_config(name, version, script, console=False):
    config = get_sdist_config(name, version, script)
    config.update( get_py2exe_config(name, version, script, console) )
    
    if '--verbose' in sys.argv:
        pprint(config)

    return config

