
Gloopy is a Python library for creating 3D polyhedra and rendering them using
OpenGL. It uses Pyglet to open a window and manage events, and PyOpenGL for
OpenGL bindings.

Gloopy provides the following services:

- Creation and manipulation of 3D, flat-surfaced, polyhedra, using the
  Shape class.
- Factory functions to produce particular shapes, such as Cube or Icosahedron.
- Some basic algorithms to modify existing shapes, such as by subdividing or
  extruding their surfaces.
- Conversion of shapes into Glyph instances, which
  manage vertex arrays stored in a VBO.
- A simple Render class which renders glyphs
  with given positions and orientations.
- A camera attribute on the single Gloopy instance,
  that can be positioned, oriented, or told to look at a particular item or
  position.


Dependencies
------------

Written mostly on Windows, tested occasionally on Ubuntu.

- Python 2.7
- Pyglet 1.1.4
- PyOpenGL 3.0.1


Documentation
-------------

In the Gloopy source, see gloopy/docs/html/index.html

and the scripts in the 'examples' directory.

Documentation is not currently available online.


License
-------

Gloopy is released under the New BSD License, the text of which is to be found
in the project's LICENSE.txt. Alternatively, you may use it under the terms of
any other OSI-approved license.


Status & Known Issues
---------------------

It works for me, but has not been used any real projects. The API is
a mess and may change substantially in later releases.

No issue tracker is currently maintained, but the major shortfalls as
I percieve them are:

- Some algorithmic modifiers, such as face subdivision, extrusion, stellation,
  do not currently work on MultiShapes. This is because these modifiers rely
  on modifying attributes of the given shape in place, such as by inserting
  new entries in the .faces collection. However, MultiShapes provide many of
  these attributes by using generators to form a composite stream of their
  children. I guess I ought to make all shape modifiers functional.
- The supplied 'directional lighting' shader is broken - rotating an object
  does not modify the apparent illumination of its surfaces.
- No attempt is made to handle textures. All faces are plain colors.
- We don't currently handle multiple shaders within a single scene.


Thanks
------

`PyWeek <http://pyweek.org>`_ participants 'Scav' and 'Threads' for showing me
how it should be done, and PyWeek message board users donal.h, Cosmologicon,
RB[0], PyTM30, Tee and saluk for cajoling me into accepting the merit of
allowing people to bring pre-existing codebases into PyWeek so long as they
are public.


