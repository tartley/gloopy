
from math import pi
from unittest import TestCase, main

from OpenGL import GL

from ..vector import (
    Vector, neg_x_axis, neg_y_axis, neg_z_axis, x_axis, y_axis, z_axis,
)
from ..orientation import Orientation


class TestOrientation(TestCase):

    def testConstructionDefaults(self):
        o = Orientation()
        self.assertEqual(o.forward, neg_z_axis)
        self.assertEqual(o.up, y_axis)
        self.assertEqual(o.right, x_axis)

    def testConstructionConvertsBareTuples(self):
        o = Orientation(x_axis, z_axis)
        self.assertEquals(o.forward, x_axis)
        self.assertTrue(isinstance(o.forward, Vector))
        self.assertEquals(o.up, z_axis)
        self.assertTrue(isinstance(o.up, Vector))
        self.assertEquals(o.right, neg_y_axis)
        self.assertTrue(isinstance(o.right, Vector))

    def testConstructionNormalises(self):
        o = Orientation((1, 2, 3))
        self.assertAlmostEquals(o.forward.length, 1, places=15)
        self.assertAlmostEquals(o.up.length, 1, places=15)
        self.assertAlmostEquals(o.right.length, 1, places=15)

    def testConstructionBarfsOnNonOrthogonalVectors(self):
        self.assertRaises(AssertionError,
            lambda: Orientation((1, 2, 3), (3, -2, 1)))

    def testConstructionProvidesDefaultUp(self):
        self.assertEqual(Orientation(x_axis).up, y_axis)
        self.assertEqual(Orientation(y_axis).up, z_axis)
        self.assertEqual(Orientation(neg_y_axis).up, neg_z_axis)

    def testStr(self):
        self.assertEqual(str(Orientation(x_axis, up=y_axis)),
            'Orientation(Vector(1, 0, 0), up=Vector(0, 1, 0))')

    def testEqual(self):
        a = Orientation((0, 2, 3))
        self.assertTrue(a == Orientation((0, 2, 3)))
        self.assertFalse(a == Orientation((11, 2, 3)))
        self.assertFalse(a == Orientation((0, 2, 3), up=(0, -3, 2)))
        self.assertFalse(a == 123)

    def testNotEqual(self):
        a = Orientation((0, 2, 3))
        self.assertFalse(a != Orientation((0, 2, 3)))
        self.assertTrue(a != Orientation((11, 2, 3)))
        self.assertTrue(a != Orientation((0, 2, 3), up=(0, -3, 2)))
        self.assertTrue(a != 123)

    def testHash(self):
        a = Orientation((0, 2, 3))
        self.assertRaises(TypeError, lambda: hash(a))

    def testRoll(self):
        o = Orientation(z_axis)
        o.roll(pi/2)
        self.assertEqual(o, Orientation(z_axis, up=neg_x_axis))

    def testYaw(self):
        o = Orientation(z_axis)
        o.yaw(pi/2)
        self.assertEqual(o, Orientation(neg_x_axis))

    def testPitch(self):
        o = Orientation(z_axis)
        o.pitch(pi/2)
        self.assertEqual(o, Orientation(y_axis, up=neg_z_axis))

    def testMatrix(self):
        o = Orientation((1, 2, 3))
        self.assertEquals(type(o.matrix), (GL.GLfloat * 16))
        expected = [
            o.right.x,    o.right.y,    o.right.z,   0,
            o.up.x,       o.up.y,       o.up.z,      0,
           -o.forward.x, -o.forward.y, -o.forward.z, 0,
            0,            0,            0,           1,
        ]
        for a, e in zip(o.matrix, expected):
            self.assertAlmostEqual(a, e)


if __name__ == '__main__':
    main()

