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
import zlayers

                
            
            

class idfZoneView(QtGui.QWidget):
    def __init__(self,parent = None):
        QtGui.QWidget.__init__ (self, parent )
        self.scene = None
        self.model = None
        self.layerhandler =  zlayers.zLayers(self.model)
        #viewpoint is unit vertice defining a point from which the scene is viewed in x = east, y = north, z = up
        self.viewpoint = [0.0,0.0,1.0]
        self.layer = 0.0
        self.buildView()


    def buildView(self):
        #lays out widget
        self.view = QtGui.QGraphicsView()
        self.scene = QtGui.QGraphicsScene()
        self.view.setScene(self.scene)

        hlayout = QtGui.QHBoxLayout(self)
        self.tools = QtGui.QToolBar()
        self.tools.setOrientation(Qt)
        hlayout.addWidget(self.tools)
        vl = QtGui.QVBoxLayout()
        vl.addWidget(self.view)
        self.commandedit = QtGui.QLineEdit()
        vl.addWidget(self.commandedit)
        hlayout.addLayout(vl)
        self.orient = QtGui.QToolBar()
        hlayout.addWidget(self.orient)

    def createActions(self):
        pass
        



    def setModel(self,model):
        self.model =  model
        self.layerhandler.setModel(self.model)
        self.model.reset()
    


    #logic for viewing.
    #view looks after view angle and depth. The view tells the scene to zoom in or out
    #the scene tells the view if there is any zoom levels either way.

    #When a building is loaded, and all the vertice points are created in the surfaceitems, the tree
    #can be analyzed to extract floor and roof levels. A list is available to display a graphic, and allow
    #selection. If the view is from an angle, zooming isn't allowed. If it is from parallel to the ground,
    #the scene would show the outside layers of the building, and zooming would penetrate layer by layer.