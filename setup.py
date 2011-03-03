
NAME = 'gloopy'
VERSION= __import__(NAME).VERSION
RELEASE = __import__(NAME).RELEASE
SCRIPT = None
CONSOLE = False

def main():
    import sys
    from pprint import pprint

    from setup_utils import distribute_setup
    from setup_utils.sdist_setup import get_sdist_config
    distribute_setup.use_setuptools()
    from setuptools import setup

    config = get_sdist_config(NAME, RELEASE, SCRIPT)

    if 'py2exe' in sys.argv:
        import py2exe
        from setup_utils.py2exe_setup import get_py2exe_config
        config.update(
            get_py2exe_config(NAME, RELEASE, SCRIPT, CONSOLE)
        )

    config.update(dict(
        author='Jonathan Hartley',
        author_email='tartley@tartley.com',
        url='http://bitbucket.org/tartley/gloopy',
        license='New BSD',
    ) )

    if '--verbose' in sys.argv:
        pprint(config)

    setup(**config)


if __name__ == '__main__':
    main()

