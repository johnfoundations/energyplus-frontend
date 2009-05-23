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
import dimensionscene
import projectwidget
from lineroutines import *



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
    
    hhlayout = QtGui.QHBoxLayout()
    self.floorname = QtGui.QLineEdit()
    hhlayout.addWidget(QtGui.QLabel('Enter Floor Name:'))
    hhlayout.addWidget(self.floorname)
    layout.addLayout(hhlayout)
    
    self.floornamebutton = QtGui.QPushButton('Add F&loor')
    layout.addWidget(self.floornamebutton)
    self.floorlist = QtGui.QComboBox()
    layout.addWidget(self.floorlist)
    self.zonegroupbox = QtGui.QGroupBox('Floor Details')
    zonegblayout = QtGui.QVBoxLayout()
    hhlayout = QtGui.QHBoxLayout()
    hhlayout.addWidget(QtGui.QLabel('Enter Zone Name:'))
    self.zonename = QtGui.QLineEdit()
    hhlayout.addWidget(self.zonename)
    zonegblayout.addLayout(hhlayout)
    self.zonenamebutton = QtGui.QPushButton('Add &Zone')
    zonegblayout.addWidget(self.zonenamebutton)
    self.zonelist = QtGui.QComboBox()
    zonegblayout.addWidget(self.zonelist)
    self.zonegroupbox.setLayout(zonegblayout)
    layout.addWidget(self.zonegroupbox)
    self.tabs = QtGui.QTabWidget()
    self.tabs.addTab(self.dimensiontab(),'Dimensions')
    layout.addWidget(self.tabs)
    self.floorarray = []
    self.zonearray = dict()
    self.currentfloor = ''
    self.currentsegmentlist = []
    self.segmentarray = dict()
    self.connect(self.floornamebutton, QtCore.SIGNAL('clicked ( bool)'),self.floornamebuttonclicked)
    self.connect(self.zonenamebutton, QtCore.SIGNAL('clicked ( bool)'),self.zonenamebuttonclicked)
    self.connect(self.floorlist,QtCore.SIGNAL('currentIndexChanged (int)'),self.floorlistchanged)
    self.connect(self.zonelist,QtCore.SIGNAL('currentIndexChanged (int)'),self.zonelistchanged)

    hlayout.addLayout(layout)
    self.colorindex = 0
    self.colorlist = []
    self.proposed = []
  

  def dimensiontab(self):
    widget = QtGui.QWidget()
    lseglayout = QtGui.QVBoxLayout()
    self.linesegments = QtGui.QLineEdit()
    lseglayout.addWidget(self.linesegments)
    hhlayout = QtGui.QHBoxLayout()
    self.backsegmentbutton = QtGui.QPushButton('<--')
    self.backsegmentbutton.setEnabled(False)
    self.indpoint = QtGui.QLineEdit()
    rx = QtCore.QRegExp('-*[0-9]*\.[0-9]*,-*[0-9]*\.[0-9]*')
    self.indpoint.setValidator(QtGui.QRegExpValidator(rx,self.indpoint))
    hhlayout.addWidget(self.backsegmentbutton)
    hhlayout.addWidget(self.indpoint)
    hhlayout.addStretch()
    lseglayout.addLayout(hhlayout)
    self.upsegmentbutton = QtGui.QPushButton('^')
    self.upsegmentbutton.setShortcut(QtGui.QKeySequence("Alt+Up"))
    self.downsegmentbutton = QtGui.QPushButton('\/')
    self.downsegmentbutton.setShortcut(QtGui.QKeySequence("Alt+Down"))
    self.leftsegmentbutton = QtGui.QPushButton('<')
    self.leftsegmentbutton.setShortcut(QtGui.QKeySequence("Alt+Left"))
    self.rightsegmentbutton= QtGui.QPushButton('>')
    self.rightsegmentbutton.setShortcut(QtGui.QKeySequence("Alt+Right"))
    self.addsegmentbutton = QtGui.QPushButton('*')
    self.addsegmentbutton.setShortcut(QtGui.QKeySequence("Alt+."))
    self.leftsegmentbutton.setEnabled(False)
    self.rightsegmentbutton.setEnabled(False)
    self.upsegmentbutton.setEnabled(False)
    self.downsegmentbutton.setEnabled(False)
    hhlayout = QtGui.QHBoxLayout()
    hhlayout.addStretch()
    hhlayout.addWidget(self.upsegmentbutton)
    hhlayout.addStretch()
    lseglayout.addLayout(hhlayout)
    hhlayout = QtGui.QHBoxLayout()
    hhlayout.addStretch()
    hhlayout.addWidget(self.leftsegmentbutton)
    hhlayout.addWidget(self.addsegmentbutton)
    hhlayout.addWidget(self.rightsegmentbutton)
    hhlayout.addStretch()
    lseglayout.addLayout(hhlayout)
    hhlayout = QtGui.QHBoxLayout()
    hhlayout.addStretch()
    hhlayout.addWidget(self.downsegmentbutton)
    hhlayout.addStretch()
    lseglayout.addLayout(hhlayout)
    lseglayout.addStretch()
    self.connect(self.backsegmentbutton, QtCore.SIGNAL('clicked ( bool)'),self.backsegmentbuttonclicked)
    self.connect(self.addsegmentbutton, QtCore.SIGNAL('clicked(bool)'), self.addsegmentbuttonclicked)
    self.connect(self.leftsegmentbutton, QtCore.SIGNAL('clicked(bool)'), self.leftsegmentbuttonclicked)
    self.connect(self.rightsegmentbutton, QtCore.SIGNAL('clicked(bool)'), self.rightsegmentbuttonclicked)
    self.connect(self.upsegmentbutton, QtCore.SIGNAL('clicked(bool)'), self.upsegmentbuttonclicked)
    self.connect(self.downsegmentbutton, QtCore.SIGNAL('clicked(bool)'), self.downsegmentbuttonclicked)
    
    widget.setLayout(lseglayout)
    return widget

  def windowtab(self):
   widget - QtGui.QVBoxLayout()
    
    
  def floornamebuttonclicked(self):
    print 'floornamebutton'
    if not self.floorname.text() == '':
      self.floorarray.append(self.floorname.text())
      self.floorlist.addItem(self.floorname.text())
      self.zonearray[str(self.floorname.text())] = []
      if len(self.segmentarray) == 0:
        self.segmentarray[str(self.floorname.text())] = self.currentsegmentlist
      else:
        self.segmentarray[str(self.floorname.text())] = []
      self.floorname.setText('')

  def zonenamebuttonclicked(self):
    print 'zonenamebutton'
    if not self.zonename.text() == '':
      print self.zonearray
      print self.currentfloor
      self.zonearray[self.currentfloor].append(str(self.zonename.text()))
      self.zonelist.addItem(self.zonename.text())
      self.zonename.setText('')

  def backsegmentbuttonclicked(self):
    print 'backsegmentbuttonclicked'
    self.currentsegmentlist.pop()
    self.segmentarray[self.floorzone] = self.currentsegmentlist[:]
    self.bdpscene.clearLastLineSegment()
    if len(self.currentsegmentlist) == 0:
      self.leftsegmentbutton.setEnabled(False)
    self.linesegments.setText(self.buildSegmentStr())

  def addsegmentbuttonclicked(self):
    print 'addsegmentbuttonclicked'
    if len(self.proposed) > 0:
      self.bdpscene.clearLastLineSegment()
      self.proposed = []
    s = self.linesegments.text()
    self.linesegments.setText(self.linesegments.text()+ ', ' + self.indpoint.text())
    ps = self.indpointtopoint()
    self.currentsegmentlist.append(ps)
    print self.floorzone
    self.segmentarray[self.floorzone] = self.currentsegmentlist[:]
    self.indpoint.setText('')
    if not s == '':
      self.bdpscene.drawLineSegments(self.seglinetosceneline(self.currentsegmentlist),0)
    if len(self.currentsegmentlist) > 0:
      self.backsegmentbutton.setEnabled(True)
      self.leftsegmentbutton.setEnabled(True)
      self.rightsegmentbutton.setEnabled(True)
      self.upsegmentbutton.setEnabled(True)
      self.downsegmentbutton.setEnabled(True)
      
  def leftsegmentbuttonclicked(self):
    print 'leftsegmentbuttonclicked'
    if len(self.proposed) > 0:
      self.bdpscene.clearLastLineSegment()
      self.proposed = []
    p = self.currentsegmentlist[-1]
    closest = self.lroutines.intersectLeft(p,self.currentsegmentlist)
    print closest
    if closest == None:
      closest = [-10.0,0.0]
    else:
      closest = self.pointtosegoffset(self.currentsegmentlist,closest)
    self.proposed =  closest
    self.indpoint.setText(str(closest[0])+','+str(closest[1]))
    l = [p,closest]
    self.bdpscene.drawLineSegments(l,0)

  def rightsegmentbuttonclicked(self):
    print 'rightsegmentbuttonclicked'
    if len(self.proposed) > 0:
      self.bdpscene.clearLastLineSegment()
      self.proposed = []
    p = self.currentsegmentlist[-1]
    closest = self.lroutines.intersectRight(p,self.currentsegmentlist)
    print closest
    if closest == None:
      closest = [10.0,0.0]
    else:
      closest = self.pointtosegoffset(self.currentsegmentlist,closest)
    self.proposed =  closest
    self.indpoint.setText(str(closest[0])+','+str(closest[1]))
    l = [p,closest]
    self.bdpscene.drawLineSegments(l,0)
        
  def upsegmentbuttonclicked(self):
    print 'upsegmentbuttonclicked'
    if len(self.proposed) > 0:
      self.bdpscene.clearLastLineSegment()
      self.proposed = []
    p = self.currentsegmentlist[-1]
    closest = self.lroutines.intersectUp(p,self.currentsegmentlist)
    print closest
    if closest == None:
      closest = [0.0,-10.0]
    else:
      closest = self.pointtosegoffset(self.currentsegmentlist,closest)
    self.proposed =  closest
    self.indpoint.setText(str(closest[0])+','+str(closest[1]))
    l = [p,closest]
    self.bdpscene.drawLineSegments(l,0)
        

  def downsegmentbuttonclicked(self):
    print 'downsegmentbuttonclicked'
    if len(self.proposed) > 0:
      self.bdpscene.clearLastLineSegment()
      self.proposed = []
    p = self.currentsegmentlist[-1]
    closest = self.lroutines.intersectDown(p,self.currentsegmentlist)
    print closest
    if closest == None:
      closest = [0.0,10.0]
    else:
      closest = self.pointtosegoffset(self.currentsegmentlist,closest)
    self.proposed =  closest
    self.indpoint.setText(str(closest[0])+','+str(closest[1]))
    l = [p,closest]
    self.bdpscene.drawLineSegments(l,0)

        
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
    #takes last two items in l and returns point and offset
    print l
    s = [0.0,0.0]
    for item in l:
      s[0] = s[0]+item[0]
      s[1] = s[1]-item[1]
    print s
    s[0] = s[0] - l[-1][0]
    s[1] = s[1] + l[-1][1]
    print s
    return [s,[l[-1][0],-l[-1][1]]]
      
  def pointtosegoffset(self,l,p):
    #returns point, last in l and offset to p
    print l
    s = [0.0,0.0]
    for item in l:
      s[0] = s[0]+item[0]
      s[1] = s[1]-item[1]
    print s
    #s is point
    return [s,p[0]-s[0],p[1]+s[1]]

  def floorlistchanged(self,i):
    print 'floorlistchanged'
    print i
    s = self.floorlist.itemText(i)
    self.zonegroupbox.setTitle(s + ' Zones and Details')
    self.currentfloor = str(s)
    self.zonelist.clear()
    if self.currentfloor in self.zonearray:
      self.zonelist.addItems(self.zonearray[self.currentfloor])
    if len(self.zonearray) == 0:
      self.floorzone = self.currentfloor

  def buildSegmentStr(self):
    s = ""
    for seg in self.currentsegmentlist:
      s = s + str(seg) + ','
    return s


  def zonelistchanged(self,i):
    print 'zonelistchanged'
    print self.segmentarray
    #update segments
    self.floorzone = self.currentfloor+':'+str(self.zonelist.itemText(i))
    print self.floorzone
    if self.floorzone in self.segmentarray:
      self.currentsegmentlist = self.segmentarray[self.floorzone]
    else:
      self.currentsegmentlist = []
    self.linesegments.setText(self.buildSegmentStr())

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


    
