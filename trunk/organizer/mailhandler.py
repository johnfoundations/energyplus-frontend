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

from PyKDE4 import kdecore
from PyQt4 import QtCore, QtGui
import os
import sys
import config
from smptclass import Smtp


class mailerThread(QtCore.QThread):
    def __init__(self, parent = None):
        QtCore.QThread.__init__(self, parent)
        #set up variables
        self.mailercontinue = True
        config.setupConfig()




    def run(self):
        while self.mailercontinue:
            if len(os.listdir(str(config.getDestFolder())+'/pdf/spool')) > 0:
                filename = os.listdir(str(config.getDestFolder())+'/pdf/spool')[0]
                filepath = str(config.getDestFolder())+'/pdf/spool/'+ filename
                try:
                    smtp = Smtp(str(config.getSMTPServer()), str(config.getSMTPUser()), str(config.getSMTPPassword()),587)
                except:
                    self.mailercontinue = False
                    print 'error logging in'
                    self.terminate()

                smtp.subject(filename+' attached')
                smtp.message('Book keeping data attached.')
                smtp.from_addr(str(config.getSMTPUser()))
                print 'sending email to',str(config.getDestEmail())
                smtp.rcpt_to(str(config.getDestEmail()))

                smtp.attach(filepath)
                try:
                    smtp.send()
                    #move file
                    os.rename(filepath,str(config.getDestFolder())+'/pdf/save/'+filename)
                    print 'sending completed signal'
                    self.emit(QtCore.SIGNAL('fileSent(QString)'),os.path.splitext(filename)[0])
                except:
                    print 'send failed'

                self.sleep(2)

            else:
                #print 'thread sleeping'
                self.sleep(10)


if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    t = mailerThread()
    t.start()
    sys.exit(app.exec_())

