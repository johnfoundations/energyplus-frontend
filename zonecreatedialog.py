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

from PyQt4 import QtCore,QtGui
import graphicitems

class zoneCreateDialog(QtGui.QDialog):
    def __init__ (self, parent = None):
        QtGui.QDialog.__init__(self,parent)
        mainlayout = QtGui.QVBoxLayout(self)
        zl = QtGui.QGridLayout()
        self.zonename = QtGui.QLineEdit()
        zl.addWidget(QtGui.QLabel("Zone Name"),0,0)
        zl.addWidget(self.zonename,0,1)
        zl.addWidget(QtGui.QLabel("Units"),0,2)
        self.units = QtGui.QComboBox()
        self.units.addItems(('SI','IP'))
        zl.addWidget(self.units,0,3)
        zl.addWidget(QtGui.QLabel('Zone Origin x,y,z'),1,0)
        self.origin = QtGui.QLineEdit()
        zl.addWidget(self.origin,1,1)
        zl.addWidget(QtGui.QLabel('Zone Height Z axis'),2,0)
        self.zoneheight = QtGui.QLineEdit()
        zl.addWidget(self.zoneheight,2,1)
        mainlayout.addLayout(zl)
        buttongroup = QtGui.QButtonGroup()
        self.bywidthlength = QtGui.QRadioButton('By Width and Length')
        self.widthlengthgroupbox = QtGui.QGroupBox()
        lwl = QtGui.QHBoxLayout()
        lwl.addWidget(QtGui.QLabel('Width, Y axis'))
        self.widthlengthwidth = QtGui.QLineEdit()
        lwl.addWidget(self.widthlengthwidth)
        lwl.addWidget(QtGui.QLabel('Length, X axis'))
        self.widthlengthlength = QtGui.QLineEdit()
        lwl.addWidget(self.widthlengthlength)
        self.widthlengthgroupbox.setLayout(lwl)
        mainlayout.addWidget(self.bywidthlength)
        mainlayout.addWidget(self.widthlengthgroupbox)
        self.bypoints = QtGui.QRadioButton('By Points, Start at bottom left, clockwise. x,y,z')
        mainlayout.addWidget(self.bypoints)
        buttongroup.addButton(self.bywidthlength)
        buttongroup.addButton(self.bypoints)
        self.bypointsgroupbox = QtGui.QGroupBox()
        ptl = QtGui.QHBoxLayout()
        ptlc = QtGui.QVBoxLayout()
        ptlc.addWidget(QtGui.QLabel('Point coordinates:'))
        self.pcoord = QtGui.QLineEdit()
        ptlc.addWidget(self.pcoord)
        ptlc.addStretch()
        ptl.addLayout(ptlc)
        ptlbutt = QtGui.QVBoxLayout()
        self.addbutton = QtGui.QPushButton('Add Point')
        self.delbutton = QtGui.QPushButton('Delete Point')
        ptlbutt.addWidget(self.addbutton)
        ptlbutt.addWidget(self.delbutton)
        ptlbutt.addStretch()
        ptl.addLayout(ptlbutt)
        self.pointlist = QtGui.QListWidget()
        ptl.addWidget(self.pointlist)
        self.bypointsgroupbox.setLayout(ptl)
        mainlayout.addWidget(self.bypointsgroupbox)
        
        
        
if __name__ == "__main__":
    import sys
    from PyQt4 import QtGui

    app = QtGui.QApplication(sys.argv)
    view = zoneCreateDialog()
    view.show()
    sys.exit(app.exec_())
        
        
        