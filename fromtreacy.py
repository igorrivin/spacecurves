import numpy as np
import sys
import os

from geom import Point, Segment

def otherend(pt, seg):
    if pt == seg.beg:
        return seg.end
    return seg.beg

def otherseg(pt, seg):
    s1 = pt.segset
    s2 = set(seg)
    d = s1 - s2
    return list(d)[0]

thelines = sys.stdin.readlines()

for i in thelines[3:]:
    fields = [x.strip() for x in i.split(' ')]
    numfields = fields[:3] + fields[4:]
    numbers = [float(x) for x in numfields]
    val1 = np.array(numbers[:3])
    val2 = np.array(numbers[4:])
    p1 = Point.add_point(val1)
    p2 = Point.add_point(val2)
    s = Segment(p1, p2)


ptlist = Point.point_list()

endpoints = [pt in ptlist if len(pt.segset)==1]

if len(endpoints) == 0:
    closed = True
    basept = ptlist[0]
    endpt = ptlist[-1]
else:
    closed = False
    basept = endpoints[0]
    endpt = endpoints[1]


newlist = []

while True:
    newlist.append(basept)
    theseg = list(basept.segset)[0]
    nextpt = otherend(basept, theseg)
    if nextpt == endpt:
        break
    basept = nextpt
newlist.append(endpt)

for i in newlist:
    v = i.val
    print(v[0], v[1], v[2])


    
    



