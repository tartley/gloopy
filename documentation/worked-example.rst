Worked Example
==============

The best way to illustrate how to use Gloopy and what it is capable of, is
with a worked example.

A Simple Cube
-------------

We can write a short script to display a Cube. First we must initialise
Gloopy::

    from gloopy import Gloopy

    gloopy = Gloopy()
    gloopy.init()

Next, we create a GameItem.::

    from gloopy.color import Color
    from gloopy.model.item.gameitem import GameItem
    from gloopy.shapes.cube import Cube

    item = GameItem( shape=Cube(1, Color.Green) )

A GameItem represents a single item to be rendered. It is just a dumb
collection of attributes, such as a `shape`, which determines what it looks
like. We can set these attributes using kwargs to the constructor, as shown
above, where we set this one to be a green cube of size 1.

Cube is a factory function that returns a new instance of the Shape class.
There are other factory functions to make other shapes, found in the
:mod:`~gloopy.shapes` module, or, after looking at those examples and
examining the Shape class, you will be able to write your own.

In order to see our cube rendered to the screen, we need to add it to the
world::

    gloopy.world.add(item)

``gloopy.world`` is an instance of :class:`~gloopy.model.world.World`, which is
just a dumb collection of GameItems.

In order to give ourselves a dramatic view of the cube, let's position the
camera::

    from gloopy.geom.vector import Vector
    gloopy.camera.position = Vector(1, 2, 3)

Having completed all our setup, we call ``gloopy.run()``::

    gloopy.run()

This makes the pyglet window visible, schedules screen refreshes using
``pyglet.clock.schedule()`` and calls ``pyglet.app.run()``, which will
continue displaying our cube until the escape key is pressed.

This script can be found at examples/simple-cube.py

