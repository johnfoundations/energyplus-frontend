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

from PyQt4 import QtCore
import idfglobals
from PyQt4 import QtGui


class idfZoneModel(QtCore.QAbstractItemModel):
    def __init__(self,zoneclass,idf,parent = None):
        QtCore.QAbstractItemModel.__init__(self, parent)
        self.zone = zoneclass
        self.idf = idf
        self.parentmodel = parent
        self.setZoneClass(self.zone)

    def setZoneClass(self,zoneclass):
        self.zone = zoneclass
        if zoneclass == None:
            self.zoneroot = treeItem(None,None)
        else:
            self.zoneroot = self.idf.createZoneTree(zoneclass,zoneclass.getGroup())
        
    def columnCount (self, parent):
        if parent.isValid():
            return parent.internalPointer().childCount()
        else:
            return self.zoneroot.childCount()

    def flags(self, index):
        if not index.isValid():
            return QtCore.Qt.ItemIsEnabled

        return QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsSelectable

    def headerData(self, section, orientation, role):
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

        if parentItem == self.zoneroot:
            return QtCore.QModelIndex()

        return self.createIndex(parentItem.row(), 0, parentItem)

    def rowCount(self, parent):
        if parent.column() > 0:
            return 0

        if not parent.isValid():
            parentItem = self.zoneroot
        else:
            parentItem = parent.internalPointer()

        return parentItem.childCount()



       

    def data(self,modelindex,role):
        #retrieve class from idfsource
        idf = modelindex.internalPointer()

        if role == QtCore.Qt.ToolTipRole:
            return QtCore.QVariant(idf.data.getNotes())

        if role == QtCore.Qt.DisplayRole:
            return QtCore.QVariant(idf.data.getName())

        return QtCore.QVariant()


    def index(self, row, column, parent):
        if row < 0 or column < 0 or row >= self.rowCount(parent) or column >= self.columnCount(parent):
            return QtCore.QModelIndex()

        if not parent.isValid():
            parentItem = self.zoneroot
        else:
            parentItem = parent.internalPointer()

        childItem = parentItem.child(row)
        if childItem:
            return self.createIndex(row, column, childItem)
        else:
            return QtCore.QModelIndex()




class zonemodeltest(QtGui.QMainWindow):
    def __init__(self):
        QtGui.QMainWindow.__init__(self)
        fname = 'Singlezonetemplate.idf'

        f = idfdata.idfData()
        f.openIdf(fname)

        model = idfabstractmodel.idfAbstractModel(f)
        self.zonemodel = idfZoneModel(None,f)

        model.query(idfglobals.IdfQueryClassname,'Zone')


        widget = QtGui.QWidget()
        layout = QtGui.QHBoxLayout(widget)
        view = QtGui.QTreeView()
        view.setModel(model)
        layout.addWidget(view)

        view2 = QtGui.QTreeView()
        view2.setModel(self.zonemodel)
        layout.addWidget(view2)
        self.setCentralWidget(widget)
        self.connect(view, QtCore.SIGNAL('activated (QModelIndex)'),self.classActivated)

    def classActivated(self,index):
        idf = index.internalPointer().data
        self.zonemodel.setZoneClass(idf)
        self.zonemodel.reset()
        


if __name__ == "__main__":
    import sys
    import idfdata
    from PyQt4 import QtGui
    import idfabstractmodel

    app = QtGui.QApplication(sys.argv)

    mtest = zonemodeltest()
    mtest.setWindowTitle("Simple Tree Model")
    mtest.show()
    sys.exit(app.exec_())
