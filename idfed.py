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

# File : idfeditor.py
import sys
from PyQt4 import QtGui, QtCore
from gwidget import GWidget
import projecttab
import project
import zonetab


# We start a new class here
# derived from QMainWindow
# A calendar is displayed and clicking on a date makes this date be displayed on the label on the bottom

class idfeditor(QtGui.QMainWindow):
  def __init__(self):
    QtGui.QMainWindow.__init__(self)
  	#myWidget = GWidget()
    self.createActions()
    self.createMenus()
    self.createToolbar()
    self.createTabs()
    self.setCentralWidget(self.tabs)
    self.setWindowTitle('IDF Creator')
    self.setGeometry(QtGui.QDesktopWidget().screenGeometry())
    self.openProject()
  
  def createTabs(self) :
    self.project = project.Project()
    self.tabs = QtGui.QTabWidget()
    ptab = projecttab.projectTab()
    sarea = QtGui.QScrollArea()
    layout = QtGui.QVBoxLayout()
    layout.addWidget(ptab)
    sarea.setLayout(layout)
    self.tabs.addTab(sarea,'Project')
    gtab = GWidget()
    sarea = QtGui.QScrollArea()
    layout = QtGui.QVBoxLayout()
    layout.addWidget(gtab)
    sarea.setLayout(layout)
    self.tabs.addTab(sarea,'Objects')
    ztab = zonetab.zoneTab()
    sarea = QtGui.QScrollArea()
    layout = QtGui.QVBoxLayout()
    layout.addWidget(ztab)
    sarea.setLayout(layout)
    self.tabs.addTab(sarea,'Zones')
    self.connect(self, QtCore.SIGNAL('reloadProject()'), ptab.updateProject)
    self.connect(self, QtCore.SIGNAL('reloadProject()'), gtab.updateProject)
    self.connect(self, QtCore.SIGNAL('reloadProject()'), ztab.updateProject)
    ztab.setProject(self.project)
    gtab.setProject(self.project)
    ptab.setProject(self.project)
    
  def createActions(self):
    self.exit = QtGui.QAction('Exit', self)
    self.exit.setShortcut('Ctrl+Q')
    self.exit.setStatusTip('Exit application')
    self.connect(self.exit, QtCore.SIGNAL('triggered()'), QtCore.SLOT('close()'))
    self.newproject = QtGui.QAction('New Project', self)
    self.newproject.setShortcut('Ctrl+N')
    self.newproject.setStatusTip('Create a New Project')
    self.connect(self.newproject, QtCore.SIGNAL('triggered()'), self.createNewProject)
    self.openproject = QtGui.QAction('Open Project', self)
    self.openproject.setShortcut('Ctrl+O')
    self.openproject.setStatusTip('Open a Project')
    self.connect(self.openproject, QtCore.SIGNAL('triggered()'), self.openProject)

  def createMenus(self):
    
    menubar = self.menuBar()
    filem = menubar.addMenu('&File')
#    filem.addAction(self.newproject)
    filem.addAction(self.openproject)
    filem.addAction(self.exit)


  def createToolbar(self):
    toolbar = self.addToolBar('')
    toolbar.addAction(self.exit)
#    toolbar.addAction(self.newproject)
    toolbar.addAction(self.openproject)

  def createNewProject(self):
    print 'createNewProject'
    

  def openProject(self):
    print 'openProject'
    self.project.createNewProject()
    self.emit(QtCore.SIGNAL('reloadProject()'))










    

if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    window = idfeditor()
    window.show()
    sys.exit(app.exec_())
