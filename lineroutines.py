# -*- coding: utf-8 -*-
"""***************************************************************************
*   Copyright (C) 2009 by Derek Kite   *
*   dkite@shaw.ca   *
*                                                                         *
*   This program is free software; you can redistribute it and/or modify  *
*   it under the terms of the GNU General Public License as published by  *
*   the Free Software Foundation; either version 2 of the License, or     *
*   (at your option) any later version.                                   *
*                                                                         *
*   This program is distributed in the hope that it will be useful,       *
*   but WITHOUT ANY WARRANTY; without even the implied warranty of        *
*   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the         *
*   GNU General Public License for more details.                          *
*                                                                         *
*   You should have received a copy of the GNU General Public License     *
*   along with this program; if not, write to the                         *
*   Free Software Foundation, Inc.,                                       *
*   59 Temple Place - Suite 330, Boston, MA  02111-1307, USA.             *
***************************************************************************"""

import projectwizard
from PyQt4 import QtGui, QtCore


# line routines, intersections, etc.

class lineRoutines():
  def __init__(self,scene):
    self.scene = scene

  def lineIntersect(self,initialpoint,directionpoint,linelist):
    #targetline is qlinef that you want to check for intersections
    #linelist is first element the origin, every element after the difference to the next point
    targetline = QtCore.QLineF(QtCore.QPointF(initialpoint[0],initialpoint[1]),QtCore.QPointF(directionpoint[0],directionpoint[1]))
    print linelist
    print targetline
    s = QtCore.QPointF(linelist[0][0],linelist[0][1])
    e = QtCore.QPointF(linelist[0][0],linelist[0][1])
    print e
    print s
    intersected = []
    unbounded = []
    for p in linelist:
      e.setX(e.x()+p[0])
      e.setY(e.y()+p[1])
      line =QtCore.QLineF(e,s)
      intersectionpoint = None
      res = targetline.intersect(line,intersectionpoint)
      if res == 1:
        intersected.append(intersectionpoint)
      if res == 2:
        unbounded.append(intersectionpoint)
      s.setX(e.x())
      s.setY(e.y())

    initialpointF = QtCore.QPointF(initialpoint[0],initialpoint[1])
    closestpoint = None
    if len(intersected) > 0:
      for p in intersected:
        if closestpoint == None:
          closestpoint = p
          continue
        if QtCore.QLineF(initialpointF,closestpoint).length() > QtCore.QLineF(initialpointF,p).length():
          if QtCore.QLineF(initialpointF,p).length() > 0:
            closestpoint = p

    if not closestpoint == None:
      return [closestpoint.x(),closestpoint.y()]
    else:
      return None #initialpoint

  def intersectLeft(self,point,linelist):
    rect = self.scene.sceneRect()
    dirpoint = [rect.x()-10,point[1]]
    return self.lineIntersect(point,dirpoint,linelist)

  def intersectRight(self,point,linelist):
    rect = self.scene.sceneRect()
    dirpoint = [rect.x()+rect.width()+10,point[1]]
    return self.lineIntersect(point,dirpoint,linelist)

  def intersectUp(self,point,linelist):
    rect = self.scene.sceneRect()
    dirpoint = [point[0],rect.y()-10]
    return self.lineIntersect(point,dirpoint,linelist)

  def intersectDown(self,point,linelist):
    rect = self.scene.sceneRect()
    dirpoint = [point[0],rect.y()+rect.height()+10]
    return self.lineIntersect(point,dirpoint,linelist)
