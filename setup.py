
NAME = 'TODO'
SCRIPT = 'demo.py'


def main():
    from setup_utils import distribute_setup, get_config
    distribute_setup.use_setuptools()

    from setuptools import setup
    import py2exe

    version = __import__(NAME).__version__
    config = get_config(NAME, version, SCRIPT, console=True)
    config.update(dict(
        author='TODO',
        author_email='TODO',
        url='TODO',
        license='TODO',
    ) )

    setup(**config)


if __name__ == '__main__':
    main()

