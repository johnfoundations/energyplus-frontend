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


class idfAbstractModel(QtCore.QAbstractItemModel):
    def __init__(source,parent = 0)
        QAbstractItemModel (self, parent)
        self.idfsource = source

    def setIdfSource(self,source):
      self.idfsource = source


    def columnCount (self, modelindexparent=0):
        if modleindexparent == 0:
            return 2
        else:
            #if parent is first column, no children
            if modelindexparent.column() = 1:
                instance = self.data(modelindexparent,IdfClassRole)
                return instance.fieldcount()
            else:
                return 2

        
    def flags(self,modelindex):

    def data(self,modelindex,role):
        if modelindex.row() > self.idfsource.size():
            return QtCore.QVariant()

        #retrieve class from idfsource
        idfclass = self.idfsource.recordAt(modelindex.row()
        if idfclass == None:
            return QtCore.QVariant()

        if role == IdfClassRole:
            return idfclass

        if role == QtCore.ToolTipRole:
            return QtCore.QString(idfclass.getMemo())

        if role == QtCore.EditRole or role == QtCore.DisplayRole:
            if modelindex.column() > idfclass.fieldCount():
                return QtCore.QVariant()

            return QtCore.QString(idfclass.getFieldData(modelindex.column())
            

    def headerData

    def rowCount

    def setData

    def setHeaderData

    def insertRows

    def removeRows

    def insertColumns

    def removeColumns

    def createIndex

    