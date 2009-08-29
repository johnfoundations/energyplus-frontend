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
import idfglobals

class newClassDialog(QtGui.QDialog):
    def __init__(self,parent=None,flags=0):
        QtGui.QDialog.__init__(self,parent)
        hl = QtGui.QHBoxLayout()
        vl = QtGui.QVBoxLayout(self)
        self.classlist = QtGui.QTreeWidget()
        self.classlist.setSelectionMode(QtGui.QAbstractItemView.ExtendedSelection)
        self.memo = QtGui.QLabel('Class Description')
        ccl = QtGui.QHBoxLayout()
        self.copycount = QtGui.QSpinBox()
        self.copycount.setMinimum(1)
        ccl.addWidget(QtGui.QLabel('Number or Copies to Create:'))
        ccl.addWidget(self.copycount)
        ccl.addStretch()
        rv = QtGui.QVBoxLayout()
        rv.addWidget(self.memo)
        #lrv.addSpacing()
        rv.addLayout(ccl)
        rv.addStretch()

        buttonBox = QtGui.QDialogButtonBox(QtGui.QDialogButtonBox.Ok | QtGui.QDialogButtonBox.Cancel);

        self.connect(buttonBox, QtCore.SIGNAL('accepted()'), self.accept);
        self.connect(buttonBox, QtCore.SIGNAL('rejected()'), self.reject);

        rv.addWidget(buttonBox)
        hl.addWidget(self.classlist)
        hl.addLayout(rv)
        vl.addLayout(hl)
        
        self.populateClassList()
        self.selected = []

    def populateClassList(self):
        self.classlist.setColumnCount(1)
        self.classlist.setHeaderLabel('IDD Classes')
        olist = idfglobals.getObjectTree()
        klist = olist.keys()
        klist.sort()
        for k in klist :
            items = olist[k]
            items.sort()
            i = QtGui.QTreeWidgetItem([k])
            self.classlist.addTopLevelItem(i)
            for ei in items :
                j = QtGui.QTreeWidgetItem(i,[ei])
                self.classlist.addTopLevelItem(j)

    def accept(self):
        s = self.classlist.selectedItems()
        self.selected = []
        for i in s :
            for x in range(self.copycount.value()):
                self.selected.append(i.text(0))

        self.done(1)

    def reject(self):
        self.selected = []
        self.done(0)


            
        

