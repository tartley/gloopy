Gloopy is a simple framwork for OpenGL applications in Python, using Pyglet for
windowing, and PyOpenGL for bindings & utils.

Provides a very simple render loop, and classes to aid in the creation of
flat-surfaced polyhedra. Each shape may have a position and orientation, and a
render loop iterates through all items, rendering them all as VBOs of vertex
arrays, from the point of view of a camera, which may also be positioned and
oriented.

http://bitbucket.org/tartley/gloopy

Written mostly on Windows, tested occasionally on Ubuntu.

Status
------

It works for me, but has not been used any substantial projects. The API is
a mess and may change substantially in later releases.


Dependencies
------------

  * Python 2.7
  * Pyglet 1.1.4
  * PyOpenGL 3.0.1


Documentation
-------------

See docs/html/index.html

and the scripts in the 'examples' directory.


Known Issues
------------

No tracker is currently maintained.


Thanks
------

PyWeek participants 'Scav' and 'Threads' for showing me how it should be done,
and PyWeek message board users donal.h, Cosmologicon, RB[0], PyTM30, Tee and
saluk for cajoling me into accepting the merit of allowing people to bring
pre-existing codebases into PyWeek.

