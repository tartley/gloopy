from __future__ import division
from math import sqrt, pi
from unittest import TestCase, main

from ..vector import EPSILON, Vector


class testVector(TestCase):

    def testConstructor(self):
        v = Vector(1, 2, 3)
        self.assertEquals(v.x, 1)
        self.assertEquals(v.y, 2)
        self.assertEquals(v.z, 3)
        self.assertRaises(TypeError, lambda: Vector())
        self.assertRaises(TypeError, lambda: Vector(1))
        self.assertRaises(TypeError, lambda: Vector(1, 2))
        self.assertRaises(TypeError, lambda: Vector(1, 2, 3, 4))

    def testAccess(self):
        v = Vector(1, 2, 3)
        self.assertEqual(v.x, 1)
        self.assertEqual(v.y, 2)
        self.assertEqual(v.z, 3)

    def testRepr(self):
        v = Vector(1, 2, 3)
        self.assertEqual(str(v), 'Vector(1, 2, 3)')

        v = Vector(1.1, 2.2, 3.3)
        self.assertEqual(str(v), 'Vector(1.1, 2.2, 3.3)')

    def testEq(self):
        self.assertTrue(Vector(1, 2, 3) == Vector(1, 2, 3))
        self.assertTrue(Vector(1, 2, 3) == (1, 2, 3))
        self.assertFalse(Vector(1, 2, 3) == Vector(11, 2, 3))
        self.assertFalse(Vector(1, 2, 3) == Vector(1, 22, 3))
        self.assertFalse(Vector(1, 2, 3) == Vector(1, 2, 33))

        self.assertFalse(Vector(1, 2, 3) == 123)
        self.assertFalse(Vector(1, 2, 3) == 'hello')
        self.assertFalse(Vector(1, 2, 3) == 1.23)

    def testNotEq(self):
        self.assertFalse(Vector(1, 2, 3) != Vector(1, 2, 3))
        self.assertFalse(Vector(1, 2, 3) != (1, 2, 3))
        self.assertTrue(Vector(1, 2, 3) != Vector(11, 2, 3))
        self.assertTrue(Vector(1, 2, 3) != Vector(1, 22, 3))
        self.assertTrue(Vector(1, 2, 3) != Vector(1, 2, 33))

        self.assertTrue(Vector(1, 2, 3) != 123)
        self.assertTrue(Vector(1, 2, 3) != 'hello')
        self.assertTrue(Vector(1, 2, 3) != 1.23)

    def testHash(self):
        self.assertRaises(TypeError, lambda: hash(Vector(1, 2, 3)))

    def testAlmostEqual(self):
        error = EPSILON * 0.9
        self.assertEqual(Vector(1, 2, 3), Vector(1 + error, 2, 3))
        self.assertEqual(Vector(1, 2, 3), Vector(1, 2 + error, 3))
        self.assertEqual(Vector(1, 2, 3), Vector(1, 2, 3 + error))

        self.assertEqual(Vector(1, 2, 3),     (1, 2, 3 + error))
        self.assertEqual(    (1, 2, 3), Vector(1, 2, 3 + error))

        error = EPSILON * 1.1
        self.assertNotEqual(Vector(1, 2, 3), Vector(1 + error, 2, 3))
        self.assertNotEqual(Vector(1, 2, 3), Vector(1, 2 + error, 3))
        self.assertNotEqual(Vector(1, 2, 3), Vector(1, 2, 3 + error))

        self.assertNotEqual(Vector(1, 2, 3),     (1, 2, 3 + error))
        self.assertNotEqual(    (1, 2, 3), Vector(1, 2, 3 + error))

    def testLength(self):
        self.assertEqual(Vector(2, 3, 4).length, sqrt(4 + 9 + 16))

    def testLength2(self):
        self.assertEqual(Vector(2, 3, 4).length2, 4 + 9 + 16)

    def testNormalize(self):
        v = Vector(3, 4, 5)
        self.assertEqual(
            v.normalized(),
            Vector(3.0 / v.length, 4.0 / v.length, 5.0 / v.length) )

    def testNeg(self):
        v = -Vector(1, 2, 3)
        self.assertEqual(v.x, -1)
        self.assertEqual(v.y, -2)
        self.assertEqual(v.z, -3)

    def testAdd(self):
        self.assertEqual(Vector(1, 2, 3) + Vector(10, 20, 30), (11, 22, 33))
        self.assertEqual(Vector(1, 2, 3) +     (10, 20, 30), (11, 22, 33))
        self.assertEqual(    (1, 2, 3) + Vector(10, 20, 30), (11, 22, 33))
        self.assertRaises(TypeError, lambda: Vector(1, 2, 3) + 4)
        self.assertRaises(TypeError, lambda: 4 + Vector(1, 2, 3))

    def testSub(self):
        self.assertEqual(Vector(11, 22, 33) - Vector(10, 20, 30), (1, 2, 3))
        self.assertEqual(Vector(11, 22, 33) -     (10, 20, 30), (1, 2, 3))
        self.assertEqual(    (11, 22, 33) - Vector(10, 20, 30), (1, 2, 3))
        self.assertRaises(TypeError, lambda: Vector(1, 2, 3) - 4)
        self.assertRaises(TypeError, lambda: 4 - Vector(1, 2, 3))

    def testMul(self):
        self.assertEqual(Vector(1, 2, 3) * 10, Vector(10, 20, 30))
        self.assertEqual(10 * Vector(1, 2, 3), Vector(10, 20, 30))

    def testDiv(self):
        self.assertEqual(Vector(20, 40, 30) / 20, Vector(1, 2, 1.5))
        self.assertEqual(Vector(2, 0, 0) / 3, Vector(0.6666666666666667, 0, 0))
        self.assertRaises(ZeroDivisionError, lambda: Vector(1, 2, 3) / 0)
        self.assertRaises(TypeError, lambda: 3 / Vector(1, 2, 3))

    def testCrossProduct(self):
        a = Vector(1, 0, 0)
        b = Vector(0, 2, 0)
        c = Vector(0, 0, 3)
        self.assertEqual(a.cross(b), (0, 0, 2))
        self.assertEqual(b.cross(a), (0, 0, -2))
        self.assertEqual(a.cross(c), (0, -3, 0))
        self.assertEqual(c.cross(a), (0, 3, 0))
        self.assertEqual(b.cross(c), (6, 0, 0))
        self.assertEqual(c.cross(b), (-6, 0, 0))

    def testDotProduct(self):
        a = Vector(2, 3, 5)
        b = Vector(7, 11, 13)
        self.assertEqual(a.dot(b), 2 * 7 + 3 * 11 + 5 * 13)

    def testAngle(self):
        a = Vector(1, 0, 0)
        b = Vector(1, 1, 0)
        self.assertAlmostEqual(a.angle(b), pi/4, places=15)
        self.assertAlmostEqual(a.angle(a), 0, places=7)
        self.assertAlmostEqual(b.angle(b), 0, places=7)

    def testRotate(self):
        self.assertEqual(Vector.XAxis.rotate(Vector.XAxis, pi/2), Vector.XAxis)
        self.assertEqual(Vector.YAxis.rotate(Vector.XAxis, pi/2), Vector.ZNegAxis)
        self.assertEqual(Vector.ZAxis.rotate(Vector.XAxis, pi/2), Vector.YAxis)

        self.assertEqual(Vector.XAxis.rotate(Vector.YAxis, pi/2), Vector.ZAxis)
        self.assertEqual(Vector.YAxis.rotate(Vector.YAxis, pi/2), Vector.YAxis)
        self.assertEqual(Vector.ZAxis.rotate(Vector.YAxis, pi/2), Vector.XNegAxis)

        self.assertEqual(Vector.XAxis.rotate(Vector.ZAxis, pi/2), Vector.YNegAxis)
        self.assertEqual(Vector.YAxis.rotate(Vector.ZAxis, pi/2), Vector.XAxis)
        self.assertEqual(Vector.ZAxis.rotate(Vector.ZAxis, pi/2), Vector.ZAxis)


if __name__ == '__main__':
    main()

