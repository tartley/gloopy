from __future__ import division

from collections import namedtuple
from random import uniform



class Color(namedtuple('__BaseColor', 'r g b a')):
    '''
    4-component named tuple: (r, g, b, a), all floats from 0.0 to 1.0,
    with some methods.

    .. function:: __init__(r, g, b[, a=1])

        ``r``,  ``g``, ``b``: red, green and blue

        ``a``: alpha (defaults to fully opaque)

        For example, to specify red color::

            from gloopy.color import Color
            red = Color(1, 0, 0)

        Or semi-transparent blue::

            red = Color(0, 0, 1, 0.5)

    Some predefined instances of Color provide named colors. These named colors
    are defined as attributes of the Color class::

        from gloopy.color import Color
        print Color.RoyalPurple
    
    The names and values are taken from the top 69 results of the xkcd color
    survey:

        http://blog.xkcd.com/2010/05/03/color-survey-results/
    '''

    CHANNEL_MAX = 1.0

    __slots__ = []

    # make constructor's 'a' argument optional
    def __new__(cls, r, g, b, a=CHANNEL_MAX):
        return super(Color, cls).__new__(cls, r, g, b, a)


    @staticmethod
    def Random():
        '''
        Return a new random color
        '''
        return Color(
            uniform(0, Color.CHANNEL_MAX),
            uniform(0, Color.CHANNEL_MAX),
            uniform(0, Color.CHANNEL_MAX),
        )


    def tinted(self, other, bias=0.5):
        '''
        Return a new color, interpolated between this color and `other` by an
        amount specified by `bias`, which normally ranges from 0.0 (entirely
        this color) to 1.0 (entirely `other`.)
        '''
        unbias = 1 - bias
        return Color(
            self.r * unbias + other.r * bias,
            self.g * unbias + other.g * bias,
            self.b * unbias + other.b * bias,
            self.a * unbias + other.a * bias,
        )

    def inverted(self):
        '''
        Return a new color which is the complement of this one, i.e. if this
        color contains a lot of red, the return value will contain little red,
        and so on.
        '''
        return Color(
            1.0 - self.r,
            1.0 - self.g,
            1.0 - self.b,
            self.a
        )


Color.Blue         = Color(0.012, 0.263, 0.875)
Color.Pink         = Color(1.000, 0.506, 0.753)
Color.Peach        = Color(1.000, 0.690, 0.486)
Color.Purple       = Color(0.494, 0.118, 0.612)
Color.RoyalBlue    = Color(0.020, 0.016, 0.667)
Color.LightBrown   = Color(0.678, 0.506, 0.314)
Color.DarkRed      = Color(0.518, 0.000, 0.000)
Color.NeonGreen    = Color(0.047, 1.000, 0.047)
Color.Aquamarine   = Color(0.016, 0.847, 0.698)
Color.Black        = Color(0.000, 0.000, 0.000)
Color.Maroon       = Color(0.396, 0.000, 0.129)
Color.Orange       = Color(0.976, 0.451, 0.024)
Color.Red          = Color(0.898, 0.000, 0.000)
Color.MintGreen    = Color(0.561, 1.000, 0.624)
Color.PaleGreen    = Color(0.780, 0.992, 0.710)
Color.Brown        = Color(0.396, 0.216, 0.000)
Color.Turquoise    = Color(0.024, 0.761, 0.675)
Color.Khaki        = Color(0.667, 0.651, 0.384)
Color.DarkGreen    = Color(0.012, 0.208, 0.000)
Color.DarkTeal     = Color(0.004, 0.302, 0.306)
Color.LightPurple  = Color(0.749, 0.467, 0.965)
Color.BrightBlue   = Color(0.004, 0.396, 0.988)
Color.BabyBlue     = Color(0.635, 0.812, 0.996)
Color.Salmon       = Color(1.000, 0.475, 0.424)
Color.DarkPurple   = Color(0.208, 0.024, 0.243)
Color.RoyalPurple  = Color(0.294, 0.000, 0.431)
Color.BrickRed     = Color(0.561, 0.078, 0.008)
Color.Rose         = Color(0.812, 0.384, 0.459)
Color.Olive        = Color(0.431, 0.459, 0.055)
Color.Cyan         = Color(0.000, 1.000, 1.000)
Color.HotPink      = Color(1.000, 0.008, 0.553)
Color.OliveGreen   = Color(0.404, 0.478, 0.016)
Color.LightBlue    = Color(0.584, 0.816, 0.988)
Color.Plum         = Color(0.345, 0.059, 0.255)
Color.Aqua         = Color(0.075, 0.918, 0.788)
Color.Grey         = Color(0.576, 0.576, 0.576)
Color.YellowGreen  = Color(0.753, 0.984, 0.176)
Color.LightGreen   = Color(0.588, 0.976, 0.482)
Color.DarkPink     = Color(0.796, 0.255, 0.420)
Color.ForestGreen  = Color(0.024, 0.278, 0.047)
Color.Green        = Color(0.082, 0.690, 0.102)
Color.Beige        = Color(0.902, 0.855, 0.651)
Color.Teal         = Color(0.008, 0.576, 0.525)
Color.PaleBlue     = Color(0.816, 0.996, 0.996)
Color.Burgundy     = Color(0.380, 0.000, 0.137)
Color.Tan          = Color(0.820, 0.698, 0.435)
Color.Mustard      = Color(0.808, 0.702, 0.004)
Color.SkyBlue      = Color(0.459, 0.733, 0.992)
Color.BurntOrange  = Color(0.753, 0.306, 0.004)
Color.GrassGreen   = Color(0.247, 0.608, 0.043)
Color.Indigo       = Color(0.220, 0.008, 0.510)
Color.Lilac        = Color(0.808, 0.635, 0.992)
Color.BrightGreen  = Color(0.004, 1.000, 0.027)
Color.DarkBlue     = Color(0.000, 0.012, 0.357)
Color.LimeGreen    = Color(0.537, 0.996, 0.020)
Color.SeaGreen     = Color(0.325, 0.988, 0.631)
Color.Lavender     = Color(0.780, 0.624, 0.937)
Color.Yellow       = Color(1.000, 1.000, 0.078)
Color.Mauve        = Color(0.682, 0.443, 0.506)
Color.NavyBlue     = Color(0.000, 0.067, 0.275)
Color.LightPink    = Color(1.000, 0.820, 0.875)
Color.BlueGreen    = Color(0.075, 0.494, 0.427)
Color.Gold         = Color(0.859, 0.706, 0.047)
Color.BrightPurple = Color(0.745, 0.012, 0.992)
Color.Violet       = Color(0.604, 0.055, 0.918)
Color.Navy         = Color(0.004, 0.082, 0.243)
Color.Periwinkle   = Color(0.557, 0.510, 0.996)
Color.Magenta      = Color(0.761, 0.000, 0.471)
Color.Lime         = Color(0.667, 1.000, 0.196)

# some extras defined by me
Color.White        = Color(1.000, 1.000, 1.000)
Color.LightGrey    = Color(0.753, 0.753, 0.753)
Color.DarkGrey     = Color(0.251, 0.251, 0.251)

Color.All = {
    name: value
    for name, value in Color.__dict__.iteritems()
    if isinstance(value, Color)
}

