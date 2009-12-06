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
import loadclassdialog

class idfmodeltest(QtGui.QMainWindow):
    def __init__(self):
        QtGui.QMainWindow.__init__(self)
        self.tabs = QtGui.QTabWidget()
        self.idfmodel = None
        self.sortorderlist = [-1,-1]
        self.filename = ''
        self.readSettings()
        self.createActions()
        self.createMenus()
        
        self.tabs.addTab(self.headerPage(),'IDF File Description')
        self.tabs.addTab(self.classPage(), 'IDF Data')
        self.setCentralWidget(self.tabs)


    def readSettings(self):
        settings = QtCore.QSettings("EPlus", "IDF Editor")
        size = settings.value("size", QtCore.QSize(1000, 600)).toSize()
        self.resize(size)

    def writeSettings(self):
        settings = QtCore.QSettings("EPlus", "IDF Editor");
        settings.setValue("size", self.size());
 
    def closeEvent(self,event):
        print 'mainwindow closeEvent'
        self.writeSettings()
        event.accept()

    def classPage(self):
        self.idf = idfdata.idfData()
        self.model = idfabstractmodel.idfAbstractModel(self.idf)

        self.querylist = QtGui.QComboBox()
        self.querylist.addItems(['All','Classname','Name','Group','Dependancy','Reference','Fieldname','Fieldvalue'])

        self.queryline = QtGui.QLineEdit()
        self.querybutton = QtGui.QPushButton("Query")

        self.view = QtGui.QTreeView()
        self.view.setModel(self.model)
        self.view.sizePolicy().setHorizontalPolicy(QtGui.QSizePolicy.Fixed)
        self.view.header().setClickable(True)
        
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
        self.classview.horizontalHeader().setClickable(True)
        self.classview.setSelectionMode(QtGui.QAbstractItemView.NoSelection)
        classvbox.addWidget(self.classviewname)
        classvbox.addWidget(self.classview)
        mainhbox.addLayout(classvbox)
        splitter.addWidget(widget)
        self.connect(self.view, QtCore.SIGNAL('activated (QModelIndex)'),self.classActivated)
        
        self.connect(self.querybutton, QtCore.SIGNAL('clicked ( bool)'),self.querybuttonclicked)
        self.connect(self.view.header(),QtCore.SIGNAL('sectionClicked ( int )'),self.viewlistsort)
        self.connect(self.classview.horizontalHeader(),QtCore.SIGNAL('sectionClicked ( int )'),self.changeunits)

        return splitter
        

    def headerPage(self):
        widget = QtGui.QWidget()
        vl = QtGui.QVBoxLayout(widget)
        self.commentedit = QtGui.QTextEdit()
        vl.addWidget(self.commentedit)
        return widget
        

    def createActions(self):
        self.exit = QtGui.QAction('E&xit', self)
        self.exit.setShortcut('Ctrl+Q')
        self.exit.setStatusTip('Exit application')
        self.connect(self.exit, QtCore.SIGNAL('triggered()'), QtCore.SLOT('close()'))
        
        self.savefile = QtGui.QAction('&Save', self)
        self.savefile.setShortcut('Ctrl+S')
        self.savefile.setStatusTip('Write IDF File to Disk')
        self.connect(self.savefile, QtCore.SIGNAL('triggered()'), self.saveFile)

        self.saveasfile = QtGui.QAction('Save &As', self)
        self.saveasfile.setShortcut('Ctrl+A')
        self.saveasfile.setStatusTip('Prompt to Write IDF File to Disk')
        self.connect(self.saveasfile, QtCore.SIGNAL('triggered()'), self.saveAsFile)

        self.openfile = QtGui.QAction('&Open File', self)
        self.openfile.setShortcut('Ctrl+O')
        self.openfile.setStatusTip('Open an IDF File')
        self.connect(self.openfile, QtCore.SIGNAL('triggered()'), self.openFile)

        self.newobj = QtGui.QAction('&New Object',self)
        self.newobj.setShortcut('Ctrl+N')
        self.newobj.setStatusTip('Create New Object')
        self.connect(self.newobj, QtCore.SIGNAL('triggered()'), self.newobject)

        self.loadobj = QtGui.QAction('&Load Objects',self)
        self.loadobj.setShortcut('Ctrl+L')
        self.loadobj.setStatusTip('Load Object from IDF File')
        self.connect(self.loadobj, QtCore.SIGNAL('triggered()'), self.loadobject)

        self.delobj = QtGui.QAction('&Delete Selected Object',self)
        self.delobj.setShortcut('Ctrl+D')
        self.delobj.setStatusTip('Delete Selected Object')
        self.connect(self.delobj, QtCore.SIGNAL('triggered()'), self.delobject)


    def createMenus(self):
        menubar = self.menuBar()
        filem = menubar.addMenu('&File')
        filem.addAction(self.openfile)
        filem.addAction(self.savefile)
        filem.addAction(self.saveasfile)
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


    def saveFile(self):
        if self.filename == '':
            self.filename = QtGui.QFileDialog.getSaveFileName(self,"Save To", ".", "*.idf");

        if self.filename != '':
            self.writeFile(self.filename)
            

    def saveAsFile(self):
        self.filename = QtGui.QFileDialog.getSaveFileName(self,"Save To", ".", "*.idf");
        if self.filename != '':
            self.writeFile(self.filename)
        

    def writeFile(self,destfile):
        self.idf.comments = str(self.commentedit.toPlainText())
        self.idf.writeIdf(destfile)


    def openFile(self):
        self.fileName = QtGui.QFileDialog.getOpenFileName(self,"Open IDF File", ".", "*.idf *.IDF");
        self.idf.openIdf(self.fileName)
        self.commentedit.setText(self.idf.comments)
        self.model.reset()
        self.sizeTree()

    def newobject(self):
        newdialog = newclassdialog.newClassDialog()
        result = newdialog.exec_()
        if result:
            newclasses = newdialog.selected
            for n  in newclasses:
                self.idf.insertRecordByClassname(n)

            self.idf.buildDependsTree()
            self.model.reset()
            self.sizeTree()
                

    def loadobject(self):
        loaddialog = loadclassdialog.loadClassDialog()
        result = loaddialog.exec_()
        if result:
            for c in loaddialog.destidf.idflist:
                self.idf.insertRecord(c)

            self.idf.buildDependsTree()
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

    def viewlistsort(self,column):
        if self.sortorderlist[column] != 0:
            self.sortorderlist[column] = 0
        else:
            self.sortorderlist[column] = 1

        self.model.sort(column,self.sortorderlist[column])
    
    def changeunits(self,column):
        print 'changeunits',column
        if column == 0:
            if self.idfmodel != None:
                self.idfmodel.toggleUnits()


if __name__ == "__main__":

    app = QtGui.QApplication(sys.argv)
    window = idfmodeltest()
    window.show()
    sys.exit(app.exec_())

        

