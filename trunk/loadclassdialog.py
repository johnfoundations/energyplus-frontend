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
import idfdata
import idfabstractmodel

class loadClassDialog(QtGui.QDialog):
    def __init__(self,parent=None,flags=0):
        QtGui.QDialog.__init__(self,parent)

        self.sourceidf = idfdata.idfData()
        self.sourcemodel = idfabstractmodel.idfAbstractModel(self.sourceidf)
        self.destidf = idfdata.idfData()
        self.destmodel = idfabstractmodel.idfAbstractModel(self.destidf)
        self.sourceclasslist = QtGui.QTreeView()
        self.sourceclasslist.setModel(self.sourcemodel)
        self.sourceclasslist.setSelectionMode(QtGui.QAbstractItemView.ExtendedSelection)
        self.destclasslist = QtGui.QTreeView()
        self.destclasslist.setModel(self.destmodel)
        self.classdata = QtGui.QTextEdit()
        self.classdata.setReadOnly(True)
        self.classdata.setWordWrapMode(QtGui.QTextOption.NoWrap)
        self.todest = QtGui.QPushButton('-->')
        self.tosource = QtGui.QPushButton('<--')
        buttonBox = QtGui.QDialogButtonBox(QtGui.QDialogButtonBox.Ok | QtGui.QDialogButtonBox.Cancel);
        self.loadfilebutton = QtGui.QPushButton('&Load IDF File')
        self.loaddependancies = QtGui.QCheckBox('&Copy Dependancies?')
        self.loaddependancies.setChecked(True)
        
        hl = QtGui.QHBoxLayout(self)
        vl = QtGui.QVBoxLayout()
        
        vl.addWidget(self.loadfilebutton)
        vl.addWidget(self.sourceclasslist)
        vl.addWidget(self.classdata)

        vc = QtGui.QVBoxLayout()
        vc.addStretch()
        vc.addWidget(self.todest)
        vc.addWidget(self.tosource)
        vc.addStretch()

        rv = QtGui.QVBoxLayout()
        
        rv.addWidget(self.destclasslist)
        rv.addWidget(self.loaddependancies)

        rv.addWidget(buttonBox)
        

        self.connect(buttonBox, QtCore.SIGNAL('accepted()'), self.accept);
        self.connect(buttonBox, QtCore.SIGNAL('rejected()'), self.reject);
        self.connect(self.todest, QtCore.SIGNAL('pressed()'), self.moveToDest);
        self.connect(self.tosource, QtCore.SIGNAL('pressed()'), self.moveToSource);
        self.connect(self.loadfilebutton, QtCore.SIGNAL('pressed()'), self.loadFile);
        self.connect(self.sourceclasslist, QtCore.SIGNAL('activated(QModelIndex)'), self.sourceListActivated);
        
        hl.addLayout(vl)
        hl.addLayout(vc)
        hl.addLayout(rv)
        self.selected = []
        self.loadFile()


    def accept(self):
        self.done(1)

    def reject(self):
        self.selected = []
        self.done(0)

    def moveToSource(self):
        indexlist = self.destclasslist.selectedIndexes()
        print len(indexlist)
        for i in indexlist:
            if i.column() == 0:
                self.sourceidf.insertRecord(i.internalPointer().data)
                self.destidf.deleteRecord(i.internalPointer().data)
        self.destmodel.reset()
        self.sourcemodel.reset()

    def moveToDest(self):
        indexlist = self.sourceclasslist.selectedIndexes()
        print len(indexlist)
        for i in indexlist:
            if i.column() == 0:
                instance = i.internalPointer().data
                self.destidf.insertRecord(instance)
                self.sourceidf.deleteRecord(instance)
                cl = self.sourceidf.getDependancies(instance)
                for c in cl:
                    self.destidf.insertRecord(c)
                    self.sourceidf.deleteRecord(c)
                    
        self.destmodel.reset()
        self.sourcemodel.reset()

    def loadFile(self):
        self.fileName = QtGui.QFileDialog.getOpenFileName(self,"Open IDF File", ".", "*.idf *.IDF");
        self.sourceidf.openIdf(self.fileName)
        self.sourcemodel.reset()

    def sourceListActivated(self,model):
        idf = model.internalPointer().data
        self.classdata.setPlainText(idf.__str__())
        

        
            
        

