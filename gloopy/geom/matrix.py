
from .vector import Vector


class Matrix(object):
    '''
    4x4 matrix. Supports iteration over elements.

    .. function:: __init__(self, position=None, orientation=None)

        Creates a matrix representing the given orientation and offset.
    '''
    # ugly hack: orientation.py populates this to prevent cyclic imports
    _zero_rotation = None

    def __init__(self, position=None, orientation=None, elements=None):
        if elements:
            self.elements = elements
        else:
            if position is None:
                position = Vector.Origin
            if orientation is None:
                orientation = Matrix._zero_rotation
            p = position
            o = orientation
            self.elements = [
                  o.right.x,    o.right.y,    o.right.z, p.x,
                     o.up.x,       o.up.y,       o.up.z, p.y,
               -o.forward.x, -o.forward.y, -o.forward.z, p.z,
                          0,            0,            0,   1,
            ]

    def __iter__(self):
        return self.elements.__iter__()

    def __mul__(self, other):
        sa = self.elements[0]
        sb = self.elements[1]
        sc = self.elements[2]
        sd = self.elements[3]
        se = self.elements[4]
        sf = self.elements[5]
        sg = self.elements[6]
        sh = self.elements[7]
        si = self.elements[8]
        sj = self.elements[9]
        sk = self.elements[10]
        sl = self.elements[11]
        sm = self.elements[12]
        sn = self.elements[13]
        so = self.elements[14]
        sp = self.elements[15]
        oa = other.elements[0]
        ob = other.elements[1]
        oc = other.elements[2]
        od = other.elements[3]
        oe = other.elements[4]
        of = other.elements[5]
        og = other.elements[6]
        oh = other.elements[7]
        oi = other.elements[8]
        oj = other.elements[9]
        ok = other.elements[10]
        ol = other.elements[11]
        om = other.elements[12]
        on = other.elements[13]
        oo = other.elements[14]
        op = other.elements[15]
        return Matrix(elements=[
            sa * oa + sb * oe + sc * oi + sd * om,
            sa * ob + sb * of + sc * oj + sd * on,
            sa * oc + sb * og + sc * ok + sd * oo,
            sa * od + sb * oh + sc * ol + sd * op,
            se * oa + sf * oe + sg * oi + sh * om,
            se * ob + sf * of + sg * oj + sh * on,
            se * oc + sf * og + sg * ok + sh * oo,
            se * od + sf * oh + sg * ol + sh * op,
            si * oa + sj * oe + sk * oi + sl * om,
            si * ob + sj * of + sk * oj + sl * on,
            si * oc + sj * og + sk * ok + sl * oo,
            si * od + sj * oh + sk * ol + sl * op,
            sm * oa + sn * oe + so * oi + sp * om,
            sm * ob + sn * of + so * oj + sp * on,
            sm * oc + sn * og + so * ok + sp * oo,
            sm * od + sn * oh + so * ol + sp * op,
        ])


    def transform(self, vert):
        '''
        Return a new Vector equal to `vert` transformed by this matrix
        (i.e. rotated by our orientation and translated by our position.)
        '''
        e = self.elements
        return Vector(
            vert.x * e[0] + vert.y * e[1] + vert.z * e[2]   + e[3],
            vert.x * e[4] + vert.y * e[5] + vert.z * e[6]   + e[7],
            vert.x * e[8] + vert.y * e[9] + vert.z * e[10]  + e[11],
        )

