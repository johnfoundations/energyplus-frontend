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

from PyQt4 import QtGui, QtCore
import sys


class shapeDimension(QtGui.QWidget):
  def __init__(self,shape, parent=None):
    QtGui.QWidget.__init__(self,parent)
    #shape from projectwizard.py
    self.scene = QtGui.QGraphicsScene()
    self.view = QtGui.QGraphicsView(self.scene)
    self.layout = QtGui.QVBoxLayout()
    self.layout.addWidget(self.view)
    self.createDict()

  def drawShape(self,shape):
    s = QtCore.QPointF(0,0)
    e = QtCore.QPointF(0,0)
    for p in self.points[shape]:
      e.setX(e.x()+p[0])
      e.setY(e.y()+p[1])
      self.scene.addLine(QtCore.QLineF(s,e))
      s.setX(e.x())
      s.setY(e.y())

    for p in self.edit[shape]:
      l = self.scene.addText('0')
      l.moveBy(p[0],p[1])
      #l.setTextInteractionFlags(QtCore.TextEditable)
      self.measures.append(l)

    arrow = QtGui.QPolygonF()
    arrow.append(QtCore.QPointF(-100,-60))
    arrow.append(QtCore.QPointF(-95,-50))
    arrow.append(QtCore.QPointF(-105,-50))
    arrow.append(QtCore.QPointF(-100,-60))
    arrow.append(QtCore.QPointF(-100,-20))
    self.scene.addPolygon(arrow)
    n = QtGui.QPolygonF()
    n.append(QtCore.QPointF(-104,-45))
    n.append(QtCore.QPointF(-104,-35))
    n.append(QtCore.QPointF(-104,-45))
    n.append(QtCore.QPointF(-96,-35))
    n.append(QtCore.QPointF(-96,-45))
    n.append(QtCore.QPointF(-96,-35))
    self.scene.addPolygon(n)
    self.setLayout(self.layout)


  def createDict(self):
    self.points = dict()
    self.points['L'] =   [[0,100],[100,0],[0,-50],[-50,0],[0,-50],[-50,0]]
    self.points['L90'] = [[0,100],[50,0],[0,-50],[50,0],[0,-50],[-100,0]]
    self.points['L180']= [[0,50],[50,0],[0,50],[50,0],[0,-100],[-100,0]]
    self.points['L270']= [[0,50],[-50,0],[0,50],[100,0],[0,-100],[-50,0]]
    self.points['H']  = [[0,99],[33,0],[0,-33],[33,0],[0,33],[33,0],[0,-99],[-33,0],[0,33],[-33,0],[0,-33],[-33,0]]
    self.points['H90']  = [[0,33],[33,0],[0,33],[-33,0],[0,33],[99,0],[0,-33],[-33,0],[0,-33],[33,0],[0,-33],[-99,0]]
    self.points['T']  = [[0,50],[33,0],[0,50],[33,0],[0,-50],[33,0],[0,-50],[-99,0]]
    self.points['T90']  = [[0,33],[-50,0],[0,33],[50,0],[0,33],[50,0],[0,-99],[-50,0]]
    self.points['T180']  = [[0,50],[-33,0],[0,50],[99,0],[0,-50],[-33,0],[0,-50],[-33,0]]
    self.points['T270']  = [[0,99],[50,0],[0,-33],[50,0],[0,-33],[-50,0],[0,-33],[-50,0]]
    self.points['U']  = [[0,100],[99,0],[0,-100],[-33,0],[0,50],[-33,0],[0,-50],[-33,0]]
    self.points['U90']  = [[0,99],[100,0],[0,-33],[-50,0],[0,-33],[50,0],[0,-33],[-100,0]]
    self.points['U180']  = [[0,100],[33,0],[0,-50],[33,0],[0,50],[33,0],[0,-100],[-99,0]]
    self.points['U270']  = [[0,33],[50,0],[0,33],[-50,0],[0,33],[100,0],[0,-99],[-100,0]]

    self.edit = dict()
    self.edit['L']     = [[20,-15],[105,75],[50,105],[-5,50]]
    self.edit['L90']   = []
    self.edit['L180']  = []
    self.edit['L270']= []
    self.edit['H']= []
    self.edit['H90']= []
    self.edit['T']= []
    self.edit['T90']= []
    self.edit['T180']= []
    self.edit['T270']= []
    self.edit['U']= []
    self.edit['U90']= []
    self.edit['U180']= []
    self.edit['U270']= []

    self.measures = []







