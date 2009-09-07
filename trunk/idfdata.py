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
import idfglobals 

class treeItem:
    def __init__(self, parent,data):
        self.parentItem = parent
        self.childItems = []
        self.data = data


    def __cmp__(self,other):
        if self.parentItem.cmpcolumn:
            return cmp(self.data.getName(),other.data.getName())
        else:
            return cmp(self.data.getClassnameIDD(),other.data.getClassnameIDD())

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
        self.referencedict = dict()
        self.cmpcolumn = 0

    def getDepends(self,name):
        dlist = []
        for o in self.referencedict[name]:
            dlist.append(o.getName())
        return dlist


    def next(self):
        if self.current == len(self.idflist):
            print 'next false'
            return False
        self.current = self.current + 1
        return True

    def previous(self):
        if self.current == 0:
            return False
        self.current = self.current - 1    
        return True

    def first(self):
        if len(self.idflist) == 0:
            return False
        self.current = 0
        return True

    def last(self):
        if len(self.idflist) == 0:
            return False
        self.current = self.idflist(self.current) - 1
        return True

    def size(self):
        return len(self.idftree)
        #returns count

    def seek(self,index):
        if index > self.size() or index < 0:
            return False
        self.current = index
        return True

    def record(self):
        return self.idflist[self.current]


    def recordAt(self,row,column):
        idfrec = self.idftree[row]
        if column == 0:
            return idfrec
        else:
            try:
                return idfrec.child(column)
            except:
                return idfrec
       
    def insertRecord(self,instance) :
        self.idflist.append(instance)
        self.populateTree(self.idflist)

    def deleteRecord(self,instance) :
        try:
            index = self.idflist.index(instance)
        except:
            return False

        self.idflist.pop(index)
        self.populateTree(self.idflist)


    def dataAt(self,row,column):
        try:
            return self.idflist[row]
        except:
            return None
        
    def query(self,flag,data):
        #flags in idfglobals
        querylist = []

        if flag == idfglobals.IdfQueryAll:
            querylist = self.idflist

        
        if flag == idfglobals.IdfQueryClassname:
            for idf in self.idflist:
                if idf.getClassnameIDD() == data:
                    querylist.append(idf)

        if flag == idfglobals.IdfQueryName:
            for idf in self.idflist:
                if idf.getName() == data:
                    querylist.append(idf)
                    
        if flag == idfglobals.IdfQueryGroup:
            for idf in self.idflist:
                if idf.getGroup() == data:
                    querylist.append(idf)
                    
        if flag == idfglobals.IdfQueryDependancy:
            for idf in self.idflist:
                if data in idf.getDepends():
                    querylist.append(idf)
                    
        if flag == idfglobals.IdfQueryReference:
            for idf in self.idflist:
                if data in idf.getReference():
                    querylist.append(idf)
                    
        if flag == idfglobals.IdfQueryFieldname:
            for idf in self.idflist:
                for fld in idf.fieldlist:
                    if fld.getFieldName() == data:
                        querylist.append(idf)
                        break
                    
        if flag == idfglobals.IdfQueryFieldValue:
            for idf in self.idflist:
                for fld in idf.fieldlist:
                    if fld.getValue() == data:
                        querylist.append(idf)
                        break
                
        self.populateTree(querylist)

    def buildDependsTree(self):
        for i in self.idflist:
            #first get a list of depend from object
            rl = i.getReference()
            #look through references and build dict
            for ref in rl:
                if not ref in self.referencedict:
                    l = []
                    l.append(i)
                    self.referencedict[ref] = l
                else:
                    self.referencedict[ref].append(i)    


        
    def openIdf(self,filename):
        idf = idfread.idfRead(filename)
        if idf.success == False:
            msgBox = QtGui.QMessageBox()
            msgBox.setText("An Error Occurred when Loading the IDF file. Ok to continue with created objects")
            msgBox.setInformativeText(idf.errormsg)
            msgBox.setStandardButtons(QtGui.QMessageBox.Ok | QtGui.QMessageBox.Cancel)
            msgBox.setDefaultButton(QtGui.QMessageBox.Cancel)
            if msgBox.exec_() == 1:
                return
        if len(self.idflist) > 0:
            self.idflist = idf.getActiveList()
        else:
            self.idflist = self.idflist + idf.getActiveList()

        self.idfreadlist.append(idf)
        self.populateTree(self.idflist)
        self.buildDependsTree()


    def populateTree(self,olist):
        self.idftree = []
        for idf in olist:
            t = treeItem(self,idf)
            for field in idf.fieldlist:
                t.appendChild(treeItem(t,idf))
            self.idftree.append(t)


    def getDependancies(self, idfclass):
        l = []
        cl = []
        for f in idfclass.fieldlist:
            if f.__class__.__name__ == 'FieldObjectlist':
                if not f.value in l:
                    l.append(f.value)

        count = len(l)

        while True:
            for i in self.idflist:
                if i.getName() in l:
                    for f in i.fieldlist:
                        if f.__class__.__name__ == 'FieldObjectlist':
                            if not f.value in l:
                                l.append(f.value)

            if len(l) > count:
                count = len(l)
            else:
                break
                            

        for i in self.idflist:
            if i.getName() in l:
                cl.append(i)

        return cl
                

    def sortTree(self,column,direction):
        self.cmpcolumn = column
      
        if direction == QtCore.Qt.AscendingOrder:
            self.idftree.sort()
        else:
            self.idftree.reverse()
        

    def writeIdf(self,filename):
        pass
