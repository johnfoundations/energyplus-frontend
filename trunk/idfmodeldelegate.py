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
import sys
import idfdata


class idfClassDelegate(QtGui.QItemDelegate):
    def __init__(self,parent=None):
        QtGui.QItemDelegate.__init__(self,parent)

    def createEditor(self,parent,option,index):
        return index.internalPointer().fieldlist[index.row()].createEditor(parent)

    def setEditorData(self,editor,index):
        data = index.data(QtCore.Qt.EditRole)
        index.internalPointer().fieldlist[index.row()].setEditorValue(editor)
     
    def setModelData(self,editor,model,index):
        value = index.internalPointer().fieldlist[index.row()].getEditorValue(editor)
        model.setData(index, value, QtCore.Qt.EditRole)
         

    def updateEditorGeometry(self,editor,option,index):
        editor.setGeometry(option.rect)

