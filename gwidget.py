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

# class that displays and controls inputs to define a building
from PyQt4 import QtGui, QtCore
import sys
import iddclass
import idfglobals
import fieldclasses
import objectclass
import idfread
import idftreemodel



class GWidget(QtGui.QWidget):
  def __init__(self, parent=None):
    QtGui.QWidget.__init__(self, parent)
#    self.idfScene = GGraphicsScene()
#    self.idfView =  QtGui.QGraphicsView(self.idfScene)    
    self.horizontallayout = QtGui.QHBoxLayout()
    self.verticallayout = QtGui.QVBoxLayout(self)
    self.activeobjectlist = QtGui.QTreeView()
    self.horizontallayout.addWidget(self.activeobjectlist)
#    self.horizontallayout.addWidget(self.idfView)
    self.verticallayout.addLayout(self.horizontallayout)
    
    f = idfread.idfRead('Singlezonetemplate.idf')
    self.activemodel = idftreemodel.TreeModel(f.getActivelist())
    idfglobals.referencedict = f.getActiveReferences()
    self.activeobjectlist.setModel(self.activemodel)
    self.activeobjectedit = None
    self.connect(self.activeobjectlist, QtCore.SIGNAL('activated (const QModelIndex&)'),
                 self.activeObjectChanged)

  def populateObjectTree(self):
    self.objecttree.setColumnCount(1)
    self.objecttree.setHeaderLabel('Objects')
    olist = idfglobals.getObjectTree()
    klist = olist.keys() 
    for k in olist :
      items = olist[k]
      i = QtGui.QTreeWidgetItem([k])
      self.objecttree.addTopLevelItem(i)
      for ei in items :
        j = QtGui.QTreeWidgetItem(i,[ei])
        self.objecttree.addTopLevelItem(j)

  def activeObjectChanged(self,Index) :
    iddcl = Index.internalPointer().iddinstance
    if not iddcl.__class__.__name__ == 'int':
      if not self.activeobjectedit == None:
        self.activeobjectedit.getData()
        self.activeobjectedit.closeWidget()
      self.activeobjectedit = iddcl
      if not self.activeobjectedit == None:
        self.horizontallayout.addWidget(self.activeobjectedit.CreateEditWidget())
      else:
        print 'No object to display'
    
  






class GGraphicsScene(QtGui.QGraphicsScene) :
  def __init__(self, parent=None):
    QtGui.QGraphicsScene.__init__(self,parent)
    



  def mousePressEvent(self, mouseEvent):
    print "MousePressEvent on widget"
    

