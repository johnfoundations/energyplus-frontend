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
from dimensionwidget import *
import projectwidget
from lineroutines import *
import floorlisttab
import zonelisttab



class zoneTab(projectwidget.projectWidget):
  def __init__(self, parent=None):
    projectwidget.projectWidget.__init__(self, parent)
    
    hlayout = QtGui.QHBoxLayout(self)
    self.bdpscene = dimensionscene.shapeDimension('')
    vl = QtGui.QVBoxLayout()
    self.lroutines = lineRoutines(self.bdpscene.scene)
    vl.addWidget(self.bdpscene)
    hlayout.addLayout(vl)
    
    layout = QtGui.QVBoxLayout()
    layout.addWidget(QtGui.QLabel('Zoning Details'))
    self.tabs = QtGui.QTabWidget()
    self.floortab = floorlisttab.floorListTab(self.bdpscene)
    self.zonetab = zonelisttab.zoneListTab(self.bdpscene)
    self.tabs.addTab(self.floortab,'Floors')
    self.tabs.addTab(self.zonetab,'Zones')
    layout.addWidget(self.tabs)
    self.floorarray = []
    self.zonearray = dict()
    self.currentfloor = ''
    self.currentsegmentlist = []
    self.segmentarray = dict()



    hlayout.addLayout(layout)
    self.colorindex = 0
    self.colorlist = []
    self.proposed = []
  






  def windowtab(self):
   widget - QtGui.QVBoxLayout()
    
    
  


        
  def indpointtopoint(self):
    s = self.indpoint.text()
    ps = s.split(',')
    t0 = 0.0
    t1 = 0.0
    try:
      t0 = float(ps[0])
      t1 = float(ps[1])
    except:
      print 'point is not valid'
    return [t0,t1]

  def idftoscenepolygon(self,l):
    #first point is origin. idf y is up, scene y is down
    ll = []
    for items in l:
      ll.append([items[0],-items[1]])
    return ll
    
  def idftoscene(self,l):
    ll = l[:]
    ll[0] = [ll[0][0],-ll[0][1]]
    return ll

  def seglinetosceneline(self,l):
    #l is relative array
    #takes last two items in l and returns point and offset
    print 'seglinetosceneline'
    print l
    s = relativetoabsolute(l)
    return [s[-2],l[-1]]

      
  def pointtosegoffset(self,l,p):
    #returns point, last in l and offset to p
    print 'pointtosegoffset'
    print l
    s = [0.0,0.0]
    for item in l:
      s[0] = s[0]+item[0]
      s[1] = s[1]-item[1]
    print s
    #s is point
    return [s,p[0]-s[0],p[1]+s[1]]

  def relativetoabsolute(self,l):
    #l[0] is absolute, all else relative to it
    ll = []
    lw = l[:]
    p = lw.pop(0)
    ll.append(p)
    for pt in lw:
      tp = [[p[0][0]+pt[0][0],p[0][1]+pt[0][1]],[p[1][0]+pt[1][0],p[1][1]+pt[1][1]]]
      ll.append(tp)
      p = tp

    return ll
    
  def absolutetorelative(self,l):
    ll = []
    lw = l[:]
    p = lw.pot(0)
    ll.append(p)
    for pt in lw:
      tp = [[p[0][0]-pt[0][0],p[0][1]-pt[0][1]],[p[1][0]-pt[1][0],p[1][1]-pt[1][1]]]
      ll.append(tp)
      p = pt

    return ll
 


  def buildSegmentStr(self,l):
    s = ""
    for seg in l:#self.currentsegmentlist:
      s = s + str(seg) + ','
    return s



  def updateProject(self):
    r = self.projectlink.getOutlineArray()
    print r
    self.currentsegmentlist = r[:]
    self.bdpscene.drawShape(r)
    
    
  def getColor(self):
    if len(self.colorlist) == 0:
      self.colorlist = [QtGui.Qt.red, QtGui.Qt.darkRed, QtGui.Qt.green, QtGui.Qt.darkGreen, QtGui.Qt.blue, QtGui.Qt.darkBlue, QtGui.Qt.cyan, QtGui.Qt.darkCyan, QtGui.Qt.magenta, QtGui.Qt.darkMagenta, QtGui.Qt.yellow, QtGui.Qt.darkYellow, QtGui.Qt.gray, QtGui.Qt.darkGray, QtGui.Qt.lightGray]
    i = self.colorindex
    self.colorindex = self.colorindex + 1
    return self.colorlist[i]

def set_qtrace():
  from PyQt4 import QtCore
  QtCore.pyqtRemoveInputHook()
  import pdb
  pdb.set_trace()

def out_qtrace():
  from PyQt4 import QtCore
  QtCore.pyqtRestoreInputHook()
    
#if __name__ == "__main__":
  