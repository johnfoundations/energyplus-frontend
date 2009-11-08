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

from PyQt4 import QtCore, QtGui
import idfglobals
import idfdata
import iddclass
import surfaceitem
import objectclass
import verticemath

IdfVerticeRole = 45

class idfZoneModel(QtCore.QAbstractItemModel):
    modelreset = QtCore.pyqtSignal()
    
    def __init__(self,scene,idf,parent = None):
        print 'init'
        self.idf = idf
        self.parentmodel = parent
        self.zoneroot = None
        self.geometryrules = dict()
        self.itemdict = dict()
        self.zhandler = None
        #self.createZoneTree()
        self.math = verticemath.verticeMath()
        QtCore.QAbstractItemModel.__init__(self, parent)


    def reset(self):
        print 'zonemodel reset'
        self.createZoneTree()
        QtCore.QAbstractItemModel.reset(self)
        self.modelreset.emit()
    
            

    def setScene(self,scene):
        print 'zonemodel setscene'
        self.scene =  scene


        

    def createZoneTree(self):
        print 'zonemodel createZoneTree'
        buildingclass = None
        zonelist = dict()
        surfacelist = []
        if len(self.idf.idflist) == 0:
            return
        for c in self.idf.idflist:
            if c.getClassnameIDD() == 'Building':
                buildingclass = c

            elif c.getClassnameIDD() == 'GlobalGeometryRules':
                self.geometryrules = c.getDataDict()
              

            elif c.getClassnameIDD() == 'Zone':
                zonelist[c.getName()] = [c]

            elif c.getGroup() == 'Thermal Zones and Surfaces':
                surfacelist.append(c)
              

        if buildingclass == None:
            buildingclass = iddclass.building()
            self.idf.insertRecord(buildingclass)
            
        self.zoneroot = idfdata.treeItem(None,surfaceitem.surfaceItem(buildingclass,self))
        zonelist['Undefined'] = []
        surfacedict = dict()


        for c in surfacelist:
            z = c.getFieldDataByName('Zone Name')
            if z:
                if z in zonelist:
                    zonelist[z].append(c)
                else:
                    zonelist['Undefined'].append(c)
            else:
                s = c.getFieldDataByName("Building Surface Name")
                if s:
                    if s in surfacedict:
                        surfacedict[s].append(c)
                    else:
                        surfacedict[s] = [c]
                else:
                    zonelist['Undefined'].append(c)
        undefclass = undefined()
        undefnode = idfdata.treeItem(self.zoneroot,surfaceitem.surfaceItem(undefclass,self))
        for k,l in zonelist.iteritems():
            #create treeitem
            if k == 'Undefined':
                zti = undefnode
            else:
                zti = idfdata.treeItem(self.zoneroot,surfaceitem.surfaceItem(l.pop(0),self))
                self.itemdict[k] = zti

            self.zoneroot.appendChild(zti)
            for c in l:
                sti = idfdata.treeItem(zti,surfaceitem.surfaceItem(c,self))
                self.itemdict[c.getName()] = sti
                if c.getName() in surfacedict:
                    for cl in surfacedict[c.getName()]:
                        sti.appendChild(idfdata.treeItem(sti,surfaceitem.surfaceItem(cl,self)))
                    del surfacedict[c.getName()]
                zti.appendChild(sti)

        for k,l in surfacedict.iteritems():
            for c in l:
                undefnode.appendChild(idfdata.treeItem(undefnode,surfaceitem.surfaceItem(c,self)))

        
    def getGeometryRules(self):
        if len(self.geometryrules) == 0:
            self.geometryrules = {"Starting Vertex Position":"UpperLeftCorner",  \
                                  "Vertex Entry Direction":"Counterclockwise",  \
                                  "Coordinate System":"World", \
                                  "Daylighting Reference Point Coordinate System":"Relative",  \
                                  "Rectangular Surface Coordinate System":"Relative"}

        return self.geometryrules

    def getZone(self,zname):
        for z in self.zoneroot.childItems:
            if z.data.idfclass.getClassnameIDD() == 'Zone' and z.data.idfclass.getName() == zname:
                return z,z.data.idfclass

        return None,None
        #treeitem,idd class instance

    def getSurface(self,surfacename):
        if surfacename in self.itemdict:
            return self.itemdict[surfacename].data
        

        
    def columnCount (self, parent):
        
        return 1
#        if parent.isValid():
#            return parent.internalPointer().childCount()
#        else:
#            return self.zoneroot.childCount()

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

    def rowCount(self, parent=QtCore.QModelIndex()):
        if parent.column() > 0:
            return 0

        if self.zoneroot == None:
            return 0

        if not parent.isValid():
            parentItem = self.zoneroot
        else:
            parentItem = parent.internalPointer()

        return parentItem.childCount()



       

    def data(self,modelindex,role):
        #retrieve class from idfsource
        titem = modelindex.internalPointer()

        if role == QtCore.Qt.ToolTipRole:
            return QtCore.QVariant(titem.data.idfclass.getMemo())

        if role == QtCore.Qt.DisplayRole:
            return QtCore.QVariant(titem.data.idfclass.getName() + ' -- ' + titem.data.idfclass.getClassnameIDD())

        if role == IdfVerticeRole:
#            print 'data', titem.data.verticelist
            return QtCore.QVariant(titem.data.verticelist)

        return QtCore.QVariant()


    def index(self, row, column, parent=QtCore.QModelIndex()):
        if row < 0 or column < 0 or row >= self.rowCount(parent) or column >= self.columnCount(parent):
            print 'index data out of range'
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




class undefined(objectclass.ObjectAbstract):

    def getName(self):
        return 'Undefined'

    def getClassnameIDD(self):
        return 'Abstract'


class zonemodeltest(QtGui.QMainWindow):
    def __init__(self):
        QtGui.QMainWindow.__init__(self)
        fname = 'singlezonecopy.idf'

        f = idfdata.idfData()
        f.openIdf(fname)

 #       model = idfabstractmodel.idfAbstractModel(f)
        self.zonemodel = idfZoneModel(None,f)

 #       model.query(idfglobals.IdfQueryClassname,'Zone')


        widget = QtGui.QWidget()
        layout = QtGui.QHBoxLayout(widget)
 #       view = QtGui.QTreeView()
 #       view.setModel(model)
 #       layout.addWidget(view)

        view2 = QtGui.QTreeView()
        view2.setModel(self.zonemodel)
        layout.addWidget(view2)
        self.setCentralWidget(widget)
 #       self.connect(view, QtCore.SIGNAL('activated (QModelIndex)'),self.classActivated)

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
