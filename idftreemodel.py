#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""***************************************************************************
**
** Copyright (C) 2005-2005 Trolltech AS. All rights reserved.
**
** This file is part of the example classes of the Qt Toolkit.
**
** This file may be used under the terms of the GNU General Public
** License version 2.0 as published by the Free Software Foundation
** and appearing in the file LICENSE.GPL included in the packaging of
** this file.  Please review the following information to ensure GNU
** General Public Licensing requirements will be met:
** http://www.trolltech.com/products/qt/opensource.html
**
** If you are unsure which license is appropriate for your use, please
** review the following information:
** http://www.trolltech.com/products/qt/licensing.html or contact the
** sales department at sales@trolltech.com.
**
** This file is provided AS IS with NO WARRANTY OF ANY KIND, INCLUDING THE
** WARRANTY OF DESIGN, MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE.
**
***************************************************************************"""

import sys
from PyQt4 import QtCore, QtGui

import idfread
#import pdb


class TreeItem:
    def __init__(self, data,instance=0,parent=None):
        self.parentItem = parent  
        self.itemData = data      #list
        self.childItems = []      #tree items
        self.iddinstance = instance

    def appendChild(self, item):
        self.childItems.append(item)   #tree items

    def child(self, row):
        return self.childItems[row]    #tree items

    def childCount(self):
        return len(self.childItems)

    def columnCount(self):
      return len(self.itemData)

    def data(self, column):
        return self.itemData[column]

    def parent(self):
        return self.parentItem             #tree item

    def row(self):
        if self.parentItem:
            return self.parentItem.childItems.index(self)
        return 0

    def insertItem(self,idditem,ignoredepends):
      if len(idditem.getDepends()) == 0 or ignoredepends :
        if self.iddinstance == 0 and idditem.getGroup() == self.itemData[0] :
          tlist = []
          tlist.append(idditem.getClassnameIDD())
          tlist.append(idditem.getName())
          self.appendChild(TreeItem(tlist,idditem,self))
          return True
      if len(idditem.getDepends()) > 0 and not self.iddinstance ==0:
        dep = idditem.getDepends()
        if dep[0] in self.iddinstance.getReference()  :
          tlist = []
          tlist.append(idditem.getClassnameIDD())
          tlist.append(idditem.getName())
          self.appendChild(TreeItem(tlist,idditem,self))
          return True
      for l in self.childItems :
        res = l.insertItem(idditem,ignoredepends)
        if res :
          return True
      return False
        
      
        
      




class TreeModel(QtCore.QAbstractItemModel):
    def __init__(self, data, parent=None):
        QtCore.QAbstractItemModel.__init__(self, parent)
        rootData = []
        rootData.append(QtCore.QVariant("IDD Class Name"))
        rootData.append(QtCore.QVariant("Instance Name"))
        
        self.rootItem = TreeItem(rootData)
        self.setupModelData(data, self.rootItem)

    def columnCount(self, parent):
        if parent.isValid():
            return parent.internalPointer().columnCount()
        else:
            return self.rootItem.columnCount()

    def data(self, index, role):
        if not index.isValid():
            return QtCore.QVariant()

        if role != QtCore.Qt.DisplayRole:
            return QtCore.QVariant()

        item = index.internalPointer()

        return QtCore.QVariant(item.data(index.column()))

    def flags(self, index):
        if not index.isValid():
            return QtCore.Qt.ItemIsEnabled

        return QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsSelectable

    def headerData(self, section, orientation, role):
        if orientation == QtCore.Qt.Horizontal and role == QtCore.Qt.DisplayRole:
            return self.rootItem.data(section)

        return QtCore.QVariant()

    def index(self, row, column, parent):
        if row < 0 or column < 0 or row >= self.rowCount(parent) or column >= self.columnCount(parent):
            return QtCore.QModelIndex()

        if not parent.isValid():
            parentItem = self.rootItem
        else:
            parentItem = parent.internalPointer()

        childItem = parentItem.child(row)
        if childItem:
            return self.createIndex(row, column, childItem)
        else:
            return QtCore.QModelIndex()

    def parent(self, index):
        if not index.isValid():
            return QtCore.QModelIndex()

        childItem = index.internalPointer()
        parentItem = childItem.parent()

        if parentItem == self.rootItem:
            return QtCore.QModelIndex()

        return self.createIndex(parentItem.row(), 0, parentItem)

    def rowCount(self, parent):
        if parent.column() > 0:
            return 0

        if not parent.isValid():
            parentItem = self.rootItem
        else:
            parentItem = parent.internalPointer()

        return parentItem.childCount()

    def setupModelData(self, lines, parent):
        parents = []
        parents.append(parent)

        number = 0
        remaininglines = []
        remaininglines = lines[:]
        ignoredepends = False
        while number == 0:
          newremaining = []

          for v in remaininglines:
            if not self.rootItem.insertItem(v,ignoredepends) :
              if len(v.getDepends()) == 0:
                parent.appendChild(TreeItem([v.getGroup(),''],0,parent))
              newremaining.append(v)
          if len(newremaining) == len(remaininglines) :
            ignoredepends = True
          if len(newremaining) == 0:
            number = 1
          remaininglines = newremaining[:]
        if len(remaininglines) > 0 :
          unconnected = TreeItem(['Unconnected',''],0,parent)
          for v in remaininglines:
            tlist = []
            tlist.append(v.getClassnameIDD())
            tlist.append(v.getName())
            unconnected.appendChild(TreeItem(tlist,v,unconnected))
          parent.appendChild(unconnected)

            
            
            
          

if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)

    f = idfread.idfRead('Singlezonetemplate.idf')

    model = TreeModel(f.getActivelist())

    view = QtGui.QTreeView()
    view.setModel(model)
    view.setWindowTitle("Simple Tree Model")
    view.show()
    sys.exit(app.exec_())
