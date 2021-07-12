import numpy as np
from sortedcontainers import SortedKeyList
from itertools import cycle
from .utils import *
from .plcurves import *

def intersections(seg1, seg2):
    """return the intersection point, if any, between the projections of two (oriented) segments in space. 
    The return value is the pair of baricentric coordinates of the intersection points, or None. If the end 
    of one segment is the beginning of the other, they are viewed as non-intersection."""
    if seg1 == seg2:
        return None
    if np.array_equal(seg1.beg, seg2.end) or np.array_equal(seg2.beg, seg1.end):
        return None
    p = seg1.beg[0:2]
    r = seg1.vec[0:2]
    q = seg2.beg[0:2]
    s = seg2.vec[0:2]
    diff1 = q - p
    cross1 = np.linalg.det(np.vstack((diff1, s)))
    cross2 = np.linalg.det(np.vstack((r, s)))
    cross3 = np.linalg.det(np.vstack((diff1, r)))
    if cross2 == 0 and cross3 == 0:
        raise Exception('collinear')
    if cross2 == 0:
        return None
    t = cross1 / cross2
    if t < 0 or t > 1:
        return None
    u = cross3/cross2
    if u < 0 or u > 1:
        return None
    return t, u

def dtCode(crossings):
    """
    Compute the Dowker-Thistlethwaite code of a list of crossings. Note that this code works for a knot only right now.
    """
    def dtpair(c1, c2):
        code1 = c1.DTcode
        code2 = c2.DTcode
        if code1%2 == code2%2:
            raise Exception("Goofy crossings")
        if code1%2 == 0:
            thecode = code1
            othercode = code2
            cc = c1
        else:
            thecode = code2
            othercode = code1
            cc = c2
        if cc.over is True:
            return (othercode, -thecode)
        else:
            return (othercode, thecode)
        
    codelist = []
    for i in range(0, len(crossings), 2):
        codelist.append(dtpair(crossings[i], crossings[i+1]))
    return [x[1] for x in sorted(codelist)]

def snaplink(l):
    """
    Generate the DT code in the form Snappy likes it."
    """
    relist = [tuple(l)]
    return 'Link(\"DT: ' + str(relist) + '\")'

class Crossing:
    
    def are_same(c1, c2):
        return c1.seg1 == c2.seg2 and c1.seg2 == c2.seg1

    def __init__(self, seg1, seg2, ind1=0, ind2=0, comp1=0, comp2=0):
        self.seg1 = seg1
        self.seg2 = seg2
        self.ind1 = ind1
        self.ind2 = ind2
        self.comp1 = comp1
        self.comp2 = comp2
        inter = intersections(seg1, seg2)
        if inter is None:
            self.over = None
            return
        a = inter[0]
        b = inter[1]
        z1 = (seg1.beg + a * seg1.vec)[2]
        z2 = (seg2.beg + b * seg2.vec)[2]
        if z1 == z2:
            raise Exception('not embedded, seg1 was {0}, seg2 was {1}'.format(seg1, seg2))
        self.t1 = a
        self.t2 = b
        seg1.crossings.add(self)
        if z1 > z2:
            self.over = True
        else:
            self.over = False
        self.cyclic_order = self.cyclic_o()
        self.DTcode = None
        self.thehash = self.get_hash()

    def cyclic_o(self):
        def get_c_dict(s1, s2):
            c_dict = {}
            c_dict[0] = (s1, "beg")
            c_dict[2] = (s1, "end")
            r = rank_two(s1.beg, s2.beg, s2.end)
            if r[0] == 1:
                c_dict[1] = (s2, "beg")
                c_dict[3] = (s2, "end")
            else:
                c_dict[1] = (s2, "end")
                c_dict[3] = (s2, "beg")
            return c_dict
        if self.over is False:
            return get_c_dict(self.seg1, self.seg2)
        else:
            return get_c_dict(self.seg2, self.seg1)

    def get_hash(self):
        h1 = hash(self.seg1)
        h2 = hash(self.seg2)
        if h1 < h2:
            return hash((self.seg1, self.seg2))
        return hash((self.seg2, self.seg1))

