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
        return 2

    def parent(self,index) :
        return QtCore.QModelIndex()

        
    def flags(self,index):
        if not index.isValid():
            return QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsSelectable
        else:
            return QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsSelectable
        

    def data(self,modelindex,role):
        #retrieve class from idfsource
        idf = modelindex.internalPointer()

        if role == QtCore.Qt.ToolTipRole:
            return QtCore.QVariant(idf.data.getMemo())

        if role == QtCore.Qt.EditRole or role == QtCore.Qt.DisplayRole:
            if modelindex.column() == 0:
                return QtCore.QVariant(idf.data.getClassnameIDD())

            elif modelindex.column() == 1:
                return QtCore.QVariant(idf.data.getName())

        return QtCore.QVariant()

    def headerData(self,section,orientation,role = QtCore.Qt.DisplayRole):
        if orientation == QtCore.Qt.Horizontal and role == QtCore.Qt.DisplayRole:
             if section == 0:
                 return QtCore.QVariant("IDDClass")
             else:
                 return QtCore.QVariant("Name")
        return QtCore.QVariant()
        

    def rowCount (self,parent ):
        if parent.isValid():
            return 0
#            return parent.internalPointer().childCount()
        else:
            #not valid model.??
            return self.idfsource.size()
            
    def index(self, row, column, parent):
        
   #     if parent.isValid():
   #         dp = parent.internalPointer().child(row)
   #     else:
        dp = self.idfsource.recordAt(row,0)

        return self.createIndex(row, column, dp)



    def query(self,searchflag,data):
        self.idfsource.query(searchflag,data)
        self.reset()


    def sort(self,column,order):
        self.idfsource.sortTree(column,order)
        self.reset()


class idfClassModel(QtCore.QAbstractTableModel):
    def __init__(self,idfclass,parent = None):
        QtCore.QAbstractTableModel.__init__(self, parent)
        self.idfclass = idfclass
        self.parentmodel = parent
        self.convert = True

        
    def columnCount (self, parent):
        return 1


    def flags(self,index):
        if not index.isValid():
            return QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsEditable | QtCore.Qt.ItemIsSelectable
        else:
            return QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEditable 
       

    def data(self,modelindex,role):
        #retrieve class from idfsource
        idf = modelindex.internalPointer()
        field = idf.fieldlist[modelindex.row()]

        if role == QtCore.Qt.ToolTipRole:
            return QtCore.QVariant(field.getNotes())

        if role == QtCore.Qt.EditRole or role == QtCore.Qt.DisplayRole:
            return QtCore.QVariant(field.getValue(self.convert))

        return QtCore.QVariant()

    def setData(self,index,value,role) :
        if role == QtCore.Qt.EditRole :
            idf = index.internalPointer()
            idf.fieldlist[index.row()].setValue(value,self.convert)
            self.idfclass.editSignal(self,index.row())
               


    def insertRows(self,row,count,parent) :
        if row == self.rowCount(0) and count > -1:
            self.beginInsertRows(parent,row,row+count-1)
            self.idfclass.createExtensibleFields()
            self.endInsertRows()
            return True
        return False

    def headerData(self,section,orientation,role = QtCore.Qt.DisplayRole):
        if orientation == QtCore.Qt.Horizontal and role == QtCore.Qt.DisplayRole:
             return QtCore.QVariant("Value")

        if orientation == QtCore.Qt.Vertical and role == QtCore.Qt.DisplayRole:
            return QtCore.QVariant(self.idfclass.fieldlist[section].fieldname + ' ' + self.idfclass.fieldlist[section].getUnits(self.convert))
            
        return QtCore.QVariant()


    def rowCount (self,parent ):
        return len(self.idfclass.fieldlist)

    def index(self, row, column, parent):
        if parent.isValid():
            dp = parent.internalPointer().child(row)
        else:
            dp = self.idfclass

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

    querylist = QtGui.QComboBox()
    querylist.addItems(['Classname','Name','Group','Dependancy','Reference','Fieldname','Fieldvalue'])

    queryline = QtGui.QLineEdit()
    querybutton = QtGui.QPushButton("Query")



    view = QtGui.QTreeView()
    view.setModel(model)


    view.setWindowTitle("Simple Tree Model")
    view.show()
    sys.exit(app.exec_())
