A simple template for new Python projects.

http://code.google.com/p/python-project-template/

This is intended to provide a lightweight template for new Python projects that
encapsulates as much of the boilerplate project infrastructure as possible,
with applicability for pyglet game and OpenGL graphics projects borne in mind.

Features:
  * For libraries, setup.py creates sdist, and registers and uploads source
    to The Cheese Shop.
  * For applications, setup.py creates py2exe stand-alone Windows binaries.
  * Makefile contains useful commands such as 'clean', 'tags', 'profile',
    'sdist' and 'py2exe' and 'stats' (count lines of code.)


Dependencies
------------

  * Microsoft Windows
  * Python 2.7
  * Setuptools 0.6c11
  * Distribute 0.6.14

Optional:

  * Cygwin binaries foremost on the PATH.

The exact version numbers of the dependencies are probably not important, but
this is what I'm using.

Cywin binaries are used by some entries in the Makefile, although you don't
need to be running from a Cygwin bash prompt to use them - they also work fine
from a Windows Cmd shell. Some other optional installable tools are referenced
in the Makefile, and are explained there.

Currently only Windows is supported, I hope to confirm Linux support and then
creation of Linux binaries soon. I have no idea how to produce Mac binaries, so
if anyone wants to help out on that, or any other fixes or ideas, that would be
marvellous.


Usage
-----

0) Install the dependencies listed above.

1) Start new Python projects by cloning this repo::

    hg clone https://python-project-template.googlecode.com/hg/ newproject

2) Then remove .hg so as to not interfere with the version control of the
'newproject' subsequently built on top of this::

    rm -rf newproject/.hg

3) Grep for occurrences of TODO to customise the files for your new project.
This includes renaming the 'TODO' folder, which is intended to be the root
folder for newproject's source code.

The idea is that you will need to modify the short and simple 'setup.py', and
add your project's name to the Makefile, but you should not need to modify the
more fiddly files found in directory 'setup'.

4) Finally, replace this README with newproject's (you might want to keep the
section headings.) Bear in mind that when uploading an sdist to The Cheese
Shop, the first line of the README is used as your project's description, and
the rest of the README is the long_description. The Cheese Shop expects these
to be in RestructuredText format, like this README is.

5) You're good to go, get coding!


Known Issues
------------

Python-project-template has not yet been used to create any other real
projects. Hopefully this will be rectified imminently, and no doubt fixes will
result.

See the project issues at:
http://code.google.com/p/python-project-template/issues/list?sort=priority


Thanks
------

The modest contents of this directory owe much to Tarek Ziadé's excellent book
'Expert Python Programming', which improved the way I work with Python every
day.

