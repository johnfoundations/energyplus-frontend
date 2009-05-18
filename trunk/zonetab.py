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



class zoneTab(QtGui.QWidget):
  def __init__(self, parent=None):
    QtGui.QWidget.__init__(self, parent)
    hlayout = QtGui.QHBoxLayout(self)
    self.bdpscene = dimensionscene.shapeDimension('')
    vl = QtGui.QVBoxLayout()
    vl.addWidget(self.bdpscene)
    hlayout.addLayout(vl)
    layout = QtGui.QVBoxLayout()
    layout.addWidget(QtGui.QLabel('Zoning Details'))
    hhlayout = QtGui.QHBoxLayout()
    self.floorname = QtGui.QLineEdit()
    hhlayout.addWidget(QtGui.QLabel('Enter Floor Name:'))
    hhlayout.addWidget(self.floorname)
    layout.addLayout(hhlayout)
    self.floornamebutton = QtGui.QPushButton('Add Floor')
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
    self.zonenamebutton = QtGui.QPushButton('Add Zone')
    zonegblayout.addWidget(self.zonenamebutton)
    self.zonelist = QtGui.QComboBox()
    zonegblayout.addWidget(self.zonelist)
    self.zonegroupbox.setLayout(zonegblayout)
    layout.addWidget(self.zonegroupbox)
    layout.addStretch()
    self.floorarray = []
    self.zonearray = dict()
    self.currentfloor = ''
    self.connect(self.floornamebutton, QtCore.SIGNAL('clicked ( bool)'),self.floornamebuttonclicked)
    self.connect(self.zonenamebutton, QtCore.SIGNAL('clicked ( bool)'),self.zonenamebuttonclicked)
    self.connect(self.floorlist,QtCore.SIGNAL('currentIndexChanged (int)'),self.floorlistchanged)
    self.connect(self.zonelist,QtCore.SIGNAL('currentIndexChanged (int)'),self.zonelistchanged)
    hlayout.addLayout(layout)

    
    
    
  def floornamebuttonclicked(self):
    print 'floornamebutton'
    if not self.floorname.text() == '':
      self.floorarray.append(self.floorname.text())
      self.floorlist.addItem(self.floorname.text())
      self.zonearray[str(self.floorname.text())] = []
      self.floorname.setText('')

  def zonenamebuttonclicked(self):
    print 'zonenamebutton'
    if not self.zonename.text() == '':
      print self.zonearray
      print self.currentfloor
      self.zonearray[self.currentfloor].append(str(self.zonename.text()))
      self.zonelist.addItem(self.zonename.text())
      self.zonename.setText('')



  def floorlistchanged(self,i):
    print 'floorlistchanged'
    print i
    s = self.floorlist.itemText(i)
    self.zonegroupbox.setTitle(s + ' Zones and Details')
    self.currentfloor = str(s)
    self.zonelist.clear()
    self.zonelist.addItems(self.zonearray[self.currentfloor])

  def zonelistchanged(self,i):
    print 'zonelistchanged'
    print i

                