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
import iddclass
import sys
import re
import idfdata
import idfabstractmodel
import idfmodeldelegate
import newclassdialog
import loadclassdialog

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
        self.view.sizePolicy().setHorizontalPolicy(QtGui.QSizePolicy.Fixed)
        
        splitter = QtGui.QSplitter()
        widget = QtGui.QWidget()

        mainhbox = QtGui.QHBoxLayout(widget)
        self.viewwidget = QtGui.QWidget()
        vbox = QtGui.QVBoxLayout()
        vbox.setSizeConstraint(QtGui.QLayout.SetMinAndMaxSize)
        hbox = QtGui.QHBoxLayout()

        hbox.addWidget(self.querylist)
        hbox.addWidget(self.queryline)

        vbox.addLayout(hbox)
        vbox.addWidget(self.querybutton)
        vbox.addWidget(self.view)
        self.viewwidget.setLayout(vbox)
        splitter.addWidget(self.viewwidget)
#        mainhbox.addWidget(viewwidget)
        classvbox = QtGui.QVBoxLayout()
        self.classviewname = QtGui.QLabel()
        self.classview = QtGui.QTableView()
        self.delegate  = idfmodeldelegate.idfClassDelegate()
        self.classview.setItemDelegate(self.delegate)
        self.classview.setEditTriggers(QtGui.QAbstractItemView.AllEditTriggers)
        self.classview.horizontalHeader().setStretchLastSection(True)
        
        classvbox.addWidget(self.classviewname)
        classvbox.addWidget(self.classview)
        mainhbox.addLayout(classvbox)
        splitter.addWidget(widget)
        self.connect(self.view, QtCore.SIGNAL('activated (QModelIndex)'),self.classActivated)
        
        self.connect(self.querybutton, QtCore.SIGNAL('clicked ( bool)'),self.querybuttonclicked)
        self.createActions()
        self.createMenus()
        self.setCentralWidget(splitter)
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

        self.loadobj = QtGui.QAction('Load Objects',self)
        self.loadobj.setShortcut('Ctrl+L')
        self.loadobj.setStatusTip('Load Object from IDF File')
        self.connect(self.loadobj, QtCore.SIGNAL('triggered()'), self.loadobject)

        self.delobj = QtGui.QAction('Delete Selected Object',self)
        self.delobj.setShortcut('Ctrl+D')
        self.delobj.setStatusTip('Delete Selected Object')
        self.connect(self.delobj, QtCore.SIGNAL('triggered()'), self.delobject)


    def createMenus(self):
        menubar = self.menuBar()
        filem = menubar.addMenu('&File')
        filem.addAction(self.openfile)
        filem.addAction(self.writefile)
        filem.addAction(self.exit)
        objm = menubar.addMenu('&Objects')
        objm.addAction(self.newobj)
        objm.addAction(self.loadobj)
        objm.addAction(self.delobj)


    def sizeTree(self):
        width = self.view.sizeHintForColumn(0) + self.view.sizeHintForColumn(1)
        if width < 200:
            width = 200
        print width
        self.viewwidget.setMaximumWidth(width)


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
        self.sizeTree()

    def newobject(self):
        newdialog = newclassdialog.newClassDialog()
        result = newdialog.exec_()
        if result:
            newclasses = newdialog.selected
            for n  in newclasses:
                evalstr = 'iddclass.'+ re.sub(r'[:-]','_',str(n)) +'()'
                classinstance = eval (evalstr)
                self.idf.insertRecord(classinstance)

            self.model.reset()
            self.sizeTree()
                

    def loadobject(self):
        loaddialog = loadclassdialog.loadClassDialog()
        result = loaddialog.exec_()
        if result:
            for c in loaddialog.destidf.idflist:
                self.idf.insertRecord(c)
            self.model.reset()
            self.sizeTree()



    def classActivated(self,index):
        
        idf = index.internalPointer().data
        text = idf.getClassnameIDD() + ' : '+ idf.getName()
        self.classviewname.setText(text)
        self.idfmodel = idfabstractmodel.idfClassModel(idf,index.model())
        self.classview.setModel(self.idfmodel)


    def delobject(self):
        indexlist = self.view.selectedIndexes()
        if len(indexlist) == 0:
            return
        msgBox = QtGui.QMessageBox()
        msgBox.setText("Do you want to delete the selected objects?")
        msgBox.setStandardButtons(QtGui.QMessageBox.Yes | QtGui.QMessageBox.Cancel)
        msgBox.setDefaultButton(QtGui.QMessageBox.Cancel)
        if msgBox.exec_():
            for i in indexlist:
                if i.column() == 0:
                    self.idf.deleteRecord(i.internalPointer().data)
            self.model.reset()


if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    window = idfmodeltest()
    window.show()
    sys.exit(app.exec_())

        

