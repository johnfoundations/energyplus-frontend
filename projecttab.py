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
from PyQt4 import QtGui, QtCore
import sys



class projectTab(QtGui.QWidget):
  def __init__(self, parent=None):
    QtGui.QWidget.__init__(self, parent)
    layout = QtGui.QVBoxLayout(self)
    layout.addWidget(QtGui.QLabel('Project Name:'))
    self.projectname = QtGui.QLineEdit()
    layout.addWidget(self.projectname)
    layout.addWidget(QtGui.QLabel('Project Details: Name, address, etc'))
    self.projectdetails = QtGui.QTextEdit()
    layout.addWidget(self.projectdetails)
    layout.addWidget(QtGui.QLabel('Units:'))
    self.units = QtGui.QComboBox()
    self.units.addItems(['Imperial','Metric'])
    layout.addWidget(self.units)
    layout.addStretch()
    