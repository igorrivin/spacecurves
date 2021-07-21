import numpy as np
from .projections import *
from sortedcontainers import SortedKeyList

class Segment:
    def __init__(self, beg, end):
        self.beg = beg
        self.end = end
        self.vec = end - beg
        self.crossings = SortedKeyList(key=self.get_val)


    def get_val(self, crossing):
        if crossing.seg1 == self:
            return crossing.t1
        return crossing.t2


    def length(self):
        return np.linalg.norm(self.vec)

    def transform(self, mat):
        newbeg = mat @ beg
        newend = mat @ end
        return Segment(newbeg, newend)

    def traverse(self, beg):
        if len(self.crossings) == 0:
            return beg
        for i, c in enumerate(self.crossings, beg):
            c.DTcode = i
        return beg + len(self.crossings)

    def __repr__(self):
        return str(self.beg) + " " + str(self.end)

class PLCurve:
  def __init__(self, pointlist, isClosed):
      self.pointlist = pointlist
      ll = len(self.pointlist)
      preseglist = [Segment(pointlist[i], pointlist[i+1])for i in range(ll-1)]
      if isClosed is True:
          preseglist.append(Segment(pointlist[ll-1], pointlist[0]))
      self.seglist = preseglist

  def length(self):
      return sum([x.length() for x in seglist])
  
  def DTtraverse(self, beg):
      newbeg = beg
      for seg in self.seglist:
          newbeg = seg.traverse(newbeg)
          return newbeg


class Link:
    def __init__(self, curvelist):
        self.curvelist = curvelist
        self.crossings = []
        self.makeAllCrossings()
        beg = 1
        for c in self.curvelist:
            beg  = c.DTtraverse(beg)
        self.crossings.sort(key=lambda x: x.thehash)
        self.DTcode = dtCode(self.crossings)

    def makeCrossings(self, curve1, curve2, comp1, comp2):
        for i, seg1 in enumerate(curve1.seglist):
            for j, seg2 in enumerate(curve2.seglist):
                newcross = Crossing(seg1, seg2, i, j, comp1, comp2)
                if newcross.over is not None:
                    self.crossings.append(newcross)

    def makeAllCrossings(self):
        for i, c in enumerate(self.curvelist):
            for j, d in enumerate(self.curvelist):
                self.makeCrossings(c, d, i, j)
    
    
