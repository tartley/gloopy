Introduction
============

Gloopy is a Python library that creates and manipulates 3D polyhedra, and
renders them using OpenGL. It uses Pyglet to open a window and manage events,
and PyOpenGL for OpenGL bindings.

Gloopy provides the following services:

* Creation and manipulation of 3D, flat-surfaced, polyhedra, using the `Shape` class.
* Factory functions to produce particular shapes, such as `Cube` or `Isocosahedron`.
* Some basic algorithms to modify existing shapes, such as by subdividing or extruding their surfaces.
* Conversion of shapes into `Glyphs`, OpenGL vertex arrays stored in VBOs.
* A simple `Renderer` renders an iterable of glyphs, each with its own position and orientation.
* A `Camera` class that can be positioned, oriented, or told to look at a particular item or position.


Dependencies
------------

Written mostly on Windows, tested occasionally on Ubuntu.

* Python 2.7
* Pyglet 1.1.4
* PyOpenGL 3.0.1


Documentation
-------------

In the Gloopy source, see docs/html/index.html

and the scripts in the 'examples' directory.

Documentation is not currently available online.


Status & Known Issues
---------------------

It works for me, but has not been used any substantial projects. The API is
a mess and may change substantially in later releases.

No issue tracker is currently maintained, but the major shortfalls as
I percieve them are:

* The supplied 'directional lighting' shader is broken - rotating an object does not modify the apparent illumination of its surfaces.
* It doesn't handle texture mapped surfaces
* It doesn't handle the use of multiple shaders within a single scene


Thanks
------

`PyWeek <http://pyweek.org>`_ participants 'Scav' and 'Threads' for showing me
how it should be done, and PyWeek message board users donal.h, Cosmologicon,
RB[0], PyTM30, Tee and saluk for cajoling me into accepting the merit of
allowing people to bring pre-existing codebases into PyWeek.

