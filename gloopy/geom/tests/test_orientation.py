
from math import pi
from unittest import TestCase, main

from OpenGL import GL

from ..vector import Vector
from ..orientation import Orientation


class TestOrientation(TestCase):

    def testConstructionDefaults(self):
        o = Orientation()
        self.assertEqual(o.forward, Vector.ZNegAxis)
        self.assertEqual(o.up, Vector.YAxis)
        self.assertEqual(o.right, Vector.XAxis)

    def testConstructionConvertsBareTuples(self):
        o = Orientation(Vector.XAxis, Vector.ZAxis)
        self.assertEquals(o.forward, Vector.XAxis)
        self.assertTrue(isinstance(o.forward, Vector))
        self.assertEquals(o.up, Vector.ZAxis)
        self.assertTrue(isinstance(o.up, Vector))
        self.assertEquals(o.right, Vector.YNegAxis)
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
        self.assertEqual(Orientation(Vector.XAxis).up, Vector.YAxis)
        self.assertEqual(Orientation(Vector.YAxis).up, Vector.ZAxis)
        self.assertEqual(Orientation(Vector.YNegAxis).up, Vector.ZNegAxis)

    def testStr(self):
        self.assertEqual(str(Orientation(Vector.XAxis, up=Vector.YAxis)),
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
        o = Orientation(Vector.ZAxis)
        o.roll(pi/2)
        self.assertEqual(o, Orientation(Vector.ZAxis, up=Vector.XNegAxis))

    def testYaw(self):
        o = Orientation(Vector.ZAxis)
        o.yaw(pi/2)
        self.assertEqual(o, Orientation(Vector.XNegAxis))

    def testPitch(self):
        o = Orientation(Vector.ZAxis)
        o.pitch(pi/2)
        self.assertEqual(o, Orientation(Vector.YAxis, up=Vector.ZNegAxis))

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

