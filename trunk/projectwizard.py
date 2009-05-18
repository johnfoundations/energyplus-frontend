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
from dimensionscene import *
import idfread

class projectwizard(QtGui.QWizard):
  def __init__(self,parent=0,fl=0):
    QtGui.QWizard.__init__(self)
    self.addPage(self.createInitialPage())
    self.addPage(self.createProjectDetailsPage())
    self.addPage(self.createBuildingTemplatePage())
    self.bdp = self.addPage(self.createBuildingDimensionPage())
    self.addPage(self.createDefaultDetailPage())

  def getData(self):
    #returns dict with names and arrays of values
    results = dict()
    results['Name'] = str(self.projectname.text())
    results['Details'] = str(self.projectdetails.toPlainText())
    results['Units'] = str(self.units.currentText())
    results['Shape'] = self.shapefield
    results['Dimensions'] = self.bdpscene.getDimensions()
    results['Wall'] = str(self.defaultwall.currentText())
    results['Window'] = str(self.defaultwindow.currentText())
    return results
    


  def createInitialPage(self):
    page = QtGui.QWizardPage()
    layout = QtGui.QVBoxLayout()
    layout.addWidget(QtGui.QLabel('Click to Select'))
    openbutton = QtGui.QPushButton('Open Existing Project')
    idfbutton  = QtGui.QPushButton('Open Project from IDF file')
    layout.addWidget(openbutton)
    layout.addWidget(idfbutton)
    layout.addWidget(QtGui.QLabel('To Create a New Project, Press Next>'))
    page.setLayout(layout)
    return page








    

  def createProjectDetailsPage(self):
    page = QtGui.QWizardPage()
    layout = QtGui.QVBoxLayout()
    layout.addWidget(QtGui.QLabel('Create a New Simulation'))
    layout.addWidget(QtGui.QLabel('Project Name:'))
    self.projectname = QtGui.QLineEdit()
    layout.addWidget(self.projectname)
    layout.addWidget(QtGui.QLabel('Will create a folder by that name'))
    layout.addWidget(QtGui.QLabel('Project Details: Name, address, etc'))
    self.projectdetails = QtGui.QTextEdit()
    layout.addWidget(self.projectdetails)
    layout.addWidget(QtGui.QLabel('Units:'))
    self.units = QtGui.QComboBox()
    self.units.addItems(['Imperial','Metric'])
    layout.addWidget(self.units)
    page.setLayout(layout)
    return page

  def createBuildingTemplatePage(self):
    page = QtGui.QWizardPage()
    layout = QtGui.QVBoxLayout()
    layout.addWidget(QtGui.QLabel('Select Shape and Orientation of building'))
    hlayout = QtGui.QHBoxLayout()
    self.signalmapper = QtCore.QSignalMapper(self)
    self.connect(self.signalmapper,QtCore.SIGNAL('mapped(int)'),self.templateButton)
    pixlist = ['pixmaps/l-1.png','pixmaps/l-2.png','pixmaps/l-3.png','pixmaps/l-4.png',\
    'pixmaps/h-1.png','pixmaps/h-2.png',\
    'pixmaps/t-1.png','pixmaps/t-2.png','pixmaps/t-3.png','pixmaps/t-4.png',\
    'pixmaps/u-1.png','pixmaps/u-2.png','pixmaps/u-3.png','pixmaps/u-4.png']
    self.shapelist = ['L','L90','L180','L270','H','H90','T','T90','T180','T270','U','U90','U180','U270',]
    layoutL = QtGui.QHBoxLayout()
    layoutH = QtGui.QHBoxLayout()
    layoutT = QtGui.QHBoxLayout()
    layoutU = QtGui.QHBoxLayout()
    for c,p in enumerate(pixlist):
      button = QtGui.QPushButton()
      button.setIcon(QtGui.QIcon(p))
      self.connect(button, QtCore.SIGNAL('clicked ( bool)'),self.signalmapper, QtCore.SLOT('map()'))
      self.signalmapper.setMapping(button,c)
      if c in [0,1,2,3]:
        layoutL.addWidget(button)
      if c in [4,5]:
        layoutH.addWidget(button)
      if c in [6,7,8,9]:
        layoutT.addWidget(button)
      if c in [10,11,12,13]:
        layoutU.addWidget(button)

    layoutL.addStretch()
    layout.addLayout(layoutL)
    layoutH.addStretch()
    layout.addLayout(layoutH)
    layoutT.addStretch()
    layout.addLayout(layoutT)
    layoutU.addStretch()
    layout.addLayout(layoutU)
    self.shapefield = 'L'
    page.setLayout(layout)
    return page
    


  def templateButton(self,i):
    print i
    self.shapefield = self.shapelist[i]

  def createBuildingDimensionPage(self):
    page = QtGui.QWizardPage()
    layout = QtGui.QVBoxLayout()
    layout.addWidget(QtGui.QLabel('Outside Dimensions of Building'))
    self.bdpscene = shapeDimension('L')
    layout.addWidget(self.bdpscene)
    layout.addWidget(QtGui.QLabel('Click on the _ and enter the dimensions of the wall section'))
    page.setLayout(layout)
    return page
    

  def initializePage (self, id):
    if id == self.bdp:
      self.bdpscene.scene.clear()
      self.bdpscene.drawPredefinedShape(self.shapefield)
    QtGui.QWizard.initializePage(self,id)

  def createZoneDetailPage(self):
    page = QtGui.QWizardPage()
    layout = QtGui.QVBoxLayout()
    layout.addWidget(QtGui.QLabel('Zoning Details'))
    hlayout = QtGui.QHBoxLayout()
    self.floorname = QtGui.QLineEdit()
    hlayout.addWidget(QtGui.QLabel('Enter Floor Name:'))
    hlayout.addWidget(self.floorname)
    layout.addLayout(hlayout)
    self.floornamebutton = QtGui.QPushButton('Add Floor')
    layout.addWidget(self.floornamebutton)
    self.floorlist = QtGui.QComboBox()
    layout.addWidget(self.floorlist)
    self.zonegroupbox = QtGui.QGroupBox('Floor Details')
    zonegblayout = QtGui.QVBoxLayout()
    hlayout = QtGui.QHBoxLayout()
    hlayout.addWidget(QtGui.QLabel('Enter Zone Name:'))
    self.zonename = QtGui.QLineEdit()
    hlayout.addWidget(self.zonename)
    zonegblayout.addLayout(hlayout)
    self.zonenamebutton = QtGui.QPushButton('Add Zone')
    zonegblayout.addWidget(self.zonenamebutton)
    self.zonelist = QtGui.QComboBox()
    zonegblayout.addWidget(self.zonelist)
    self.zonegroupbox.setLayout(zonegblayout)
    layout.addWidget(self.zonegroupbox)
    self.floorarray = []
    self.zonearray = dict()
    self.currentfloor = ''
    self.connect(self.floornamebutton, QtCore.SIGNAL('clicked ( bool)'),self.floornamebuttonclicked)
    self.connect(self.zonenamebutton, QtCore.SIGNAL('clicked ( bool)'),self.zonenamebuttonclicked)
    self.connect(self.floorlist,QtCore.SIGNAL('currentIndexChanged (int)'),self.floorlistchanged)
    self.connect(self.zonelist,QtCore.SIGNAL('currentIndexChanged (int)'),self.zonelistchanged)
    page.setLayout(layout)
    return page
    


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

  def createDefaultDetailPage(self):
    page = QtGui.QWizardPage()
    layout = QtGui.QVBoxLayout()
    layout.addWidget(QtGui.QLabel('Construction Default Details'))
    layout.addWidget(QtGui.QLabel('Default Wall Construction'))
    ashraewallidf = idfread.idfRead('/usr/local/EnergyPlus-3-1-0/datasets/ASHRAE_2005_HOF_Materials.idf')
    compositewallidf = idfread.idfRead('/usr/local/EnergyPlus-3-1-0/datasets/CompositeWallConstructions.idf')
    windowidf = idfread.idfRead('/usr/local/EnergyPlus-3-1-0/datasets/WindowConstructs.idf')
    walls = ashraewallidf.getFilteredList('Construction') + compositewallidf.getFilteredList('Construction')
    windows = windowidf.getFilteredList('Construction')
    wallnames = []
    windownames = []
    for w in walls:
      wallnames.append(w.getName())
    for w in windows:
      windownames.append(w.getName())
    self.defaultwall = QtGui.QComboBox()
    self.defaultwall.addItems(wallnames)
    layout.addWidget(self.defaultwall)
    self.defaultwindow = QtGui.QComboBox()
    self.defaultwindow.addItems(windownames)
    layout.addWidget(QtGui.QLabel('Default Window Construction'))
    layout.addWidget(self.defaultwindow)
    page.setLayout(layout)
    return page
    


if __name__ == "__main__":
  app = QtGui.QApplication(sys.argv)
  view = projectwizard()
  view.setWindowTitle("Wizard test")
  view.show()
  sys.exit(app.exec_())
  