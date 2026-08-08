
from unittest import TestCase, main

from ..orientation import Orientation
from ..matrix import Matrix
from ..vector import Vector


class TestMatrix(TestCase):

    def testConstructor(self):
        position = Vector(1, 2, 3)
        orientation = Orientation((4, 5, 6))

        matrix = Matrix(position, orientation)

        self.assertEqual(matrix.elements[0], orientation.right.x)
        self.assertEqual(matrix.elements[1], orientation.right.y)
        self.assertEqual(matrix.elements[2], orientation.right.z)

        self.assertEqual(matrix.elements[4], orientation.up.x)
        self.assertEqual(matrix.elements[5], orientation.up.y)
        self.assertEqual(matrix.elements[6], orientation.up.z)

        self.assertEqual(matrix.elements[8], -orientation.forward.x)
        self.assertEqual(matrix.elements[9], -orientation.forward.y)
        self.assertEqual(matrix.elements[10], -orientation.forward.z)

        self.assertEqual(matrix.elements[3], position.x)
        self.assertEqual(matrix.elements[7], position.y)
        self.assertEqual(matrix.elements[11], position.z)

        self.assertEqual(matrix.elements[12], 0)
        self.assertEqual(matrix.elements[13], 0)
        self.assertEqual(matrix.elements[14], 0)
        self.assertEqual(matrix.elements[15], 1)


    def testMulVertex(self):
        position = Vector(10, 20, 30)
        vert = Vector(1, 2, 3)

        # default orientation, this should translate only, zero rotation
        orientation = Orientation()
        matrix = Matrix(position, orientation)
        self.assertEqual(matrix * vert - position, vert)

        # now try a couple of transforms which do involve a rotation
        orientation = Orientation(Vector.y_axis)
        matrix = Matrix(position, orientation)
        self.assertEqual(matrix * vert - position, (1, 3, -2))

        orientation = Orientation(Vector.x_axis)
        matrix = Matrix(position, orientation)
        self.assertEqual(matrix * vert - position, (3, 2, -1))


if __name__ == '__main__':
    main()

