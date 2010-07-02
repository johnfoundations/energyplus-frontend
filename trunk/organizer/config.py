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


#from PyKDE4 import kdecore
#from PyKDE4 import kdeui
from PyQt4 import QtGui, QtCore
import sys
import os
import keyring


class configDialog(QtGui.QDialog):
    def __init__(self):
        super(configDialog, self).__init__()
        self.setWindowTitle( "Email Configuration" )

        layout = QtGui.QVBoxLayout(self)
        layout.addWidget(QtGui.QLabel('Destination Folder for storing files:'))
        self.destfolder = QtGui.QLineEdit()
        layout.addWidget(self.destfolder)
        layout.addWidget(QtGui.QLabel('Email address to send files to:'))
        self.destemail = QtGui.QLineEdit()
        layout.addWidget(self.destemail)
        self.smtpserver = QtGui.QLineEdit()
        layout.addWidget(QtGui.QLabel('Email SMTP Server:'))
        layout.addWidget(self.smtpserver)
        self.smtpaccount = QtGui.QLineEdit()
        layout.addWidget(QtGui.QLabel('SMTP login account:'))
        layout.addWidget(self.smtpaccount)
        self.smtppassword = QtGui.QLineEdit()
        self.smtppassword.setEchoMode(QtGui.QLineEdit.PasswordEchoOnEdit)
        layout.addWidget(QtGui.QLabel('SMTP login password:'))
        layout.addWidget(self.smtppassword)
        self.autostart = QtGui.QCheckBox('Start email sending automatically')
        layout.addWidget(self.autostart)
        
#        self.setMainWidget( widget )
        
        
        buttonBox = QtGui.QDialogButtonBox(QtGui.QDialogButtonBox.Ok | QtGui.QDialogButtonBox.Cancel)
        layout.addWidget(buttonBox)
        
        self.connect(buttonBox, QtCore.SIGNAL('accepted()'),self.saveconfig)
        self.connect(buttonBox, QtCore.SIGNAL('rejected()'),self.reject)

        self.destfolder.setText(getDestFolder())
        self.destemail.setText(getDestEmail())
        self.smtpserver.setText(getSMTPServer())
        self.smtpaccount.setText(getSMTPUser())
        self.smtppassword.setText(getSMTPPassword())
        self.autostart.setChecked(getMailAutostart())
            
 

    def saveconfig(self):
        print 'saveconfig'
        settings = QtCore.QSettings("ScannSave", "Email")
        settings.setValue('SaveFolder',self.destfolder.text())
        settings.setValue('Email',self.destemail.text())
        settings.setValue('Server',self.smtpserver.text())
        settings.setValue('User',self.smtpaccount.text())
        keyring.set_password('email_login', 'scanandsave', str(self.smtppassword.text()))
        settings.setValue('Autostart',self.autostart.isChecked())
        self.accept()


config = None
destgroup = None

def getDestFolder():
    settings = QtCore.QSettings("ScannSave", "Email")
    return settings.value('SaveFolder',os.path.expanduser('~/scanandsave')).toString()

def getDestEmail():
    settings = QtCore.QSettings("ScannSave", "Email")
    return settings.value('Email',' ').toString()

def getSMTPServer():
    settings = QtCore.QSettings("ScannSave", "Email")
    return settings.value('Server','smtp.gmail.com').toString()

def getSMTPUser():
    settings = QtCore.QSettings("ScannSave", "Email")
    return settings.value('User','').toString()

def getSMTPPassword():
    p = keyring.get_password('email_login','scanandsave')
    if p == None:
        p = ''
    return p
    
def getMailAutostart():
    settings = QtCore.QSettings("ScannSave", "Email")
    return settings.value('Autostart',False).toBool()

def setupConfig():
    #set up configuration
    if getDestEmail() == ' ':
        dialog = configDialog()
        dialog.exec_()

    if not os.path.exists(getDestFolder()):
        os.mkdir(getDestFolder())
        os.mkdir(getDestFolder()+'/pdf')
        os.mkdir(getDestFolder()+'/pdf/spool')
        os.mkdir(getDestFolder()+'/pdf/save')
        os.mkdir(getDestFolder()+'/scans')
        os.mkdir(getDestFolder()+'/imagesave')



def runConfigDialog():
    dialog = configDialog()
    dialog.exec_()


def timeStamp():
    import time
    tuple_time = time.localtime()
    secs = tuple_time[5]
    hours = tuple_time[3]
    if int(hours) in range(10):
        hours = "0%s" %hours
    minutes = tuple_time[4]
    if int(minutes) in range(10):
        minutes = "0%s" %minutes
    day = tuple_time[2]
    month = tuple_time[1]
    year = tuple_time[0]
    scan = 'scan'
    time_ = "%s-%s-%s-%s-%s:%s:%s" %(scan, year, month, day, hours, minutes,secs)
    return time_

def getSpoolFolder():
    return getDestFolder()+'/pdf/spool/'

def getSaveFolder():
    return getDestFolder()+'/pdf/save/'

def getScansFolder():
    return getDestFolder()+'/scans/'

def getImageSaveFolder():
    return getDestFolder()+'/imagesave/'

def getUniqueFilename(path,identifier,ext):
    pass


def createAboutData():

    return kdecore.KAboutData(
        # Program name used internally
        "hello",

        # Catalog name
        "",

        # Displayable program name
        kdecore.ki18n("Scan and Send"),

        # Program version
        "0.1.0",

        # Short description about the program
        kdecore.ki18n("An application that scans and emails a pdf"),

        # Program license
        kdecore.KAboutData.License_BSD,

        # Copyright statement
        kdecore.ki18n ("(c) 2010 Derek Kite"),

        # Free form text
        kdecore.ki18n("Free form text\nsupporting newlines"),

        # Home page address for this program
        "",

        # Bug report email address
        "derekkite@gmail.com",
        )



if __name__ == '__main__':



    print 'init'
    about = createAboutData()
    kdecore.KCmdLineArgs.init(sys.argv,about)

    print 'kapplication'
    app = kdeui.KApplication()

    print 'setupconfig'
    setupConfig()


# INSERT APP CODE HERE

    # Start event loop
    sys.exit(app.exec_())

