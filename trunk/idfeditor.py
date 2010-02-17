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
import runsimulation

class idfmodeltest(QtGui.QMainWindow):
    def __init__(self):
        QtGui.QMainWindow.__init__(self)
        self.tabs = QtGui.QTabWidget()
        self.tabs.setMovable(True)
        self.tabs.setTabsClosable(True)
        self.log = None
        self.parentmodel = None
        self.sortorderlist = [-1,-1]
        self.filename = ''
        self.signalmapper = QtCore.QSignalMapper(self)
        self.connect(self.signalmapper,QtCore.SIGNAL('mapped(int)'),self.grouptoggle)
        self.connect(self.tabs,QtCore.SIGNAL('tabCloseRequested (int)'),self.tabclosetab)
        self.readSettings()
        self.createActions()
        self.createMenus()
        self.idfdata = idfdata.idfData()
        self.idfgroupsdict = dict()
        self.idfgroupsmenu = []
        
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

        self.closefile = QtGui.QAction('&Close File', self)
        self.closefile.setShortcut('Ctrl+C')
        self.closefile.setStatusTip('Close IDF file and all tabs')
        self.connect(self.closefile, QtCore.SIGNAL('triggered()'), self.closeFile)

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
        self.runsim.setShortcut('Ctrl+S')
        self.runsim.setStatusTip('Run Simulation on IDF File')
        self.connect(self.runsim, QtCore.SIGNAL('triggered()'), self.runsimulation)

        self.tabshowall = QtGui.QAction('Sho&w all Tabs',self)
        self.tabshowall.setShortcut('Ctrl+W')
        self.tabshowall.setStatusTip('Show all hidden tabs')
        self.connect(self.tabshowall,QtCore.SIGNAL('triggered()'),self.tabShowAll)
        
        


    def createMenus(self):
        menubar = self.menuBar()
        filem = menubar.addMenu('&File')
        filem.addAction(self.openfile)
        filem.addAction(self.savefile)
        filem.addAction(self.saveasfile)
        filem.addAction(self.closefile)
        filem.addAction(self.exit)
        objm = menubar.addMenu('&Objects')
        objm.addAction(self.newobj)
        objm.addAction(self.loadobj)
        objm.addAction(self.delobj)
        simm = menubar.addMenu('&Simulation')
        simm.addAction(self.runsim)
        self.groupTabMenu = menubar.addMenu('&Tabs')
        self.groupTabMenu.addAction(self.tabshowall)




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
        self.idfdata.comments = self.commentedit.toPlainText()
        self.idfdata.writeIdf(destfile)


    def openFile(self):
        self.fileName = QtGui.QFileDialog.getOpenFileName(self,"Open IDF File", ".", "*.idf *.IDF");
        print self.fileName
        if self.fileName == '':
            return
        self.idfdata.openIdf(self.fileName)
        self.parentmodel = idfabstractmodel.idfAbstractModel(self.idfdata)
        self.tabs.addTab(self.headerPage(),'IDF File Description')
        self.commentedit.setText(self.idfdata.comments)
        for g in self.idfdata.groups:
            t = idfeditorclasslistpage.idfEditorClassListPage(g,self.parentmodel)
            self.idfgroupsdict[g] = t
            self.tabs.addTab(t,g)
            self.createGroupAction(g)
        

        
    def closeFile(self):
        self.saveFile()
        while self.tabs.count() > 0:
            #self.tabs.widget(self.tabs.currentIndex())
            self.tabs.removeTab(self.tabs.currentIndex())
            
        self.idfdata.closeData()


    def newobject(self):
        newdialog = newclassdialog.newClassDialog()
        result = newdialog.exec_()
        if result:
            newclasses = newdialog.selected
            for n  in newclasses:
                self.idfdata.insertRecordByClassname(n)

            self.idfdata.buildDependsTree()
            self.idfdata.datachanged.emit()
            self.updateTabs()

    def createGroupAction(self,group):
        a = QtGui.QAction(group,self)
        self.idfgroupsmenu.append(a)
        a.setStatusTip('Click to Toggle Tab '+group)
        a.setCheckable(True)
        a.setChecked(True)
        self.connect(a, QtCore.SIGNAL('toggled (bool)'),self.signalmapper, QtCore.SLOT('map()'))
        self.signalmapper.setMapping(a,len(self.idfgroupsmenu) - 1)
        self.groupTabMenu.addAction(a)


    def updateTabs(self):
        for g in self.idfdata.groups:
            if g in self.idfgroupsdict:
                self.idfgroupsdict[g].model.reset()
                self.idfgroupsdict[g].sizeTree()
            else:
                t = idfeditorclasslistpage.idfEditorClassListPage(g,self.parentmodel)
                self.idfgroupsdict[g] = t
                self.tabs.addTab(t,g)
                
            if g not in self.idfgroupsmenu:
                self.createGroupAction(g)

    def loadobject(self):
        loaddialog = loadclassdialog.loadClassDialog()
        result = loaddialog.exec_()
        if result:
            for c in loaddialog.destidf.idflist:
                self.idfdata.insertRecord(c)

            self.idfdata.buildDependsTree()
            self.idfdata.datachanged.emit()
            self.updateTabs()


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

    def tabShowAll(self):
        print 'tabshowall'

    def tabclosetab(self,i):
        if self.tabs.tabText(i) != 'IDF File Description':
            self.tabs.removeTab(i)


    def grouptoggle(self,i):
        print 'grouptoggle',i
        ga = self.idfgroupsmenu[i]
        g = str(ga.text())
        tabexists = False
        #find tab
        for c in range(self.tabs.count()):
            print c,self.tabs.tabText(c),g
            if g == self.tabs.tabText(c):
                if not ga.isChecked():
                    self.tabs.removeTab(c)
                    
                return
                
        if ga.isChecked():
            self.tabs.addTab(self.idfgroupsdict[g],g)
            

    def runsimulation(self):
        #get filename of idf
        if self.filename == '':
            self.saveAsFile()
        
        if self.log == None:
            self.log = runsimulation.LogWidget()
            self.tabs.insertTab(0,self.log,'Simulation Results')
            
        self.tabs.setCurrentIndex(0)
        self.simulation = runsimulation.simulation(self.filename,self.log)
        
        
                
        

if __name__ == "__main__":

    app = QtGui.QApplication(sys.argv)
    window = idfmodeltest()
    window.show()
    sys.exit(app.exec_())

        

