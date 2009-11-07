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

    def __init__(self,model):
        QtCore.QObject.__init__(self,None)
        #list of ranges that denote zones, in [[0][9] meaning z starting at zero to nine, etc.
        #the view only knows of floor levels. Details within zones, roof, ceiling, walls, floor is handled by the zone
        self.zlist = []
        self.tempzlist = []

    def insertZ(self,z):
        self.tempzlist.append(z)

    def setLayersFromTemp(self):
        self.setLayers(self.tempzlist)

  
    def setLayers(self,zlist):
        print zlist
        self.zlist = []

        l = 0
        if len(zlist) == 0:
            return
        b = []
        for l in zlist:
            if not self.fin(l[0],b):
                b.append(l[0])
            if not self.fin(l[1],b):
                b.append(l[1])
                
        b = sorted(b)


        if len(b) == 2:
            self.zlist.append([b[0],b[1]])
            return

        for c,i in enumerate(b):
            print c,i
            if c < 1:
                continue

            #starts at third
            self.zlist.append([b[c-1],b[c]])

        self.trigger.emit()

    def fin(self,item,lst):
        #in, but close not equal
        for i in lst:
            if abs(item - i) < 0.001:
                return True

        return False

    def layerCount(self):
        return len(self.zlist)

    def layer(self):
        if len(self.zlist) == 0:
            return [0.0,0.0]
        return [self.zlist[0][0],self.zlist[len(self.zlist)-1][1]]
    


if __name__ == "__main__":
    z = zLayers(None)
    z.setLayers([[0,18],[0,9],[9,18],[18,27]])
    print z.zlist
    print z.layers()

