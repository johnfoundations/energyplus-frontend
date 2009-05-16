#!/usr/bin/env python
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

import sys
from PyQt4 import QtCore, QtGui

import idfread
import pdb


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

    #def insertItem(self,idditem,root=None):
      #if not root == None:
        #start = root
      #else:
        #start = self

      #dep = idditem.getDepends()
      
      #if dep[0] in start.iddinstance.getReference()  :
        #tlist = []
        #tlist.append(idditem.getClassnameIDD())
        #tlist.append(idditem.getName())
        #self.appendChild(TreeItem(tlist,idditem,self))
        #return True


          
        #if self.iddinstance == 0 and idditem.getGroup() == self.itemData[0] :
          #tlist = []
          #tlist.append(idditem.getClassnameIDD())
          #tlist.append(idditem.getName())
          #self.appendChild(TreeItem(tlist,idditem,self))
          #return True
      #if len(idditem.getDepends()) > 0 and not self.iddinstance ==0:
        #dep = idditem.getDepends()

      #for l in self.childItems :
        #res = l.insertItem(idditem,ignoredepends)
        #if res :
          #return True
      #return False
        
      
        
      




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

    def setupModelData(self,lines,parent):
      number = 0
      count = 0
      inserted = False
      simparams = TreeItem(['Simulation Parameters',''],0,parent)
      loccli = TreeItem(['Location and Climate',''],0,parent)
      zones = TreeItem(['Zones',''],0,parent)
      materials = TreeItem(['Materials',''],0,parent)
      other = TreeItem(['Other',''],0,parent)
      schedules = TreeItem(['Schedules',''],0,parent)
      parent.appendChild(simparams)
      parent.appendChild(loccli)
      parent.appendChild(zones)
      parent.appendChild(materials)
      parent.appendChild(schedules)
      parent.appendChild(other)
      remaininglines = []
      remaininglines = lines[:]
      while number == 0:
        newremaining = []
        for o in remaininglines:
          if o.getGroup() == 'Simulation Parameters' or o.getName() == 'GlobalGeometryRules':
            tlist = []
            tlist.append(o.getClassnameIDD())
            tlist.append(o.getName())
            simparams.appendChild(TreeItem(tlist,o,simparams))
            continue

          if o.getGroup() == 'Location and Climate':
            tlist = []
            tlist.append(o.getClassnameIDD())
            tlist.append(o.getName())
            loccli.appendChild(TreeItem(tlist,o,loccli))
            continue

          if o.getGroup() == 'Schedules':
            tlist = []
            tlist.append(o.getClassnameIDD())
            tlist.append(o.getName())
            schedules.appendChild(TreeItem(tlist,o,schedules))
            continue

          if o.getGroup() == 'Compliance Objects':
            tlist = []
            tlist.append(o.getClassnameIDD())
            tlist.append(o.getName())
            simparams.appendChild(TreeItem(tlist,o,simparams))
            continue
              
              
          if o.getGroup() == 'Surface Construction Elements':
            tlist = []
            tlist.append(o.getClassnameIDD())
            tlist.append(o.getName())
            materials.appendChild(TreeItem(tlist,o,materials))
            continue

          if o.getClassnameIDD() == 'Zone':
            tlist = []
            tlist.append(o.getClassnameIDD())
            tlist.append(o.getName())
            zones.appendChild(TreeItem(tlist,o,zones))
            continue
          
          if o.getGroup() == 'Internal Gains' or o.getGroup() == 'Thermal Zones and Surfaces':
            #insert into appropriate zone
            deps = o.getObjectDepend()
            #pdb.set_trace()
            for z in zones.childItems:
              if z.iddinstance:
                if deps == z.iddinstance.getName():
                  #found match.now see where it goes
                  found = 0
                  for zc in z.childItems:
                    if zc.data(0) == o.getGroup():
                      tlist = []
                      tlist.append(o.getClassnameIDD())
                      tlist.append(o.getName())
                      zc.appendChild(TreeItem(tlist,o,zc))
                      found = 1
                      inserted = True
                      continue
                  if found == 0:
                    igti = TreeItem([o.getGroup(),''],0,z)
                    tlist = []
                    tlist.append(o.getClassnameIDD())
                    tlist.append(o.getName())
                    igti.appendChild(TreeItem(tlist,o,igti))
                    z.appendChild(igti)
                    inserted = True
                    continue

          if inserted:
            inserted = False
          else:
            newremaining.append(o)

        remaininglines = newremaining[:]
        count = count + 1
        if count > 3:
          number = 1
      
                     
                  
              
        

      
    


    def setupModelDataorig(self, lines, parent):
        parents = []
        parents.append(parent)

        number = 0
        remaininglines = []
        remaininglines = lines[:]
        ignoredepends = True
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
