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
    self.layout = QtGui.QVBoxLayout(self)
    self.layout.addWidget(self.view)
    self.createDict()
    self.setLayout(self.layout)
    self.polygonlist = dict()
    self.zoom = 2.0
    self.createActions()
    self.linesegments = dict()
    self.rescale()
    
  def createActions(self):
    self.zoomin = QtGui.QAction('Zoom In', self)
    self.zoomin.setStatusTip('Zoom In')
    self.connect(self.zoomin, QtCore.SIGNAL('triggered()'), self.zoominslot)
    self.zoomout = QtGui.QAction('Zoom Out', self)
    self.zoomout.setStatusTip('Zoom Out')
    self.connect(self.zoomout, QtCore.SIGNAL('triggered()'), self.zoomoutslot)

  def zoominslot(self):
    print 'zoominslot'
    self.zoom = self.zoom + 0.5
    self.rescale()
    
  def zoomoutslot(self):
    print 'zoomoutslot'
    self.zoom = self.zoom - 0.5
    self.rescale()

  def rescale(self):
    print 'rescale'
    print self.zoom
    oldMatrix = self.view.matrix();
    self.view.resetMatrix();
    self.view.translate(oldMatrix.dx(), oldMatrix.dy())
    self.view.scale(self.zoom,self.zoom);

  def contextMenuEvent (self,context ):
    print 'contextMenuEvent'
    menu = QtGui.QMenu()
    menu.addAction(self.zoomin)
    menu.addAction(self.zoomout)
    menu.exec_(context.pos())
    




  def drawShape(self,shape):
    print shape
    s = QtCore.QPointF(0,0)
    e = QtCore.QPointF(0,0)
    for p in shape:
      e.setX(e.x()+p[0])
      e.setY(e.y()+p[1])
      self.scene.addLine(QtCore.QLineF(s,e))
      s.setX(e.x())
      s.setY(e.y())

  def drawLineSegments(self,line,color,name):
    print 'drawLineSegments'
    print line
    if not name in self.linesegments:
      self.linesegments[name] = []
    lline = line[:]
    lline.pop(0)
    s = QtCore.QPointF(line[0][0],line[0][1])
    e = QtCore.QPointF(line[0][0],line[0][1])
    print e
    print s
    for p in lline:
      e.setX(e.x()+p[0])
      e.setY(e.y()+p[1])
      self.linesegments[name].append(self.scene.addLine(QtCore.QLineF(s,e)))
      s.setX(e.x())
      s.setY(e.y())

  def drawLineSegmentDimensions(self,name):
    return
    rect = self.scene.itemsBoundingRect()
    if not name in self.linesegments:
      return
    p1 = []
    for p2 in self.linesegments[name]:
      if len(p1) == 0:
        p1 = p2
        s = str(p2.line().x1()) + ',' + str(p2.line().y1())
        print s
        dt = self.scene.addSimpleText(s)
        print dt
        dt.moveBy(p2.line().x1(),p2.line().y1())
        continue
      
      

  def clearLineSegments(self,name):
    if name in self.linesegments:
      for l in self.linesegments[name]:
        self.scene.removeItem(l)

  def clearLastLineSegment(self,name):
    if name in self.linesegments:
      l = self.linesegments[name].pop()
      self.scene.removeItem(l)


  def drawPolygon(self,points,name):
    print points
    print name
    s = QtCore.QPointF(spoints[0][0],points[0][1])
    e = QtCore.QPointF(spoints[0][0],points[0][1])
    print e
    print s
    poly = QtGui.QPolygonF()
    poly.append(s)
    for p in points:
      e.setX(e.x()+p[0])
      e.setY(e.y()+p[1])
      poly.append(e)
      s.setX(e.x())
      s.setY(e.y())
    pen = QtGui.QPen()
    pen.setWidth(4)
    if name in self.polygonlist:
      self.polygonlist[name].setPolygon(poly)
      self.polygonlist[name].setPen(pen)
    else:
      self.polygonlist[name] = self.scene.addPolygon(poly,pen)
      

  def drawDimensionEdit(self,shape):
    for p in self.edit[shape]:
      l = self.scene.addText('_')
      l.moveBy(p[0],p[1])
      l.setTextInteractionFlags(QtCore.Qt.TextEditable)
      self.measures.append(l)

  def drawNorthArrow(self):
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
   


  def drawPredefinedShape(self,pre):
    self.drawShape(self.points[pre])
    self.drawDimensionEdit(pre)
    self.drawNorthArrow()
  
  
  

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
    self.edit['L']     = [[45,100],[100,65],[15,-25],[-15,45]]
    self.edit['L90']   = [[15,100],[100,15],[45,-25],[-15,45]]
    self.edit['L180']  = [[65,100],[100,45],[45,-25],[-15,15]]
    self.edit['L270']  = [[-5,100],[50,45],[15,-25],[-65,65]]
    self.edit['H']     = [[5,100],[38,100],[71,100],[100,80],[100,40],[100,10]]
    self.edit['H90']   = [[5,100],[38,100],[71,100],[100,80],[100,40],[100,10]]
    self.edit['T']     = [[5,100],[38,100],[71,100],[100,65],[100,15]]
    self.edit['T90']   = [[15,100],[65,100],[100,80],[100,40],[100,10]]
    self.edit['T180']  = [[5,100],[38,100],[71,100],[100,65],[100,15]]
    self.edit['T270']  = [[15,100],[65,100],[100,80],[100,40],[100,10]]
    self.edit['U']     = [[5,100],[38,100],[71,100],[100,65],[100,15]]
    self.edit['U90']   = [[15,100],[65,100],[100,80],[100,40],[100,10]]
    self.edit['U180']  = [[5,100],[38,100],[71,100],[100,65],[100,15]]
    self.edit['U270']  = [[15,100],[65,100],[100,80],[100,40],[100,10]]

    self.zone = dict()
    self.zone['L']     = []
    self.zone['L90']   = [[15,100],[100,15],[45,-25],[-15,45]]
    self.zone['L180']  = [[65,100],[100,45],[45,-25],[-15,15]]
    self.zone['L270']  = [[-5,100],[50,45],[15,-25],[-65,65]]
    self.zone['H']     = [[5,100],[38,100],[71,100],[100,80],[100,40],[100,10]]
    self.zone['H90']   = [[5,100],[38,100],[71,100],[100,80],[100,40],[100,10]]
    self.zone['T']     = [[5,100],[38,100],[71,100],[100,65],[100,15]]
    self.zone['T90']   = [[15,100],[65,100],[100,80],[100,40],[100,10]]
    self.zone['T180']  = [[5,100],[38,100],[71,100],[100,65],[100,15]]
    self.zone['T270']  = [[15,100],[65,100],[100,80],[100,40],[100,10]]
    self.zone['U']     = [[5,100],[38,100],[71,100],[100,65],[100,15]]
    self.zone['U90']   = [[15,100],[65,100],[100,80],[100,40],[100,10]]
    self.zone['U180']  = [[5,100],[38,100],[71,100],[100,65],[100,15]]
    self.zone['U270']  = [[15,100],[65,100],[100,80],[100,40],[100,10]]
    

    
    self.measures = []

  def getDimensions(self):
    res = []
    for m in self.measures:
      res.append(str(m.toPlainText()))
    return res






