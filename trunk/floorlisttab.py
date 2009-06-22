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

class floorListTab(QtGui.QWidget):
  def __init__(self,scene,parent=None):
    QtGui.QWidget.__init__(self,parent)
    self.scene = scene
    flayout = QtGui.QVBoxLayout()
    hhlayout = QtGui.QHBoxLayout()
    self.floorname = QtGui.QLineEdit()
    hhlayout.addWidget(QtGui.QLabel('Enter Floor Name:'))
    hhlayout.addWidget(self.floorname)
    self.floornamebutton = QtGui.QPushButton('Add F&loor')
    hhlayout.addWidget(self.floornamebutton)
    flayout.addLayout(hhlayout)
    self.floorlist = QtGui.QComboBox()
    flayout.addWidget(self.floorlist)
    self.dimensions = dimensionwidget.dimensionWidget(scene)
    flayout.addWidget(self.dimensions)
    flayout.addStretch()
    self.setLayout(flayout)
    self.connect(self.floornamebutton, QtCore.SIGNAL('clicked ( bool)'),self.floornamebuttonclicked)
    self.connect(self.floorlist,QtCore.SIGNAL('currentIndexChanged (int)'),self.floorlistchanged)


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
    self.zonenamebutton.setEnabled(True)
    self.zonelist.setEnabled(True)
    self.zonename.setEnabled(True)
    self.addsegmentbutton.setEnabled(True)
    self.indpoint.setEnabled(True)


  def floorlistchanged(self,i):
    print 'floorlistchanged'
    print i
    s = self.floorlist.itemText(i)
    self.dimensiontitle.setText(s + ' outline')
    self.currentfloor = str(s)
    self.zonelist.clear()
    if self.currentfloor in self.zonearray:
      self.zonelist.addItems(self.zonearray[self.currentfloor])
    self.linesegments
    if len(self.zonearray) == 0:
      self.floorzone = self.currentfloor
      self.dimensiontitle.setText(self.floorzone)
      