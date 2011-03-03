from glob import glob
from os import listdir
from os.path import abspath, dirname, isfile, join
import sys
from setuptools import find_packages


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


def get_scripts(script):
    script = [script] if script else []
    examples = [
        join('examples', f)
        for f in listdir('examples')
        if f.endswith('.py')
    ]
    return script + examples


def get_sdist_config(name, version, script):
    description, long_description = read_description()

    config = dict(
        name=name,
        version=version,
        description=description,
        long_description=long_description,
        keywords='',
        packages=find_packages(),
        scripts=get_scripts(script),
        #data_files=[
            #('dest-dir', ['source-files']),
        #],
        classifiers=[
            'Development Status :: 1 - Planning',
            'Intended Audience :: Developers',
            'License :: OSI Approved :: BSD License',
            'Operating System :: Microsoft :: Windows',
            'Programming Language :: Python :: 2.7',
        ],    
        # see classifiers http://pypi.python.org/pypi?:action=list_classifiers
    )
    return config

