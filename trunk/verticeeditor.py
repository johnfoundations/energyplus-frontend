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
import idfzonemodel
import idfzoneview

class idfmodeltest(QtGui.QMainWindow):
    def __init__(self):
        QtGui.QMainWindow.__init__(self)
        self.tabs = QtGui.QTabWidget()
        self.idfmodel = None
        self.zoom = 10

        self.createActions()
        self.createMenus()

        self.tabs.addTab(self.verticePage(),'IDF Surface Editor')

        self.setCentralWidget(self.tabs)
        self.sizeTree()





    def verticePage(self):
        self.tvwidget = QtGui.QWidget()
        splitter = QtGui.QSplitter()
        self.idf = idfdata.idfData()
        self.model = idfzonemodel.idfZoneModel(None,self.idf)

        vl = QtGui.QHBoxLayout(self.tvwidget)
        self.zonelist = QtGui.QTreeView()
        self.zonelist.setModel(self.model)
        vl.addWidget(self.zonelist)
        splitter.addWidget(self.tvwidget)
        
        
        self.verticeview = idfzoneview.idfZoneView()
        self.verticeview.setModel(self.model)
        splitter.addWidget(self.verticeview)
        return splitter

    def sizeTree(self):
        width = self.zonelist.sizeHintForColumn(0) + self.zonelist.sizeHintForColumn(1)
        if width < 200:
            width = 200
        print width
        self.tvwidget.setMaximumWidth(width)



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

        self.zoomin = QtGui.QAction('Zoom In', self)
        self.zoomin.setShortcut('Ctrl+I')
        self.zoomin.setStatusTip('Zoom In')
        self.connect(self.zoomin, QtCore.SIGNAL('triggered()'), self.zoominslot)

        self.zoomout = QtGui.QAction('Zoom Out', self)
        self.zoomout.setShortcut('Ctrl+T')
        self.zoomout.setStatusTip('Zoom Out')
        self.connect(self.zoomout, QtCore.SIGNAL('triggered()'), self.zoomoutslot)

        def zoominslot(self):
            print 'zoominslot'
            self.zoom = self.zoom + 0.5
            self.rescale()

        def zoomoutslot(self):
            print 'zoomoutslot'
            self.zoom = self.zoom - 0.5
            self.rescale()

        def rescale(self):
            print 'rescale'
            print self.zoom
            oldMatrix = self.view.matrix();
            self.view.resetMatrix();
            self.view.translate(oldMatrix.dx(), oldMatrix.dy())
            self.view.scale(self.zoom,self.zoom);


    def createMenus(self):
        menubar = self.menuBar()
        filem = menubar.addMenu('&File')
        filem.addAction(self.openfile)
#        filem.addAction(self.savefile)
#        filem.addAction(self.saveasfile)
        filem.addAction(self.exit)
#        objm = menubar.addMenu('&Objects')
#        objm.addAction(self.newobj)
#        objm.addAction(self.loadobj)
#        objm.addAction(self.delobj)
        filem.addAction(self.zoomin)
        filem.addAction(self.zoomout)




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
        self.model.reset()
        self.rescale()


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

    def zoominslot(self):
        print 'zoominslot'
        self.zoom = self.zoom + 10
        self.rescale()

    def zoomoutslot(self):
        print 'zoomoutslot'
        self.zoom = self.zoom - 10
        self.rescale()

    def rescale(self):
        print 'rescale'
        print self.zoom
        oldMatrix = self.verticeview.view.matrix();
        self.verticeview.view.resetMatrix();
        self.verticeview.view.translate(oldMatrix.dx(), oldMatrix.dy())
        self.verticeview.view.scale(self.zoom,self.zoom);



if __name__ == "__main__":

    app = QtGui.QApplication(sys.argv)
    window = idfmodeltest()
    window.show()
    sys.exit(app.exec_())



