# -*- coding: utf-8 -*-
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
    self.idfScene = GGraphicsScene()
    self.idfView =  QtGui.QGraphicsView(self.idfScene)    
    self.horizontallayout = QtGui.QHBoxLayout(self)
#    self.objecttree = QtGui.QTreeWidget()
    self.activeobjectlist = QtGui.QTreeView()
#    self.objecttree.setSizePolicy(QtGui.QSizePolicy(1,7))
    self.horizontallayout.addWidget(self.activeobjectlist)
    self.horizontallayout.addWidget(self.idfView)
#    self.rightvert = QtGui.QVBoxLayout()
    
    f = idfread.idfRead('Singlezonetemplate.idf')
    self.activemodel = idftreemodel.TreeModel(f.getActivelist())
    self.activeobjectlist.setModel(self.activemodel)
    self.activeobjectedit = None
#    self.rightvert.addWidget(self.activeobjectlist)
    #self.rightvert.addWidget(self.activeobjectedit)
#    self.horizontallayout.addWidget(self.activeobjectedit)
    self.connect(self.activeobjectlist, QtCore.SIGNAL('activated (const QModelIndex&)'),
                 self.activeObjectChanged)
#    self.populateObjectTree()

  def populateObjectTree(self):
    self.objecttree.setColumnCount(1)
#    objects = QtGui.QTreeWidgetItem(self.objecttree)
    self.objecttree.setHeaderLabel('Objects')
    olist = idfglobals.getObjectTree()
#    objects = QtGui.QTreeWidgetItem(self.objecttree)
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
    

