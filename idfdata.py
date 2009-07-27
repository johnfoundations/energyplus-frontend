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
import idfread
from idfglobals import *

class treeItem:
    def __init__(self, parent,row,column):
        self.parentItem = parent
        self.childItems = []
        self.row = row
        self.column = column

    def appendChild(self, child):
        self.childItems.append(child)

    def child(self, row):
        return self.childItems[row]

    def childCount(self):
        return len(self.childItems)

    def row(self):
        if self.parentItem:
            items = self.parentItem.childItems
            for (row,item) in enumerate(items):
                if item is self:
                    return row

        return 0

    def parent(self):
        return self.parentItem

      
        


class idfData(QtCore.QObject):
    def __init__(self,parent = 0):
        self.idfreadlist = []   #list of idfread classes, allowing multiple idf files to be loaded
        self.idflist = []       #list of classes from idf files
        self.current = 0        #pointer to current class, used in iterating through list
        self.idftree = []

    def next(self):
        if current == len(self.idflist):
            return False
        current = current + 1
        return True

    def previous(self):
        if current == 0:
            return False
        current = current - 1    
        return True

    def first(self):
        if len(self.idflist) == 0:
            return False
        current = 0
        return True

    def last(self):
        if len(self.idflist) == 0:
            return False
        current = self.idflist(self.current) - 1
        return True

    def size(self):
        return len(self.idflist)
        #returns count

    def seek(self,index):
        if index > self.size() or index < 0:
            return False
        current = index
        return True

    def record(self):
        return self.idftree[self.current]


    def recordAt(self,row,column):
        idfrec = self.idftree[row]
        if column == 0:
            return idfrec
        else:
            try:
                return idfrec.child(column)
            except:
                return idfrec
       

    def dataAt(self,row,column):
        try:
            return self.idflist[row]
        except:
            return None
        
    def query(self,flag,data):
        #flags in idfglobals
        querylist = []
        if flag == IdfQueryClassname:
            for idf in self.idflist:
                if idf.getClassnameIDD() == data:
                    querylist.append(idf)

        if flag == IdfQueryName:
            for idf in self.idflist:
                if idf.getName() == data:
                    querylist.append(idf)
                    
        if flag == IdfQueryGroup:
            for idf in self.idflist:
                if idf.getGroup() == data:
                    querylist.append(idf)
                    
        if flag == IdfQueryDependancy:
            for idf in self.idflist:
                if data in idf.getDepends():
                    querylist.append(idf)
                    
        if flag == IdfQueryReference:
            for idf in self.idflist:
                if data in idf.getReference():
                    querylist.append(idf)
                    
        if flag == IdfQueryFieldname:
            for idf in self.idflist:
                for fld in idf.fieldlist:
                    if fld.getFieldName() == data:
                        querylist.append(idf)
                        break
                    
        if flag == IdfQueryFieldValue:
            for idf in self.idflist:
                for fld in idf.fieldlist:
                    if fld.getValue() == data:
                        querylist.append(idf)
                        break
                
        self.populateTree(querylist)



        
    def openIdf(self,filename):
        idf = idfread.idfRead(filename)
        if len(self.idflist) > 0:
            self.idflist = idf.getActiveList()
        else:
            self.idflist = self.idflist + idf.getActiveList()

        self.idfreadlist.append(idf)
        self.populateTree(self.idflist)


    def populateTree(self,olist):
        self.idftree = []
        for r,idf in enumerate(olist):
            t = treeItem(0,r,0)
            for c,field in enumerate(idf.fieldlist):
                t.appendChild(treeItem(t,r,c))
            self.idftree.append(t)
        

    def writeIdf(self,filename):
        pass
