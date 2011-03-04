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
    return paras[0], '\n\n'.join(paras[1:])


def get_sdist_config(name, version, script):
    description, long_description = read_description()
    config = dict(
        name=name,
        version=version,
        description=description,
        long_description=long_description,
        keywords='',
        packages=find_packages(),
        package_data={
            'gloopy': [
                'docs/html/*.*',
                'docs/html/_images/*.*',
                'docs/html/_modules/*.*',
                'docs/html/_modules/gloopy/*.*',
                'docs/html/_modules/gloopy/geom/*.*',
                'docs/html/_modules/gloopy/move/*.*',
                'docs/html/_modules/gloopy/shapes/*.*',
                'docs/html/_modules/gloopy/util/*.*',
                'docs/html/_modules/gloopy/view/*.*',
                'docs/html/_static/*.*',
                'docs/html/api/*.*',
                'data/shaders/*.*',
                'examples/*.py',
            ],
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
    return config

