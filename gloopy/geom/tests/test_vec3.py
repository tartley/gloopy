
from __future__ import division
from math import sqrt, pi
from unittest import TestCase, main

from ..vec3 import (
    EPSILON, NegXAxis, NegYAxis, NegZAxis, Vec3, XAxis, YAxis, ZAxis,
)


class testVec3(TestCase):

    def testConstructor(self):
        v = Vec3(1, 2, 3)
        self.assertRaises(TypeError, lambda: Vec3())
        self.assertRaises(TypeError, lambda: Vec3(1))
        self.assertRaises(TypeError, lambda: Vec3(1, 2))
        self.assertRaises(TypeError, lambda: Vec3(1, 2, 3, 4))

    def testAccess(self):
        v = Vec3(1, 2, 3)
        self.assertEqual(v.x, 1)
        self.assertEqual(v.y, 2)
        self.assertEqual(v.z, 3)

    def testRepr(self):
        v = Vec3(1, 2, 3)
        self.assertEqual(str(v), 'Vec3(1, 2, 3)')

        v = Vec3(1.1, 2.2, 3.3)
        self.assertEqual(str(v), 'Vec3(1.1, 2.2, 3.3)')

    def testEq(self):
        self.assertTrue(Vec3(1, 2, 3) == Vec3(1, 2, 3))
        self.assertTrue(Vec3(1, 2, 3) == (1, 2, 3))
        self.assertFalse(Vec3(1, 2, 3) == Vec3(11, 2, 3))
        self.assertFalse(Vec3(1, 2, 3) == Vec3(1, 22, 3))
        self.assertFalse(Vec3(1, 2, 3) == Vec3(1, 2, 33))

        self.assertFalse(Vec3(1, 2, 3) == 123)
        self.assertFalse(Vec3(1, 2, 3) == 'hello')
        self.assertFalse(Vec3(1, 2, 3) == 1.23)

    def testNotEq(self):
        self.assertFalse(Vec3(1, 2, 3) != Vec3(1, 2, 3))
        self.assertFalse(Vec3(1, 2, 3) != (1, 2, 3))
        self.assertTrue(Vec3(1, 2, 3) != Vec3(11, 2, 3))
        self.assertTrue(Vec3(1, 2, 3) != Vec3(1, 22, 3))
        self.assertTrue(Vec3(1, 2, 3) != Vec3(1, 2, 33))

        self.assertTrue(Vec3(1, 2, 3) != 123)
        self.assertTrue(Vec3(1, 2, 3) != 'hello')
        self.assertTrue(Vec3(1, 2, 3) != 1.23)

    def testHash(self):
        self.assertRaises(TypeError, lambda: hash(Vec3(1, 2, 3)))

    def testAlmostEqual(self):
        error = EPSILON * 0.9
        self.assertEqual(Vec3(1, 2, 3), Vec3(1 + error, 2, 3))
        self.assertEqual(Vec3(1, 2, 3), Vec3(1, 2 + error, 3))
        self.assertEqual(Vec3(1, 2, 3), Vec3(1, 2, 3 + error))

        self.assertEqual(Vec3(1, 2, 3),     (1, 2, 3 + error))
        self.assertEqual(    (1, 2, 3), Vec3(1, 2, 3 + error))

        error = EPSILON * 1.1
        self.assertNotEqual(Vec3(1, 2, 3), Vec3(1 + error, 2, 3))
        self.assertNotEqual(Vec3(1, 2, 3), Vec3(1, 2 + error, 3))
        self.assertNotEqual(Vec3(1, 2, 3), Vec3(1, 2, 3 + error))

        self.assertNotEqual(Vec3(1, 2, 3),     (1, 2, 3 + error))
        self.assertNotEqual(    (1, 2, 3), Vec3(1, 2, 3 + error))

    def testLength(self):
        self.assertEqual(Vec3(2, 3, 4).length, sqrt(4 + 9 + 16))

    def testLength2(self):
        self.assertEqual(Vec3(2, 3, 4).length2, 4 + 9 + 16)

    def testNormalize(self):
        v = Vec3(3, 4, 5)
        self.assertEqual(
            v.normalized(),
            Vec3(3/v.length, 4/v.length, 5/v.length) )

    def testNeg(self):
        v = -Vec3(1, 2, 3)
        self.assertEqual(v.x, -1)
        self.assertEqual(v.y, -2)
        self.assertEqual(v.z, -3)

    def testAdd(self):
        self.assertEqual(Vec3(1, 2, 3) + Vec3(10, 20, 30), (11, 22, 33))
        self.assertEqual(Vec3(1, 2, 3) +     (10, 20, 30), (11, 22, 33))
        self.assertEqual(    (1, 2, 3) + Vec3(10, 20, 30), (11, 22, 33))
        self.assertRaises(TypeError, lambda: Vec3(1, 2, 3) + 4)
        self.assertRaises(TypeError, lambda: 4 + Vec3(1, 2, 3))

    def testSub(self):
        self.assertEqual(Vec3(11, 22, 33) - Vec3(10, 20, 30), (1, 2, 3))
        self.assertEqual(Vec3(11, 22, 33) -     (10, 20, 30), (1, 2, 3))
        self.assertEqual(    (11, 22, 33) - Vec3(10, 20, 30), (1, 2, 3))
        self.assertRaises(TypeError, lambda: Vec3(1, 2, 3) - 4)
        self.assertRaises(TypeError, lambda: 4 - Vec3(1, 2, 3))

    def testMul(self):
        self.assertEqual(Vec3(1, 2, 3) * 10, Vec3(10, 20, 30))
        self.assertEqual(10 * Vec3(1, 2, 3), Vec3(10, 20, 30))

    def testDiv(self):
        self.assertEqual(Vec3(10, 20, 30) / 10, Vec3(1, 2, 3))
        self.assertEqual(Vec3(2, 0, 0) / 3, Vec3(0.6666666666666667, 0, 0))
        self.assertRaises(ZeroDivisionError, lambda: Vec3(1, 2, 3) / 0)
        self.assertRaises(TypeError, lambda: 3 / Vec3(1, 2, 3))

    def testCrossProduct(self):
        a = Vec3(1, 0, 0)
        b = Vec3(0, 2, 0)
        c = Vec3(0, 0, 3)
        self.assertEqual(a.cross(b), (0, 0, 2))
        self.assertEqual(b.cross(a), (0, 0, -2))
        self.assertEqual(a.cross(c), (0, -3, 0))
        self.assertEqual(c.cross(a), (0, 3, 0))
        self.assertEqual(b.cross(c), (6, 0, 0))
        self.assertEqual(c.cross(b), (-6, 0, 0))

    def testDotProduct(self):
        a = Vec3(2, 3, 5)
        b = Vec3(7, 11, 13)
        self.assertEqual(a.dot(b), 2 * 7 + 3 * 11 + 5 * 13)

    def testAngle(self):
        a = Vec3(1, 0, 0)
        b = Vec3(1, 1, 0)
        self.assertAlmostEqual(a.angle(b), pi/4, places=15)
        self.assertAlmostEqual(a.angle(a), 0, places=7)
        self.assertAlmostEqual(b.angle(b), 0, places=7)

    def testRotate(self):
        self.assertEqual(XAxis.rotate(XAxis, pi/2), XAxis)
        self.assertEqual(YAxis.rotate(XAxis, pi/2), NegZAxis)
        self.assertEqual(ZAxis.rotate(XAxis, pi/2), YAxis)

        self.assertEqual(XAxis.rotate(YAxis, pi/2), ZAxis)
        self.assertEqual(YAxis.rotate(YAxis, pi/2), YAxis)
        self.assertEqual(ZAxis.rotate(YAxis, pi/2), NegXAxis)

        self.assertEqual(XAxis.rotate(ZAxis, pi/2), NegYAxis)
        self.assertEqual(YAxis.rotate(ZAxis, pi/2), XAxis)
        self.assertEqual(ZAxis.rotate(ZAxis, pi/2), ZAxis)


if __name__ == '__main__':
    main()

