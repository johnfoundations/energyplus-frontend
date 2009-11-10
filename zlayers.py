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

from PyQt4 import QtCore

class zLayers(QtCore.QObject):

    layerchange = QtCore.pyqtSignal()

    def __init__(self):
        QtCore.QObject.__init__(self,None)
        #list of z values
        self.zlist = []
        self.current = 0 #contains index to current layer

    def insertZ(self,z):
        if z not in self.zlist:
            self.zlist.append(z)
            self.zlist = sorted(self.zlist)
            self.current = len(self.zlist)-1


    def layerCount(self):
        return len(self.zlist)

    def inc(self):
        if self.current != len(self.zlist)-1:
            self.current = self.current + 1
            
        return self.zlist[self.current]
            
    def dec(self):
        if self.current != 0:
            self.current = self.current - 1
            
        return self.zlist[self.current]

    def current(self):
        return self.zlist[self.current]