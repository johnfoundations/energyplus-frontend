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
import idfeditorclasslistpage

class idfmodeltest(QtGui.QMainWindow):
    def __init__(self):
        QtGui.QMainWindow.__init__(self)
        self.tabs = QtGui.QTabWidget()
        self.parentmodel = None
        self.sortorderlist = [-1,-1]
        self.filename = ''
        self.readSettings()
        self.createActions()
        self.createMenus()
        self.idfdata = idfdata.idfData()
        self.idfgroups = []
        self.tabs.addTab(self.headerPage(),'IDF File Description')
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

        self.runsim = QtGui.QAction('&Run Simulation',self)
        self.runsim = QtGui.setShortCut('Ctrl+S')
        self.runsim = QtGui.setStatusTip('Run Simulation on IDF File')
        self.connect(self.runsim, QtCore.SIGNAL('triggered()'), self.runsimulation)


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
        simm = menubar.addMenu('&Simulation')
        simm.addAction(self.runsim)




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
        self.idfdata.comments = str(self.commentedit.toPlainText())
        self.idfdata.writeIdf(destfile)


    def openFile(self):
        self.fileName = QtGui.QFileDialog.getOpenFileName(self,"Open IDF File", ".", "*.idf *.IDF");
        self.idfdata.openIdf(self.fileName)
        self.parentmodel = idfabstractmodel.idfAbstractModel(self.idfdata)
        self.commentedit.setText(self.idfdata.comments)
        for g in self.idfdata.groups:
            t = idfeditorclasslistpage.idfEditorClassListPage(g,self.parentmodel)
            self.idfgroups.append(t)
            self.tabs.addTab(t,g)
        

    def newobject(self):
        newdialog = newclassdialog.newClassDialog()
        result = newdialog.exec_()
        if result:
            newclasses = newdialog.selected
            for n  in newclasses:
                self.idfdata.insertRecordByClassname(n)

            self.idfdata.buildDependsTree()
            self.idfdata.datachanged.emit()
            for t in self.idfgroups:
                t.model.reset()
                t.sizeTree()
                

    def loadobject(self):
        loaddialog = loadclassdialog.loadClassDialog()
        result = loaddialog.exec_()
        if result:
            for c in loaddialog.destidf.idflist:
                self.idfdata.insertRecord(c)

            self.idfdata.buildDependsTree()
            self.model.reset()
            self.sizeTree()



    def delobject(self):
        indexlist = self.tabs.currentWidget().view.selectedIndexes()
        if len(indexlist) == 0:
            return
        msgBox = QtGui.QMessageBox()
        msgBox.setText("Do you want to delete the selected objects?")
        msgBox.setStandardButtons(QtGui.QMessageBox.Yes | QtGui.QMessageBox.Cancel)
        msgBox.setDefaultButton(QtGui.QMessageBox.Cancel)
        if msgBox.exec_():
            for i in indexlist:
                if i.column() == 0:
                    self.idfdata.deleteRecord(i.internalPointer().data)
            self.idfdata.datachanged.emit()
            for t in self.idfgroups:
                t.model.reset()
                t.sizeTree()

    def runsimulation(self):
        #get filename of idf
        if self.filename = '':
            self.saveAsFile()
        
        epdir = ''
        settings = QtCore.QSettings("EPlus", "IDF Editor")    
        if settings.value("epfolder",'') == '':
            #find energyplus folder
            import fnmatch
            import os
            foundep = False
            
            if os.name() == 'posix':
                epdir = '/usr/local/'
                for f in os.listdir(epdir):
                    if fnmatch.fnmatch(f, 'Energy*'):
                        epdir += f
                        foundep = True
                        
            else:
                print 'Operating System Not Supported'
                return
                
            if not foundep:
                epdir = QtGui.QFileDialog.getExistingDirectory(self, 'Find Energy Plus Installation Folder',
                                                 "/",QtGui.QFileDialog.ShowDirsOnly)
                                                 
            settings.setValue('epfolder',epdir)
            
            
        else:
            epdir = settings.value('epfolder','')
            
        if epdir == '':
            return
            
        weatherfile = ''
        if settings.value('weather','') == '':
            weatherfile = QtGui.QFileDialog.getOpenFileName(self,"Open IDF File", epdir, "*.epw *.EPW")
            
        else:
            weatherfile = settings.value('weather','')
            
        if weatherfile == '':
            return
                
        #change to idf file directory
        os.chdir(os.dirname(self.filename))
        
        #run energyplus
        
                
        

if __name__ == "__main__":

    app = QtGui.QApplication(sys.argv)
    window = idfmodeltest()
    window.show()
    sys.exit(app.exec_())

        

