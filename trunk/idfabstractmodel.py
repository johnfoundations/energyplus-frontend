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


class idfAbstractModel(QtCore.QAbstractItemModel):
    def __init__(self,source,parent = None):
        QtCore.QAbstractItemModel.__init__(self, parent)
        self.idfsource = source

    def setIdfSource(self,source):
      self.idfsource = source


    def columnCount (self, parent):
#       print "columnCount "+str(parent.row())+" "+str(parent.column())
#        if not parent.isValid():
        return 2
#        if parent.isValid():
#            return parent.internalPointer().childCount()

        
    def flags(self,index):
#        print "flags"
        if not index.isValid():
            return QtCore.Qt.ItemIsEnabled
        else:
            return QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsSelectable
        

    def data(self,modelindex,role):
        print "data" + str(role)+" "+str(modelindex.row())+" "+str(modelindex.column())
        
        #retrieve class from idfsource
        idf = modelindex.internalPointer()
        idfclass = self.idfsource.dataAt(idf.row,idf.column)

        if role == QtCore.Qt.ToolTipRole:
            return QtCore.QVariant(idfclass.getMemo())

        if role == QtCore.Qt.EditRole or role == QtCore.Qt.DisplayRole:
            if not idf.parent() == 0:
                if modelindex.column() == 0:
                    #get field name
                    return QtCore.QVariant(idfclass.fieldlist[idf.column].fieldname)

                elif modelindex.column() == 1:
                    return QtCore.QVariant(idfclass.fieldlist[idf.column].value)

            else:
                if modelindex.column() == 0:
                    return QtCore.QVariant(idfclass.getClassnameIDD())

                elif modelindex.column() == 1:
                    return QtCore.QVariant(idfclass.getName())

        return QtCore.QVariant()

    def headerData(self,section,orientation,role = QtCore.Qt.DisplayRole):
#        print "headerData"
#        print section
#        print orientation
#        print role
        if orientation == QtCore.Qt.Horizontal and role == QtCore.Qt.DisplayRole:
             if section == 0:
                 return QtCore.QVariant("IDDClass")
             else:
                 return QtCore.QVariant("Name")
        return QtCore.QVariant()
        

    def rowCount (self,parent ):
        print "rowCount"+ str(parent.row())+" "+str(parent.column())
        if parent.isValid():
            return parent.internalPointer().childCount()
        else:
            #not valid model.??
            return self.idfsource.size()
            

    def parent(self,index):
        dp = index.internalPointer().parent()
        if dp == 0:
            return QtCore.QModelIndex()
        else:
            return self.createIndex(dp.row,dp.column,dp)
        
 

#    def setData

#    def setHeaderData

#    def insertRows

#    def removeRows

#    def insertColumns

#    def removeColumns

    def index(self, row, column, parent):
        print "index" + str(row) + " " + str(column) +" " + str(parent.row()) +" " + str(parent.column())
        if parent.isValid():
            dp = parent.internalPointer().child(row)
                
        else:
            dp = self.idfsource.recordAt(row,column)

        return self.createIndex(row, column, dp)
 
        

if __name__ == "__main__":
    import sys
    import idfdata
    from PyQt4 import QtGui

    app = QtGui.QApplication(sys.argv)
    try:
        fname = sys.argv[1]
    except:
        fname = 'Singlezonetemplate.idf'

    f = idfdata.idfData()
    f.openIdf(fname)

    model = idfAbstractModel(f)

    view = QtGui.QTreeView()
    view.setModel(model)
    view.setWindowTitle("Simple Tree Model")
    view.show()
    sys.exit(app.exec_())
