from __future__ import division

from collections import namedtuple
from random import randint, uniform

__BaseColor = namedtuple('BaseColor', 'r g b a')


class Color(__BaseColor):
    '''
    A Color is a named tuple of four unsigned bytes (Note this is likely to
    change in the future to using floats throughout. It seems that once
    geometry is pushed to a VBO, the performance gains of using ubytes
    diminish substantially).

    .. function:: __init__(r, g, b[, a])

        r: red
        g: green
        b: blue
        a: alpha (defaults to fully opaque)
        All of r, g, b, a are ints from 0 to 255 (Color.MAX_CHANNEL.)
        
        For example, to specify a red color::

            from gloopy.color import Color
            red = Color(255, 0, 0)

        Or semi-transparent blue::

            red = Color(0, 0, 255, 127)
  

    Some predefined instances of Color provide named colors. These named colors
    are defined as attributes of the Color class::

        from gloopy.color import Color
        print Color.RoyalPurple
    
    The names and values are taken from the top 69 results of the xkcd color
    survey:

        http://blog.xkcd.com/2010/05/03/color-survey-results/
    '''

    COMPONENTS = 4
    MAX_CHANNEL = 0xff

    __slots__ = []

    # make constructor's 'a' argument optional
    def __new__(cls, r, g, b, a=MAX_CHANNEL):
        return super(Color, cls).__new__(cls, r, g, b, a)

    @staticmethod
    def Random():
        '''
        Return a new random color
        '''
        return Color(
            randint(0, Color.MAX_CHANNEL),
            randint(0, Color.MAX_CHANNEL),
            randint(0, Color.MAX_CHANNEL),
        )

    @staticmethod
    def Randoms():
        '''
        Generate an infinite sequence of random colors.
        '''
        while True:
            yield Color.Random()


    def as_floats(self):
        '''
        Returns this color as a tuple of normalised floats, suitable for use
        with glSetClearColor. Note this method is likely to be deleted in a
        subsequent release, when colors change to being stored internally as
        floats.
        '''
        return (
            1 / Color.MAX_CHANNEL * self.r,
            1 / Color.MAX_CHANNEL * self.g,
            1 / Color.MAX_CHANNEL * self.b,
            1 / Color.MAX_CHANNEL * self.a,
        )


    def tinted(self, other, bias=0.5):
        '''
        Return a new color, interpolated between this color and `other` by an
        amount specified by `bias`, which normally ranges from 0.0 (entirely
        this color) to 1.0 (entirely `other`.)
        '''
        return Color(
            int(self.r * (1 - bias) + other.r * bias),
            int(self.g * (1 - bias) + other.g * bias),
            int(self.b * (1 - bias) + other.b * bias),
            int(self.a * (1 - bias) + other.a * bias),
        )


    def variations(self, other=None):
        '''
        Generate an infinite sequence of colors which are tinted by random
        amounts towards `other`, which defaults to a darker version of this
        color.
        '''
        if other is None:
            other = self.tinted(Color.Black, 0.5)
        while True:
            yield self.tinted(other, uniform(0, 1))


    def inverted(self):
        '''
        Return a new color which is the complement of this one, i.e. if this
        color contains a lot of red, the return value will contain little red,
        and so on.
        '''
        return Color(
            255 - self.r,
            255 - self.g,
            255 - self.b,
            self.a
        )


Color.Purple       = Color(0x7e, 0x1e, 0x9c)
Color.Green        = Color(0x15, 0xb0, 0x1a)
Color.Blue         = Color(0x03, 0x43, 0xdf)
Color.Pink         = Color(0xff, 0x81, 0xc0)
Color.Brown        = Color(0x65, 0x37, 0x00)
Color.Red          = Color(0xe5, 0x00, 0x00)
Color.LightBlue    = Color(0x95, 0xd0, 0xfc)
Color.Teal         = Color(0x02, 0x93, 0x86)
Color.Orange       = Color(0xf9, 0x73, 0x06)
Color.LightGreen   = Color(0x96, 0xf9, 0x7b)
Color.Magenta      = Color(0xc2, 0x00, 0x78)
Color.Yellow       = Color(0xff, 0xff, 0x14)
Color.SkyBlue      = Color(0x75, 0xbb, 0xfd)
Color.Grey         = Color(0x93, 0x93, 0x93)
Color.LimeGreen    = Color(0x89, 0xfe, 0x05)
Color.LightPurple  = Color(0xbf, 0x77, 0xf6)
Color.Violet       = Color(0x9a, 0x0e, 0xea)
Color.DarkGreen    = Color(0x03, 0x35, 0x00)
Color.Turquoise    = Color(0x06, 0xc2, 0xac)
Color.Lavender     = Color(0xc7, 0x9f, 0xef)
Color.DarkBlue     = Color(0x00, 0x03, 0x5b)
Color.Tan          = Color(0xd1, 0xb2, 0x6f)
Color.Cyan         = Color(0x00, 0xff, 0xff)
Color.Aqua         = Color(0x13, 0xea, 0xc9)
Color.ForestGreen  = Color(0x06, 0x47, 0x0c)
Color.Mauve        = Color(0xae, 0x71, 0x81)
Color.DarkPurple   = Color(0x35, 0x06, 0x3e)
Color.BrightGreen  = Color(0x01, 0xff, 0x07)
Color.Maroon       = Color(0x65, 0x00, 0x21)
Color.Olive        = Color(0x6e, 0x75, 0x0e)
Color.Salmon       = Color(0xff, 0x79, 0x6c)
Color.Beige        = Color(0xe6, 0xda, 0xa6)
Color.RoyalBlue    = Color(0x05, 0x04, 0xaa)
Color.NavyBlue     = Color(0x00, 0x11, 0x46)
Color.Lilac        = Color(0xce, 0xa2, 0xfd)
Color.Black        = Color(0x00, 0x00, 0x00)
Color.HotPink      = Color(0xff, 0x02, 0x8d)
Color.LightBrown   = Color(0xad, 0x81, 0x50)
Color.PaleGreen    = Color(0xc7, 0xfd, 0xb5)
Color.Peach        = Color(0xff, 0xb0, 0x7c)
Color.OliveGreen   = Color(0x67, 0x7a, 0x04)
Color.DarkPink     = Color(0xcb, 0x41, 0x6b)
Color.Periwinkle   = Color(0x8e, 0x82, 0xfe)
Color.SeaGreen     = Color(0x53, 0xfc, 0xa1)
Color.Lime         = Color(0xaa, 0xff, 0x32)
Color.Indigo       = Color(0x38, 0x02, 0x82)
Color.Mustard      = Color(0xce, 0xb3, 0x01)
Color.LightPink    = Color(0xff, 0xd1, 0xdf)
Color.Rose         = Color(0xcf, 0x62, 0x75)
Color.BrightBlue   = Color(0x01, 0x65, 0xfc)
Color.NeonGreen    = Color(0x0c, 0xff, 0x0c)
Color.BurntOrange  = Color(0xc0, 0x4e, 0x01)
Color.Aquamarine   = Color(0x04, 0xd8, 0xb2)
Color.Navy         = Color(0x01, 0x15, 0x3e)
Color.GrassGreen   = Color(0x3f, 0x9b, 0x0b)
Color.PaleBlue     = Color(0xd0, 0xfe, 0xfe)
Color.DarkRed      = Color(0x84, 0x00, 0x00)
Color.BrightPurple = Color(0xbe, 0x03, 0xfd)
Color.YellowGreen  = Color(0xc0, 0xfb, 0x2d)
Color.BabyBlue     = Color(0xa2, 0xcf, 0xfe)
Color.Gold         = Color(0xdb, 0xb4, 0x0c)
Color.MintGreen    = Color(0x8f, 0xff, 0x9f)
Color.Plum         = Color(0x58, 0x0f, 0x41)
Color.RoyalPurple  = Color(0x4b, 0x00, 0x6e)
Color.BrickRed     = Color(0x8f, 0x14, 0x02)
Color.DarkTeal     = Color(0x01, 0x4d, 0x4e)
Color.Burgundy     = Color(0x61, 0x00, 0x23)
Color.Khaki        = Color(0xaa, 0xa6, 0x62)
Color.BlueGreen    = Color(0x13, 0x7e, 0x6d)

# some extras defined by me
Color.White     = Color(0xff, 0xff, 0xff)
Color.LightGrey = Color(0xc0, 0xc0, 0xc0)
Color.DarkGrey  = Color(0x40, 0x40, 0x40)

Color.All = {
    name: value for name, value in Color.__dict__.iteritems()
    if isinstance(value, Color)
}

