
from collections import namedtuple
from random import randint, uniform


class Color(namedtuple('ColorBase', 'r g b a')):

    NUM_COMPONENTS = 4

    __slots__ = []


    def __repr__(self):
        return 'Color(%d, %d, %d, %d)' %  (self.r, self.g, self.b, self.a)


    @staticmethod
    def Random():
        return Color(randint(0, 255), randint(0, 255), randint(0, 255), 255)


    @staticmethod
    def RandomSequence():
        while True:
            yield Color.Random()


    def tinted(self, other=None, bias=0.5):
        if other is None:
            other = white
        return Color(
            int(self.r * (1 - bias) + other.r * bias),
            int(self.g * (1 - bias) + other.g * bias),
            int(self.b * (1 - bias) + other.b * bias),
            int(self.a * (1 - bias) + other.a * bias),
        )

    def variations(self, other=None):
        while True:
            yield self.tinted(other, uniform(0, 1))


white = Color(255, 255, 255, 255)
grey = Color(128, 128, 128, 255)
black = Color(0, 0, 0, 255)

red = Color(255, 0, 0, 255)
orange = Color(255, 128, 0, 255)
yellow = Color(255, 255, 0, 255)
green = Color(0, 255, 0, 255)
cyan = Color(0, 255, 255, 255)
blue = Color(0, 0, 255, 255)
magenta = Color(255, 0, 255, 255)
paleblue = white.tinted(grey, 0.55).tinted(cyan, 0.05)

all_colors = [
    red, orange, yellow, green, cyan, blue, magenta, white, grey, black, paleblue]

