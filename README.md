Gloopy is an experimental Python demo of creating 3D polyhedra and
rendering them using OpenGL.

It uses Pyglet for windowing and events, PyOpenGL for most OpenGL bindings,
but pyglet.gl for performance critical OpenGL calls.

These two blog posts discuss it in depth, including screenshots of the output:
[week1](https://www.tartley.com/posts/flying-high-hobbyist-opengl-from-python/), 
[week2](https://www.tartley.com/posts/flying-high-opengl-from-python-part-2/).

# Keys

    1 2 3 4 5 6     Basic shapes
    Q W E R T Y U   Compound shapes

    Z X C           Hi count compound spheres
    V               Invaders

    up / down       Zoom in/out (or pageup / pagedown)

    backspace       Delete selected (last added) shape
    Ctrl M          Move selected shape away from origin

    Space           Toggle highlight of selected shape / faces
    - +             Select subset of faces
    0               Select all faces
    del             Select no faces (huh?)

    Ctrl Q W E R    Extrude
    Ctrl U I O P    Stellate
    Ctrl N          Normalize
    Ctrl S          Subdivide (good with '5')


# Dependencies

- Originally written on Windows, run occasionally on OSX, and all recent
development on Ubuntu.

- Python 3.6

This project does not use pip. Instead we track our dependencies using
the newer '[Pipenv](https://docs.pipenv.org/)', built
on top of pip. So instead of `pip install ...`, it should just be a `pipenv
install`, but:

- Our Python dependencies (PyOpenGL, etc) aren't available as pre-compiled
  wheels, so installing them requires you are able to compile and link:

      # On Ubuntu
      sudo apt-get update
      sudo apt-get install build-essential

  and requires Python C headers & shared libraries:

      # On Ubuntu, if your Python3 was installed using 'apt', then:
      sudo apt install python3.6-dev

- Then you can install Python dependencies, as specified in 'Pipfile':

      pip install --user pipenv
      pipenv install

# Running

Execute `run.py` from within the gloopy virtualenv, eg:

    pipenv run ./run.py

You should be presented with an orange fullscreen window.

If you have multiple monitors, Gloopy prints them to stdout, and chooses
the first one it discovers. To change the monitor it chooses, modify the source
code in run.py, create_window(), modifying the integer index into the
'screens' list. It would be nice to add a key to change from one screen
to another at runtime.

Pressing keys makes things happen:

## Basic Shapes

Keys          | Description
--------------|------------------------------------
`1` to `7`    | Create Platonic solids and some variations on them.

## Utilities

Keys          | Description
--------------|------------------------------------
`backspace`   | Remove the most recently created shape.
`ctrl-m`      | Move the most recently created shape (to make room for new ones.)
`up` / `down` | Move camera nearer / further away.
`esc`         | Exit.

## Compound Shapes

Keys          | Description
--------------|------------------------------------
`q` to `u`    | Create some compound shapes, each formed from a collection of Platonic solids rendered using a single OpenGL draw call. Try `u` a bunch of times to generate a series of rings.
`z` to `c`    | Massive compound shapes (zoom out to see them.)
`v`           | Space invader, generated dynamically from a loaded bitmap.
`b`           | Fractaline tetrahedron (at a scale comparable to the Platonic solids, zoom in to see it.) (see 'generating geometry' below.)

## Modifying Shapes

Modification affects the most recently created shape, ie. the one that
has flashing highlights when `space` is pressed.

Due to some silly decisions of mine, modifying only works on basic shapes
at the moment, not on compounds.

Where `^x` means press 'x' while holding 'ctrl'.

Keys          | Description
--------------|------------------------------------
`^n`          | Normalise vertices, ie. move all vertices onto a unit sphere.
space         | Toggle flashing highlight of the selected object.
`-` / `=`     | Select a subset of faces on the selected object. This limits the following operations to just the highlighted faces.
`^c`          | Recolor faces
`^q` to `^r`  | Extrude faces by various amounts.
`^s`          | Subdivide faces into smaller polygons.
`^u` / `^i`   | Stellate faces inwards
`^o` / `^p`   | Stellate faces outwards

Hence, for example:

### A unit sphere with even vertex distribution

* `5` to create a polygon
* `^s` a few times to subdivide all the faces
* `^n` to normalize the vertices to the unit sphere.

The vertices are distributed fairly evenly, compared to, points of lat/long,
for example, which cluster around the poles. This means, for example, that
textures or per-vertex lighting calculations are distributed evenly over the
surface.

### A fractal tree-like structure

* Any number 1-5 to create a polygon
* `^r` to extrude the faces by a large amount
* `space` to highlight the whole shape
* `=` twice, to highlight just the tips of the branches
* `^p` to stellate the tips into pyramids
* `^e` to extrude the pyramid faces by a medium amount
* `=` again to select just the new branch tips.

And so on, with various lengths of extrusion.


# About the Rendering

Gloopy provides the following services:

- Creation and manipulation of 3D, flat-surfaced, polyhedra, using the Shape
  class.
- Factory functions to produce particular shapes, such as Cube or Icosahedron.
- Some basic algorithms to modify existing shapes, such as by subdividing or
  extruding their surfaces.
- Conversion of shapes into Glyph instances, which manage vertex arrays stored
  in a VBO.
- A simple Render class which renders glyphs with given positions and
  orientations.
- A camera attribute on the single Gloopy instance, that can be positioned,
  oriented, or told to look at a particular item or position.
- A fragment and vertex shader are installed to perform basic
  lighting calculations.

# License

Gloopy is released under the terms of the New BSD, as specified in LICENSE.txt.

# Status & Known Issues

It works for me, but has not been used on any real projects. The API is
a mess, as is much of the code, and may change substantially in later releases.

No issue tracker is currently maintained, but the major shortfalls as
I percieve them are:

- Some algorithmic modifiers, such as face subdivision, extrusion, stellation,
  do not currently work on MultiShapes. This is because these modifiers rely
  on modifying attributes of the given shape in place, such as by inserting
  new entries in the .faces collection. However, MultiShapes provide many of
  these attributes by using generators to form a composite stream of their
  children. I guess I ought to make all shape modifiers functional.
- No attempt is made to handle textures. All faces are plain colors.
- We don't currently handle multiple shaders within a single scene.

# Thanks

`PyWeek <http://pyweek.org>`_ participants 'Scav' and 'Threads' for showing me
how it should be done, and PyWeek message board users donal.h, Cosmologicon,
RB[0], PyTM30, Tee and saluk for cajoling me into accepting the merit of
allowing people to bring pre-existing codebases into PyWeek so long as they
are public.

