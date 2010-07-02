# -*- coding: utf-8 -*-
"""***************************************************************************
*   Copyright (C) 2010 by Derek Kite   *
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

#from PyKDE4 import kdeui
#from PyKDE4 import kdecore
from PyQt4 import QtCore, QtGui
import sane
import config
from PIL import Image, ImageQt
import scanpage
import mailhandler
import os
import crop
import paperlist
import subprocess
import sys



class scanWindow(QtGui.QMainWindow):
    def __init__(self):
        super(scanWindow, self).__init__()
        self.readSizeSettings()
        print 'email thread'
        self.setUpEmailThread()
        self.tabwidget = QtGui.QTabWidget()

        #self.tabwidget.addTab(self.scannerPage(),'Scanner')


        self.setCentralWidget(self.tabwidget)
        dwidget = QtGui.QApplication.desktop()
        print 'scannerthread'
        self.createScannerToolbar()
        self.setupMenus()
        self.setUpScannerThread()
        print 'loadImageFiles'
        self.loadImageFiles()

    def readSizeSettings(self):
        settings = QtCore.QSettings("ScannSave", "Viewer")
        size = settings.value("size", QtCore.QSize(1000, 600)).toSize()
        self.resize(size)

    def writeSizeSettings(self):
        settings = QtCore.QSettings("ScannSave", "Viewer");
        settings.setValue("size", self.size());
 
    def closeEvent(self,event):
        print 'mainwindow closeEvent'
        self.writeSizeSettings()
        event.accept()
 

    def createScannerToolbar(self):
        print 'createScannerToolbar'
        self.scannertoolbar = self.addToolBar('Scanner')
        print 'create statusbar'
        self.scannerstatusbar = self.statusBar()
        print 'seticonsize'
        self.scannertoolbar.setIconSize(QtCore.QSize(64,64))

        print 'create scan action'
        self.scan = QtGui.QAction('Start S&can', self)
        self.scan.setShortcut('Ctrl+S')
        self.scan.setStatusTip('Start Scanner')
        self.scan.setIcon(QtGui.QIcon('/usr/share/icons/default.kde4/128x128/devices/scanner.png'))
        self.connect(self.scan, QtCore.SIGNAL('triggered()'), self.scanButtonClicked)

        print 'create email action'
        self.send = QtGui.QAction('E&mail', self)
        self.send.setShortcut('Ctrl+E')
        self.send.setStatusTip('Send by email')
        self.send.setIcon(QtGui.QIcon('/usr/share/icons/default.kde4/128x128/actions/mail-send.png'))
        self.connect(self.send, QtCore.SIGNAL('triggered()'), self.sendButtonClicked)

        print 'create delete action'
        self.delete = QtGui.QAction('D&lete', self)
        self.delete.setShortcut('Ctrl+D')
        self.delete.setStatusTip('Delete current image')
        self.delete.setIcon(QtGui.QIcon('/usr/share/icons/default.kde4/128x128/actions/edit-bomb.png'))
        self.connect(self.delete, QtCore.SIGNAL('triggered()'), self.deleteButtonClicked)

        self.settings = QtGui.QAction('S&ettings',self)
        self.settings.setShortcut('Ctrl-T')
        self.settings.setStatusTip('Email settings')
        self.connect(self.settings, QtCore.SIGNAL('triggered()'), self.settingsButtonClicked)


        print 'add actions'

        self.scannertoolbar.addAction(self.scan)
        self.scannertoolbar.addAction(self.send)

        print 'create comboboxes'
        self.scanner = QtGui.QComboBox()
        self.source = QtGui.QComboBox()
        self.paper = QtGui.QComboBox()

        print 'add widgets'
        self.scannertoolbar.addWidget(self.scanner)
        self.scannertoolbar.addWidget(self.source)
        self.scannertoolbar.addWidget(self.paper)
        self.scannertoolbar.addAction(self.delete)
        #self.connect(self.source, QtCore.SIGNAL("currentIndexChanged (int)"),self.sourceChanged)
        print 'createpaperlist'
        self.createPaperList()
        print 'createScannerToolbar done'

    def setupMenus(self):
        menubar = self.menuBar()
        filem = menubar.addMenu('&File')
        filem.addAction(self.settings)




    def setUpEmailThread(self):
        print 'setUpEmailThread'
        config.setupConfig()
        if config.getMailAutostart():
            print 'setUpEmailThread auto start on'
            self.mailthread = mailhandler.mailerThread()
            self.mailthread.start()
            self.connect(self.mailthread,QtCore.SIGNAL('fileSent(QString)'),self.cleanupFile)

    def sendButtonClicked(self):
        self.tabwidget.currentWidget().sendEmail()

    def deleteButtonClicked(self):
        if self.tabwidget.currentWidget().removeCurrentImage() == 0:
            self.tabwidget.removeTab(self.tabwidget.currentIndex())

    def settingsButtonClicked(self):
        dialog = config.configDialog()
        dialog.exec_()
        self.setUpEmailThread()



    def loadImageFiles(self):
        path = str(config.getScansFolder())
        imagefolderlist = os.listdir(path)
        print 'imagefolderlist',imagefolderlist
        imagefolderlist.sort()
        print imagefolderlist
        for f in imagefolderlist:
            print f
            if os.path.isdir(path+'/'+f):
                print 'isdir',f
                self.currentpagewidget=scanpage.scanPage(f)
                self.currentpagewidget.identifier = f
                self.tabwidget.addTab(self.currentpagewidget,f)
                imagedir = os.listdir(path+'/'+f)
                imagedir.sort()
                for imf in imagedir:
                    print imf
                    if os.path.splitext(imf)[1] != '.png':
                        continue

                    self.currentpagewidget.addImage(path+'/'+f+'/'+imf)


    def cleanupFile(self,s):
        #s is name. Used after sending.
        print 'cleanupFile',s

        for c in range(0,self.tabwidget.count()):
            if self.tabwidget.widget(c).identifier == s:
                self.tabwidget.widget(c).saveImageFiles()
                self.tabwidget.removeTab(c)
                break



    def scannerPage(self):
         # Create widget with vertical box layout manager
        layout = kdeui.KVBox()

        # Create push button and add to layout
        self.scanbutton = kdeui.KPushButton("Begin Scan", layout)
        self.scanbutton.setEnabled(False)

        self.connect(self.scanbutton, QtCore.SIGNAL("clicked()"),
                               self.scanButtonClicked)




        #self.source.setExclusive(True)
        self.sourcebox = QtGui.QGroupBox(layout)
        self.sourcelayout = QtGui.QVBoxLayout()


        return layout


    def scanButtonClicked(self):
        print "starting scan!"
        self.scan.setEnabled(False)
        self.currentpagewidget = scanpage.scanPage()
        self.tabwidget.addTab(self.currentpagewidget,self.currentpagewidget.identifier)
        self.sourceChanged(self.source.currentIndex())
        self.paperChanged(self.paper.currentIndex())
        self.scannerthread.setFolder(self.currentpagewidget.identifier)
        self.scannerthread.beginScan()
        print 'scan started'


    def startMailThread(self):
        if not self.mailthread.running():
            self.mailthread.start()



    def handleImage(self,filename,i):
        print 'handleImage'
        self.currentpagewidget.addImage(str(filename),i)
        self.scan.setEnabled(True)
        print 'imagehandled'


    def updateScannerList(self,slist):
        print 'checkForScanner'
        #disconnect signal
        self.disconnect(self.scanner, QtCore.SIGNAL("currentIndexChanged (int)"),self.scannerChanged)
        self.scannerlist = slist
        print self.scannerlist, len(self.scannerlist)
        if self.scanner.count() > 0:
            current = self.scanner.currentIndex()
            self.scanner.clear()

        else:
            current = 0

        for s in self.scannerlist:
            self.scanner.insertItem(self.scanner.count()+1,s[2])

        self.scanner.setCurrentIndex(current)

        self.scannerChanged(current)

        self.connect(self.scanner, QtCore.SIGNAL("currentIndexChanged (int)"),self.scannerChanged)


    def scannerChanged(self,index):
        print "scannerchanged"
        if len(self.scannerlist) > 0:
            self.scannerthread.setScanner(self.scannerlist[index][0])


    def updateSourceList(self,sourcelist):
        print 'updateSourceList',sourcelist
        self.scansourcelist = sourcelist
        if self.source.count() > 0:
            current = self.source.currentIndex()
            self.source.clear()

        else:
            current = 0

        for i,c in enumerate(self.scansourcelist):
            self.source.insertItem(i,c)

        self.source.setCurrentIndex(current)
        #self.sourceChanged(current)
        self.scan.setEnabled(True)


    def createPaperList(self):
        #in mm from scanner
        self.papertypelist = []
        for k in paperlist.paperlist.keys():
            self.papertypelist.append(k)
            self.paper.insertItem(len(self.papertypelist)+1,k)


#        self.paper.setCurrentIndex(0)
        #self.connect(self.paper, QtCore.SIGNAL("currentIndexChanged (int)"),self.paperChanged)

    def updatePaperList(self,s):
        print 'updatePaperList',s
        self.paper.setCurrentIndex(self.papertypelist.index(s))



    def sourceChanged(self,index):
        print 'sourcechanged'
        self.scannerthread.setSource(self.scansourcelist[index])

    def paperChanged(self,index):
        print 'paperchanged'
        self.scannerthread.setPaper(self.papertypelist[index])

    def setUpScannerThread(self):
        self.scannerthread = scannerThread()
        print 'thread created'
#        self.connect(self.scannerthread, QtCore.SIGNAL("finished()"), self.updateUi)
#        self.connect(self.scannerthread, QtCore.SIGNAL("terminated()"), self.updateUi)
        self.connect(self.scannerthread, QtCore.SIGNAL("scanfinished(QString,int)"), self.handleImage,QtCore.Qt.QueuedConnection)
        self.connect(self.scannerthread, QtCore.SIGNAL("scannerlist(list)"), self.updateScannerList)
        self.connect(self.scannerthread, QtCore.SIGNAL("sourcelist(list)"),  self.updateSourceList)
        self.connect(self.scannerthread, QtCore.SIGNAL("papersize(QString)"), self.updatePaperList)
        print 'signals and slots connected'
        self.scannerthread.threadInitialize()
        print 'thread initialized'


class scannerThread(QtCore.QThread):
    def __init__(self, parent = None):
        QtCore.QThread.__init__(self, parent)
        #set up variables
        print 'scannerThread init'
        self.scancount = 0
        self.currentscanner = ''

    def threadInitialize(self):
        print 'threadInitialize'
        self.currentscanner = ''
        sane.init()
        self.scannerlist = sane.get_devices()
        print self.scannerlist, len(self.scannerlist)
        self.emit(QtCore.SIGNAL('scannerlist(list)'),self.scannerlist)


    def setFolder(self,folder):
        print 'setFolder',folder
        self.destfolder=folder

    def setSource(self,source):
        print 'setSource',source
        self.source = source

    def setPaper(self,paper):
        self.paper = paper

    def setScanner(self,scanner):
        print 'setScanner',scanner
        if scanner != self.currentscanner:
            self.currentscanner = scanner
            self.scandev = sane.open(scanner)
            source = self.scandev['source']
            self.resolution = self.scandev.resolution
            self.emit(QtCore.SIGNAL('sourcelist(list)'),source.constraint)
            self.emit(QtCore.SIGNAL('papersize(QString)'),'Letter')
            self.scandev.close()

    def beginScan(self):
        print 'beginScan'
        self.start()

    def cancelScan(self):
        pass

    def __del__(self):
        self.scancount = 0
        self.wait()

    def run(self):
        dest = config.getScansFolder()+self.destfolder
        scriptpath = sys.path[0]
        print scriptpath
        args = ['python',scriptpath+'/scanprocess.py','--scanner='+self.currentscanner, \
               '--paper='+self.paper,'--source='+self.source,'--dest='+dest]
        print 'start subprocess',args
        sproc = subprocess.Popen(args,stdout=subprocess.PIPE,stderr=subprocess.PIPE,)
        print 'readline'
        for line in sproc.stdout:
            s = line.strip()
            print 'filename',s
            #s is filename
            self.emit(QtCore.SIGNAL('scanfinished(QString,int)'),s,self.resolution)
        print 'finished readline'
        print sproc.stderr.read()



