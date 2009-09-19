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

surfaceView = 0
surfaceViewNorth = 1
surfaceViewWest = 2
surfaceViewSouth = 3
surfaceViewEast = 4

#the assumptions on vertices is that all is xyz, and north is adjusted



class surfacePolygonItem(QtGui.QGraphicsPolygonItem):
    def __init__(self,parent=None):
        QtGui.QGraphicsPolygonItem.__init__ (self,parent)

    def setPolygon(self,polygon):
        #reverse y in array
        for e in polygon:
            e[1] = e[1] * -1

        QtGui.QGraphicsPolygonItem.setPolygon(QtGui.QPolygonF(polygon))







        
    