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

from PyKDE4 import kdeui
from PyKDE4 import kdecore
from PyQt4 import QtCore, QtGui
import sane
import ImageQt
import Image
import config
import pdfgen
import os
import cStringIO


class scanPage(QtGui.QWidget):
    def __init__(self,identifier = None):
        super(scanPage, self).__init__()

        writepath = config.getDestFolder()
        emaildest = config.getDestEmail()
        self.gwidget = 0
        self.workingtab = 0
  #      self.createActions()
        self.layout = QtGui.QVBoxLayout()
#        self.toolbar = QtGui.QToolBar('Tools')
 #       self.toolbar.addAction(self.savefile)
#        self.toolbar.addAction(self.sendemail)
 #       self.layout.addWidget(self.toolbar)
        self.setLayout(self.layout)
        self.imagecount = 0
        if identifier == None:
            self.identifier = config.timeStamp()
        else:
            self.identifier = identifier
        self.sending = False
        if not os.path.exists(str(config.getDestFolder())+'/scans/'+self.identifier):
            print 'path does not exist', str(config.getDestFolder())+'/scans/'+self.identifier
            os.mkdir(str(config.getDestFolder())+'/scans/'+self.identifier)


    def removeCurrentImage(self):
        print 'removeCurrentImage imagecount',self.imagecount
        if self.imagecount == 1:
            self.gwidget.deleteFile()
            os.rmdir(str(config.getDestFolder())+'/scans/'+self.identifier)
            return 0

        elif self.imagecount == 0:
            os.rmdir(str(config.getDestFolder())+'/scans/'+self.identifier)
            return 0

        else:
            self.workingtab.currentWidget().deleteFile()
            self.workingtab.removeTab(self.workingtab.currentIndex())
            self.imagecount -= 1
            return 1


    def addImage(self,filename,dpi):
        #qt image
        if self.imagecount == 0:
            print 'addImage 0'
            self.gwidget = scanImage(filename)
            self.gwidget.setDPI(dpi)
            self.layout.addWidget(self.gwidget)
            self.imagecount += 1

        else:
            print 'addImage already an image'
            #create tab
            if self.imagecount == 1:
                print 'addImage imagecount', self.imagecount
                self.workingtab = QtGui.QTabWidget()
                self.workingtab.setTabPosition(QtGui.QTabWidget.East)
                self.layout.removeWidget(self.gwidget)
                self.layout.addWidget(self.workingtab)
                self.workingtab.addTab(self.gwidget,self.identifier)

            print 'addImage inserting new'
            imgclass = scanImage(filename)
            imgclass.setDPI(dpi)
            self.workingtab.addTab(imgclass,imgclass.name)
            self.imagecount += 1


    def createActions(self):

        self.exit = QtGui.QAction('E&xit', self)
        self.exit.setShortcut('Ctrl+Q')
        self.exit.setStatusTip('Exit application')
        self.connect(self.exit, QtCore.SIGNAL('triggered()'), QtCore.SLOT('close()'))

        self.savefile = QtGui.QAction('&Save as PDF', self)
        self.savefile.setShortcut('Ctrl+S')
        self.savefile.setStatusTip('Write PDF File to Disk')
        self.savefile.setIcon(QtGui.QIcon('/usr/share/icons/default.kde4/32x32/actions/document-save.png'))
        self.connect(self.savefile, QtCore.SIGNAL('triggered()'), self.saveFile)

        self.sendemail = QtGui.QAction('Sen&d', self)
        self.sendemail.setShortcut('Ctrl+D')
        self.sendemail.setStatusTip('Send file by email')
        self.sendemail.setIcon(QtGui.QIcon('/usr/share/icons/default.kde4/32x32/actions/mail-send.png'))
        self.connect(self.sendemail, QtCore.SIGNAL('triggered()'), self.sendEmail)

    def sendEmail(self):
        if not self.sending:
            self.sending = True
        else:
            return
        print 'sendEmail',self.imagecount
        imglist = []
        if self.imagecount == 1:
            if not self.gwidget == 0:
                self.gwidget.saveText()
                imglist.append(self.gwidget.getImageFile())
                dpi = self.gwidget.dpi

        else:
            #multiple
            if self.imagecount == 0:
                return
            print self.workingtab.count()
            for c in range(0,self.workingtab.count()):
                print 'getting multiple images',c
                self.workingtab.widget(c).saveText()
                imglist.append(self.workingtab.widget(c).getImageFile())
                dpi = self.workingtab.widget(c).dpi

        print imglist
        print str(config.getDestFolder())+'/pdf/spool/'+str(self.identifier)+'.pdf'
        pdfgen.createPDF(str(config.getDestFolder())+'/pdf/spool/'+str(self.identifier)+'.pdf',imglist,dpi)
#        self.emit(QtCore.SIGNAL('spoolready()'))

    def saveFile(self):
        pass

    def saveImageFiles(self):
        os.rename(str(config.getDestFolder())+'/scans/'+self.identifier,str(config.getDestFolder())+'/imagesave/'+self.identifier)


class scanImage(QtGui.QWidget):
    def __init__(self,filename):
        super(scanImage, self).__init__()

        self.qtimg = QtGui.QImage()
        self.qtimg.load(filename)
        self.filename = filename
        path,pfile = os.path.split(filename)
        print path,pfile
        ffile,ext = os.path.splitext(pfile)
        print ffile,ext
        self.txtfilename = path+'/'+ffile+'.txt'
        self.name = ffile
        self.layout = QtGui.QVBoxLayout()
        self.description = QtGui.QTextEdit()
        self.connect(self.description,QtCore.SIGNAL('textChanged()'),self.descriptionEdited)
        self.savetimer = QtCore.QTimer()
        self.connect(self.savetimer, QtCore.SIGNAL('timeout()'),self.saveText)
        self.layout.addWidget(self.description)
        gwidget = QtGui.QGraphicsView()
        gscene = QtGui.QGraphicsScene()
        gwidget.setScene(gscene)
        print 'scanImage addPixmap'
        gscene.addPixmap(QtGui.QPixmap.fromImage(self.qtimg))
        print 'scanImage addPixmap done'
        self.layout.addWidget(gwidget)
        self.setLayout(self.layout)

        #load text files
        if os.path.exists(self.txtfilename):
            print 'txt file exists', self.txtfilename
            f = open(self.txtfilename,'r')
            txt = f.read()
            f.close()
            self.description.setText(txt)

    def getPil(self):
        imagebuffer = QtCore.QBuffer()
        imagebuffer.open(QtCore.QIODevice.ReadWrite)
        self.qtimg.save(imagebuffer, "PNG")

        strio = cStringIO.StringIO()
        strio.write(imagebuffer.data())
        imagebuffer.close()
        strio.seek(0)
        pil_im = Image.open(strio)
        return pil_im

    def setDPI(self,dpi):
        print 'setDPI',dpi
        self.dpi = dpi

    def descriptionEdited(self):
        if not self.savetimer.isActive():
            self.savetimer.setSingleShot(True)
            self.savetimer.start(15000)

    def getImageFile(self):
        return self.filename

    def deleteFile(self):
        print 'deleteFile', self.filename
        os.remove(self.filename)

    def saveText(self):
        if self.description.document().characterCount() > 0:
            print 'saveText'
            f = open(self.txtfilename,'w')
            f.write(str(self.description.toPlainText()))
            f.close()


