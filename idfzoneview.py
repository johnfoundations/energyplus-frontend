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

from PyQt4 import QtCore, QtGui


class zLayers():
    def __init__(self,model):
        self.model = model
        self.model.setZLayerHandler(self)
        #list of ranges that denote zones, in [[0][9] meaning z starting at zero to nine, etc.
        #the view only knows of floor levels. Details within zones, roof, ceiling, walls, floor is handled by the zone
        zlist = []

    def layers(self):
        #returns the number of layers within the zlist
        l = 0
        if len(zlist) == 0:
            return l
        b = zlist[0][0]
        for l in zlist:
            

class idfZoneView(QtGui.QGraphicsView):
    def __init__(self,scene,parent = None):
        QtGui.QGraphicsView.__init__ (self,scene, parent )
        self.setLayer()

    def setLayer(self):
        #
        pass


    #logic for viewing.
    #view looks after view angle and depth. The view tells the scene to zoom in or out
    #the scene tells the view if there is any zoom levels either way.

    #When a building is loaded, and all the vertice points are created in the surfaceitems, the tree
    #can be analyzed to extract floor and roof levels. A list is available to display a graphic, and allow
    #selection. If the view is from an angle, zooming isn't allowed. If it is from parallel to the ground,
    #the scene would show the outside layers of the building, and zooming would penetrate layer by layer.