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
import initwindow
#import config

#def createAboutData():
    #"""
    #Create a KAboutData with information about this application.
    #"""
    #return kdecore.KAboutData(
            ## Program name used internally
            #"hello",

            ## Catalog name
            #"",

            ## Displayable program name
            #kdecore.ki18n("Scan and Send"),

            ## Program version
            #"0.1.0",

            ## Short description about the program
            #kdecore.ki18n("An application that scans and emails a pdf"),

            ## Program license
            #kdecore.KAboutData.License_BSD,

            ## Copyright statement
            #kdecore.ki18n ("(c) 2010 Derek Kite"),

            ## Free form text
            #kdecore.ki18n("Free form text\nsupporting newlines"),

            ## Home page address for this program
            #"",

            ## Bug report email address
            #"derekkite@gmail.com",
            #)









def main():

    #print 'createaboutdata'
    #about = createAboutData()
    #print 'kcmdlineargs'
    #kdecore.KCmdLineArgs.init(sys.argv, about)
    #print 'kapplication'
    app = QtGui.QApplication(sys.argv)
    print 'initwindow'
#    config.setupConfig()

    win = initwindow.scanWindow()
    win.show()

# INSERT APP CODE HERE

    # Start event loop
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()











