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

# File : idfeditor.py
import sys
from PyQt4 import QtGui, QtCore
from gwidget import GWidget

# We start a new class here
# derived from QMainWindow
# A calendar is displayed and clicking on a date makes this date be displayed on the label on the bottom

class idfeditor(QtGui.QMainWindow):
    def __init__(self):
        QtGui.QMainWindow.__init__(self)
       	myWidget = GWidget()
        self.setCentralWidget(myWidget)
        self.setWindowTitle('IDF Creator')
        self.setGeometry(QtGui.QDesktopWidget().screenGeometry())
        self.statusBar().showMessage('Click on Scene to start')
  


if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    window = idfeditor()
    window.show()
    sys.exit(app.exec_())
