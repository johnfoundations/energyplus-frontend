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
import idfabstractmodel
import idfmodeldelegate
import newclassdialog

class idfmodeltest(QtGui.QMainWindow):
    def __init__(self):
        QtGui.QMainWindow.__init__(self)
        self.idf = idfdata.idfData()
        self.model = idfabstractmodel.idfAbstractModel(self.idf)

        self.querylist = QtGui.QComboBox()
        self.querylist.addItems(['All','Classname','Name','Group','Dependancy','Reference','Fieldname','Fieldvalue'])

        self.queryline = QtGui.QLineEdit()
        self.querybutton = QtGui.QPushButton("Query")

        self.view = QtGui.QTreeView()
        self.view.setModel(self.model)

        widget = QtGui.QWidget()

        mainhbox = QtGui.QHBoxLayout(widget)
        vbox = QtGui.QVBoxLayout()
        hbox = QtGui.QHBoxLayout()

        hbox.addWidget(self.querylist)
        hbox.addWidget(self.queryline)

        vbox.addLayout(hbox)
        vbox.addWidget(self.querybutton)
        vbox.addWidget(self.view)
        mainhbox.addLayout(vbox)
        classvbox = QtGui.QVBoxLayout()
        self.classviewname = QtGui.QLabel()
        self.classview = QtGui.QTableView()
        self.delegate  = idfmodeldelegate.idfClassDelegate()
        self.classview.setItemDelegate(self.delegate)
        self.classview.setEditTriggers(QtGui.QAbstractItemView.AllEditTriggers)
        classvbox.addWidget(self.classviewname)
        classvbox.addWidget(self.classview)
        mainhbox.addLayout(classvbox)
        self.connect(self.view, QtCore.SIGNAL('activated (QModelIndex)'),self.classActivated)
        
        self.connect(self.querybutton, QtCore.SIGNAL('clicked ( bool)'),self.querybuttonclicked)
        self.createActions()
        self.createMenus()
        self.setCentralWidget(widget)
        self.idfmodel = None


        

    def createActions(self):
        self.exit = QtGui.QAction('Exit', self)
        self.exit.setShortcut('Ctrl+Q')
        self.exit.setStatusTip('Exit application')
        self.connect(self.exit, QtCore.SIGNAL('triggered()'), QtCore.SLOT('close()'))
        
        self.writefile = QtGui.QAction('Write File', self)
        self.writefile.setShortcut('Ctrl+W')
        self.writefile.setStatusTip('Write an IDF File')
        self.connect(self.writefile, QtCore.SIGNAL('triggered()'), self.writeFile)

        self.openfile = QtGui.QAction('Open File', self)
        self.openfile.setShortcut('Ctrl+O')
        self.openfile.setStatusTip('Open an IDF File')
        self.connect(self.openfile, QtCore.SIGNAL('triggered()'), self.openFile)

        self.newobj = QtGui.QAction('New Object',self)
        self.newobj.setShortcut('Ctrl+N')
        self.newobj.setStatusTip('Create New Object')
        self.connect(self.newobj, QtCore.SIGNAL('triggered()'), self.newobject)

    def createMenus(self):
        menubar = self.menuBar()
        filem = menubar.addMenu('&File')
        filem.addAction(self.openfile)
        filem.addAction(self.writefile)
        filem.addAction(self.exit)
        objm = menubar.addMenu('&Objects')
        objm.addAction(self.newobj)



    def querybuttonclicked(self):
        self.model.query(self.querylist.currentIndex(),self.queryline.text())


    def writeFile(self):
        destfile = QtGui.QFileDialog.getSaveFileName(self,"Save To", ".", "*.idf");
        try:
            fh = open(destfile,'w')
        except:
            return
        for rec in self.idf.idflist:
            fh.write(rec.__str__()+"\n")
        fh.close()
        


    def openFile(self):
        self.fileName = QtGui.QFileDialog.getOpenFileName(self,"Open IDF File", ".", "*.idf *.IDF");
        self.idf.openIdf(self.fileName)
        self.model.reset()

    def newobject(self):
        newdialog = newclassdialog.newClassDialog()
        result = newdialog.exec_()


    def classActivated(self,model):
        
        idf = model.internalPointer().data
        text = idf.getClassnameIDD() + ' : '+ idf.getName()
        self.classviewname.setText(text)
        self.idfmodel = idfabstractmodel.idfClassModel(idf)
        self.classview.setModel(self.idfmodel)



if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    window = idfmodeltest()
    window.show()
    sys.exit(app.exec_())

        

