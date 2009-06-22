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


class dimensionWidget(QtGui.QWidget):
  def __init__(self,scene,parent=None):
    QtGui.QWidget.__init__(self,parent)
    self.scene = scene
    lseglayout = QtGui.QVBoxLayout()
    self.dimensiontitle = QtGui.QLabel('Floor:Zone')
    lseglayout.addWidget(self.dimensiontitle)
    self.linesegments = QtGui.QLineEdit()
    self.linesegments.setReadOnly(True)
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
    self.addsegmentbutton.setEnabled(False)
    self.leftsegmentbutton.setEnabled(False)
    self.rightsegmentbutton.setEnabled(False)
    self.upsegmentbutton.setEnabled(False)
    self.downsegmentbutton.setEnabled(False)
    self.indpoint.setEnabled(False)
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
    #    lseglayout.addStretch()
    self.connect(self.backsegmentbutton, QtCore.SIGNAL('clicked ( bool)'),self.backsegmentbuttonclicked)
    self.connect(self.addsegmentbutton, QtCore.SIGNAL('clicked(bool)'), self.addsegmentbuttonclicked)
    self.connect(self.leftsegmentbutton, QtCore.SIGNAL('clicked(bool)'), self.leftsegmentbuttonclicked)
    self.connect(self.rightsegmentbutton, QtCore.SIGNAL('clicked(bool)'), self.rightsegmentbuttonclicked)
    self.connect(self.upsegmentbutton, QtCore.SIGNAL('clicked(bool)'), self.upsegmentbuttonclicked)
    self.connect(self.downsegmentbutton, QtCore.SIGNAL('clicked(bool)'), self.downsegmentbuttonclicked)

    self.setLayout(lseglayout)
    
  def backsegmentbuttonclicked(self):
    print 'backsegmentbuttonclicked'
    self.currentsegmentlist.pop()
    self.segmentarray[self.floorzone] = self.currentsegmentlist[:]
    self.bdpscene.clearLastLineSegment(self.floorzone)
    if len(self.currentsegmentlist) == 0:
      self.leftsegmentbutton.setEnabled(False)
    self.linesegments.setText(self.buildSegmentStr())
      
  def addsegmentbuttonclicked(self):
    print 'addsegmentbuttonclicked'
    if len(self.proposed) > 0:
      self.bdpscene.clearLastLineSegment(self.floorzone)
      self.proposed = []
    s = self.linesegments.text()
    self.linesegments.setText(self.linesegments.text()+ ', ' + self.indpoint.text())
    ps = self.indpointtopoint()
    self.currentsegmentlist.append(ps)
    self.segmentarray[self.floorzone] = self.currentsegmentlist[:]
    self.indpoint.setText('')
    if not s == '':
      self.bdpscene.drawLineSegments(self.seglinetosceneline(self.currentsegmentlist),0,self.floorzone)
    self.bdpscene.drawLineSegmentDimensions(self.floorzone)
    if len(self.currentsegmentlist) > 0:
      self.backsegmentbutton.setEnabled(True)
      self.leftsegmentbutton.setEnabled(True)
      self.rightsegmentbutton.setEnabled(True)
      self.upsegmentbutton.setEnabled(True)
      self.downsegmentbutton.setEnabled(True)
          
  def leftsegmentbuttonclicked(self):
    print 'leftsegmentbuttonclicked'
    if len(self.proposed) > 0:
      self.bdpscene.clearLastLineSegment(self.floorzone)
      self.proposed = []
    p = self.currentsegmentlist[-1]
    closest = self.lroutines.intersectLeft(p,self.currentsegmentlist)
    if closest == None:
      closest = [-10.0,0.0]
    else:
      closest = self.pointtosegoffset(self.currentsegmentlist,closest)
    self.proposed =  closest
    self.indpoint.setText(str(closest[0])+','+str(-closest[1]))
    l = [p,closest]
    self.bdpscene.drawLineSegments(l,0,self.floorzone)
                      
  def rightsegmentbuttonclicked(self):
    print 'rightsegmentbuttonclicked'
    if len(self.proposed) > 0:
      self.bdpscene.clearLastLineSegment(self.floorzone)
      self.proposed = []
    p = self.currentsegmentlist[-1]
    closest = self.lroutines.intersectRight(p,self.currentsegmentlist)
    if closest == None:
      closest = [10.0,0.0]
    else:
      closest = self.pointtosegoffset(self.currentsegmentlist,closest)
    self.proposed =  closest
    self.indpoint.setText(str(closest[0])+','+str(-closest[1]))
    l = [p,closest]
    self.bdpscene.drawLineSegments(l,0,self.floorzone)
                              
  def upsegmentbuttonclicked(self):
    print 'upsegmentbuttonclicked'
    if len(self.proposed) > 0:
      self.bdpscene.clearLastLineSegment(self.floorzone)
      self.proposed = []
    p = self.currentsegmentlist[-1]
    closest = self.lroutines.intersectUp(p,self.currentsegmentlist)
    if closest == None:
      closest = [0.0,-10.0]
    else:
      closest = self.pointtosegoffset(self.currentsegmentlist,closest)
    self.proposed =  closest
    self.indpoint.setText(str(closest[0])+','+str(-closest[1]))
    l = [p,closest]
    self.bdpscene.drawLineSegments(l,0,self.floorzone)
                                      
                                      
  def downsegmentbuttonclicked(self):
    print 'downsegmentbuttonclicked'
    if len(self.proposed) > 0:
      self.bdpscene.clearLastLineSegment(self.floorzone)
      self.proposed = []
    p = self.currentsegmentlist[-1]
    closest = self.lroutines.intersectDown(p,self.currentsegmentlist)
    if closest == None:
      closest = [0.0,10.0]
    else:
      closest = self.pointtosegoffset(self.currentsegmentlist,closest)
    self.proposed =  closest
    self.indpoint.setText(str(closest[0])+','+str(-closest[1]))
    l = [p,closest]
    self.bdpscene.drawLineSegments(l,0,self.floorzone)
                                              
                                              