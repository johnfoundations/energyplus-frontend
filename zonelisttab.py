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
import dimensionwidget


class zoneListTab(QtGui.QWidget):
  def __init__(self,scene,parent=None):
    QtGui.QWidget.__init__(self,parent)
    self.scene = scene
    zonegblayout = QtGui.QVBoxLayout()
    hhlayout = QtGui.QHBoxLayout()
    hhlayout.addWidget(QtGui.QLabel('Enter Zone Name:'))
    self.zonename = QtGui.QLineEdit()
    hhlayout.addWidget(self.zonename)
    self.zonenamebutton = QtGui.QPushButton('Add &Zone')
    hhlayout.addWidget(self.zonenamebutton)
    zonegblayout.addLayout(hhlayout)
    self.zonelist = QtGui.QComboBox()
    zonegblayout.addWidget(self.zonelist)
    self.dimensions = dimensionwidget.dimensionWidget(scene)
    zonegblayout.addWidget(self.dimensions)
    zonegblayout.addStretch()
    self.setLayout(zonegblayout)
    self.connect(self.zonenamebutton, QtCore.SIGNAL('clicked ( bool)'),self.zonenamebuttonclicked)
    self.connect(self.zonelist,QtCore.SIGNAL('currentIndexChanged (int)'),self.zonelistchanged)
    self.zonenamebutton.setEnabled(False)
    self.zonelist.setEnabled(False)
    self.zonename.setEnabled(False)

  def zonenamebuttonclicked(self):
    print 'zonenamebutton'
    if not self.zonename.text() == '':
      print self.zonearray
      print self.currentfloor
      self.zonearray[self.currentfloor].append(str(self.zonename.text()))
      self.zonelist.addItem(self.zonename.text())
      self.zonename.setText('')

  def zonelistchanged(self,i):
    print 'zonelistchanged'
    print self.segmentarray
    #update segments
    self.floorzone = self.currentfloor+':'+str(self.zonelist.itemText(i))
    self.dimensiontitle.setText(self.floorzone)
    print self.floorzone
    if self.floorzone in self.segmentarray:
      self.currentsegmentlist = self.segmentarray[self.floorzone]
    else:
      self.currentsegmentlist = []
    self.linesegments.setText(self.buildSegmentStr())
    

      
      