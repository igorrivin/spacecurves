from sortedcontainers import SortedKeyList
import numpy as np


class Point():

    eps = 10.0e-7
    point_list = SortedKeyList(key=lambda x: x.h)
    projector = np.random.randn(3)

    def point_hash(ar):
        return ar @ Point.projector

    def add_point(ar):
        newpoint = Point(ar)

        close_vals = Point.point_list.irange_key(newpoint.h -Point.eps, newpoint.h + Point.eps)
    
        for i in close_vals:
            if np.linalg.norm(i.val-newpoint.val)<Point.eps:
                del newpoint
                return i
        Point.point_list.add(newpoint)
        return newpoint
    
    def __init__(self, ar):
        self.h = Point.point_hash(ar)
        self.val = ar
        self.edgeset = set()

    def __sub__(self, o):
      return self.val - o.val

    def update(self, ar):
      Point.point_list.discard(self)
      self.val = ar
      self.h = Point.point_hash(ar)
      Point.point_list.add(self)

    def totorus(self, r = 100, scaler = 10):
      pt = self.val

      x = pt[0]
      y = pt[1]
      z = pt[2]

      a = 2 * np.pi * z /scaler
      xim = (r+x) * np.cos(a)
      yim = (r+x) * np.sin(a)
      zim  = y

      self.update(np.array([xim, yim, zim]))

class Segment:
  def __init__(self, beg, end):
    self.beg = beg
    beg.segset.add(self)
    self.end = end
    end.segset.add(self)
    self.vec = end - beg
    self.crossings = SortedKeyList(key=self.get_val)

  def get_val(self, crossing):
    if crossing.seg1 == self:
      return crossing.t1
    return crossing.t2

  def length(self):
    return np.linalg.norm(self.vec)

  def project(self, mat):
    self.beg.val = mat @ self.beg.val
    self.end.val = mat @ self.end.val

  def traverse(self, beg):
    if len(self.crossings) == 0:
      return beg
    for i, c in enumerate(self.crossings, beg):
      c.DTcode = i
    return beg + len(self.crossings)

  def break_up(self,  zval=1.0):
    vec = self.vec
    x = vec[0]
    y = vec[1]
    z = vec[2]
    zs = np.arange(0, z, zval)
    rats = [i/z for i in zs]
    vecs = [vec *i for i in rats]
    seglist = []
    if len(vecs) == 1:
      return [self]
    p = self.beg
    for i in vecs[1:]:
      q = Point.add_point(self.beg.val + i)
      s = Segment(p, q)
      p = q
      seglist.append(s)

    if p == self.end:
      return seglist
    s = Segment(p, self.end)
    seglist.append(s)
    return seglist

  def totorus(self, zval):
    self.beg.totorus(zval)
    self.end.totorus(zval)
    self.vec = self.end - self.beg


  def __repr__(self):
    return str(self.beg) + " " + str(self.end)
