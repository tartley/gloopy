from __future__ import division

from collections import namedtuple
from random import randint


class Color(namedtuple('Color', 'r g b a')):
    '''
    r: red
    g: green
    b: blue
    a=MAX_CHANNEL: alpha or opacity.

    Colors in Gloopy are specified using unsigned bytes, meaning that all of r,
    g, b, a are ints from 0 to 255 (Color.MAX_CHANNEL.) Alpha values of less
    than MAX_CHANNEL represent levels of transparency, down to an alpha of 0,
    which is completely invisible. Specifying alpha is optional, it defaults
    to fully-opaque.

    For example, to specify a red color::

        from gloopy.color import Color
        red = Color(255, 0, 0)

    Some predefined instances of Color provide named colors. These named colors
    are defined at the gloopy.color module level::
    
        from gloopy.color import GrassGreen

    and are also attached as attributes of the Color class::

        from gloopy.color import Color
        print Color.RoyalPurple
    
    The names and values are taken from the top 69 results of the xkcd color
    survey: http://blog.xkcd.com/2010/05/03/color-survey-results/
    '''

    NUM_COMPONENTS = 4
    MAX_CHANNEL = 0xff

    __slots__ = []

    # make constructor's 'a' argument optional
    def __new__(cls, r, g, b, a=MAX_CHANNEL):
        return super(Color, cls).__new__(cls, r, g, b, a)


    @staticmethod
    def Random():
        return Color(randint(0, 255), randint(0, 255), randint(0, 255), 255)


    def as_floats(self):
        '''
        Returns this color as a tuple of normalised floats, suitable for use
        with glSetClearColor.
        '''
        return (
            1 / 255 * self.r,
            1 / 255 * self.g,
            1 / 255 * self.b,
            1 / 255 * self.a
        )


    def tinted(self, other, bias=0.5):
        return Color(
            int(self.r * (1 - bias) + other.r * bias),
            int(self.g * (1 - bias) + other.g * bias),
            int(self.b * (1 - bias) + other.b * bias),
            int(self.a * (1 - bias) + other.a * bias),
        )


Purple       = Color(0x7e, 0x1e, 0x9c)
Green        = Color(0x15, 0xb0, 0x1a)
Blue         = Color(0x03, 0x43, 0xdf)
Pink         = Color(0xff, 0x81, 0xc0)
Brown        = Color(0x65, 0x37, 0x00)
Red          = Color(0xe5, 0x00, 0x00)
LightBlue    = Color(0x95, 0xd0, 0xfc)
Teal         = Color(0x02, 0x93, 0x86)
Orange       = Color(0xf9, 0x73, 0x06)
LightGreen   = Color(0x96, 0xf9, 0x7b)
Magenta      = Color(0xc2, 0x00, 0x78)
Yellow       = Color(0xff, 0xff, 0x14)
SkyBlue      = Color(0x75, 0xbb, 0xfd)
Grey         = Color(0x93, 0x93, 0x93)
LimeGreen    = Color(0x89, 0xfe, 0x05)
LightPurple  = Color(0xbf, 0x77, 0xf6)
Violet       = Color(0x9a, 0x0e, 0xea)
DarkGreen    = Color(0x03, 0x35, 0x00)
Turquoise    = Color(0x06, 0xc2, 0xac)
Lavender     = Color(0xc7, 0x9f, 0xef)
DarkBlue     = Color(0x00, 0x03, 0x5b)
Tan          = Color(0xd1, 0xb2, 0x6f)
Cyan         = Color(0x00, 0xff, 0xff)
Aqua         = Color(0x13, 0xea, 0xc9)
ForestGreen  = Color(0x06, 0x47, 0x0c)
Mauve        = Color(0xae, 0x71, 0x81)
DarkPurple   = Color(0x35, 0x06, 0x3e)
BrightGreen  = Color(0x01, 0xff, 0x07)
Maroon       = Color(0x65, 0x00, 0x21)
Olive        = Color(0x6e, 0x75, 0x0e)
Salmon       = Color(0xff, 0x79, 0x6c)
Beige        = Color(0xe6, 0xda, 0xa6)
RoyalBlue    = Color(0x05, 0x04, 0xaa)
NavyBlue     = Color(0x00, 0x11, 0x46)
Lilac        = Color(0xce, 0xa2, 0xfd)
Black        = Color(0x00, 0x00, 0x00)
HotPink      = Color(0xff, 0x02, 0x8d)
LightBrown   = Color(0xad, 0x81, 0x50)
PaleGreen    = Color(0xc7, 0xfd, 0xb5)
Peach        = Color(0xff, 0xb0, 0x7c)
OliveGreen   = Color(0x67, 0x7a, 0x04)
DarkPink     = Color(0xcb, 0x41, 0x6b)
Periwinkle   = Color(0x8e, 0x82, 0xfe)
SeaGreen     = Color(0x53, 0xfc, 0xa1)
Lime         = Color(0xaa, 0xff, 0x32)
Indigo       = Color(0x38, 0x02, 0x82)
Mustard      = Color(0xce, 0xb3, 0x01)
LightPink    = Color(0xff, 0xd1, 0xdf)
Rose         = Color(0xcf, 0x62, 0x75)
BrightBlue   = Color(0x01, 0x65, 0xfc)
NeonGreen    = Color(0x0c, 0xff, 0x0c)
BurntOrange  = Color(0xc0, 0x4e, 0x01)
Aquamarine   = Color(0x04, 0xd8, 0xb2)
Navy         = Color(0x01, 0x15, 0x3e)
GrassGreen   = Color(0x3f, 0x9b, 0x0b)
PaleBlue     = Color(0xd0, 0xfe, 0xfe)
DarkRed      = Color(0x84, 0x00, 0x00)
BrightPurple = Color(0xbe, 0x03, 0xfd)
YellowGreen  = Color(0xc0, 0xfb, 0x2d)
BabyBlue     = Color(0xa2, 0xcf, 0xfe)
Gold         = Color(0xdb, 0xb4, 0x0c)
MintGreen    = Color(0x8f, 0xff, 0x9f)
Plum         = Color(0x58, 0x0f, 0x41)
RoyalPurple  = Color(0x4b, 0x00, 0x6e)
BrickRed     = Color(0x8f, 0x14, 0x02)
DarkTeal     = Color(0x01, 0x4d, 0x4e)
Burgundy     = Color(0x61, 0x00, 0x23)
Khaki        = Color(0xaa, 0xa6, 0x62)
BlueGreen    = Color(0x13, 0x7e, 0x6d)

# some extras defined by me
White     = Color(0xff, 0xff, 0xff)
LightGrey = Color(0xc0, 0xc0, 0xc0)
DarkGrey  = Color(0x40, 0x40, 0x40)


# attach named colors as attributes of Color class
for name, value in locals().items():
    if isinstance(value, Color):
        setattr(Color, name, value)

