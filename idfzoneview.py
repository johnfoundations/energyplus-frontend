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
import zonescene

                
            
            

class idfZoneView(QtGui.QWidget):
    def __init__(self,parent = None):
        QtGui.QWidget.__init__ (self, parent )
        self.scene = None
        self.model = None
        self.layerhandler =  zlayers.zLayers(self.model)
        self.connect(self.layerhandler, QtCore.SIGNAL('layerchange()'), self.buildingLayerChange)
        #viewpoint is unit vertice defining a point from which the scene is viewed in x = east, y = north, z = up
        self.viewpoint = [0.0,0.0,0.0]
        self.layer = 0.0
        self.buildView()


    def buildView(self):
        #lays out widget
        self.view = QtGui.QGraphicsView()
        self.scene = zonescene.zoneScene()
        self.view.setScene(self.scene)

        hlayout = QtGui.QHBoxLayout(self)
        self.tools = QtGui.QToolBar()
        self.tools.setOrientation(QtCore.Qt.Vertical)
        hlayout.addWidget(self.tools)
        vl = QtGui.QVBoxLayout()
        vl.addWidget(self.view)
        self.commandedit = QtGui.QLineEdit()
        vl.addWidget(self.commandedit)
        hlayout.addLayout(vl)
        self.orient = QtGui.QToolBar()
        self.orient.setOrientation(QtCore.Qt.Vertical)
        hlayout.addWidget(self.orient)
        self.createToolActions()
        self.createNavigateActions()

    def createToolActions(self):
        self.snappoint = QtGui.QAction('Snap to Point', self)
        self.snappoint.setShortcut('Alt+P')
        self.snappoint.setStatusTip('Toggle Snap to Point')
        self.connect(self.snappoint, QtCore.SIGNAL('triggered()'), self.snapToPoint)

        self.snaporth = QtGui.QAction('Snap Orthogonal', self)
        self.snaporth.setShortcut('Alt+O')
        self.snaporth.setStatusTip('Toggle Snap to Orthogonal')
        self.connect(self.snaporth, QtCore.SIGNAL('triggered()'), self.snapToOrth)

        self.snapline = QtGui.QAction('Snap to Line', self)
        self.snapline.setShortcut('Alt+L')
        self.snapline.setStatusTip('Toggle Snap to Line')
        self.connect(self.snapline, QtCore.SIGNAL('triggered()'), self.snapToLine)

        self.addsurface = QtGui.QAction('Add Surface', self)
        self.addsurface.setShortcut('Alt+S')
        self.addsurface.setStatusTip('Add Surface to Zone')
        self.connect(self.addsurface, QtCore.SIGNAL('triggered()'), self.addToSurface)

        self.addwindow = QtGui.QAction('Add Window', self)
        self.addwindow.setShortcut('Alt+W')
        self.addwindow.setStatusTip('Add Window to Surface')
        self.connect(self.addwindow, QtCore.SIGNAL('triggered()'), self.addToWindow)

        self.addzone = QtGui.QAction('Add Zone', self)
        self.addzone.setShortcut('Alt+Z')
        self.addzone.setStatusTip('Add New Zone')
        self.connect(self.addzone, QtCore.SIGNAL('triggered()'), self.addToZone)

        self.tools.addAction(self.snappoint)
        self.tools.addAction(self.snaporth)
        self.tools.addAction(self.snapline)
        self.tools.addAction(self.addsurface)
        self.tools.addAction(self.addwindow)
        self.tools.addAction(self.addzone)
        


    def createNavigateActions(self):

        self.north = QtGui.QAction('View North Face', self)
        self.north.setShortcut('Alt+UpArrow')
        self.north.setStatusTip('View North Face of Building')
        self.connect(self.north, QtCore.SIGNAL('triggered()'), self.viewNorth)

        self.south = QtGui.QAction('View South Face', self)
        self.south.setShortcut('Alt+DownArrow')
        self.south.setStatusTip('View South Face of Building')
        self.connect(self.south, QtCore.SIGNAL('triggered()'), self.viewSouth)

        self.east = QtGui.QAction('View East Face', self)
        self.east.setShortcut('Alt+RightArrow')
        self.east.setStatusTip('View East Face of Building')
        self.connect(self.east, QtCore.SIGNAL('triggered()'), self.viewEast)

        self.west = QtGui.QAction('View West Face', self)
        self.west.setShortcut('Alt+LeftArrow')
        self.west.setStatusTip('View West Face of Building')
        self.connect(self.west, QtCore.SIGNAL('triggered()'), self.viewWest)
        
        self.up = QtGui.QAction('View Down', self)
        self.up.setShortcut('Alt+.')
        self.up.setStatusTip('View Down on Building')
        self.connect(self.up, QtCore.SIGNAL('triggered()'), self.viewUp)

        self.drillin = QtGui.QAction('View Next Layer In', self)
        self.drillin.setShortcut('Alt+<')
        self.drillin.setStatusTip('View Next Layer into Building')
        self.connect(self.drillin, QtCore.SIGNAL('triggered()'), self.viewDrillIn)

        self.drillout = QtGui.QAction('View Nest Layer Out', self)
        self.drillout.setShortcut('Alt+>')
        self.drillout.setStatusTip('View Next Layer Out of Building')
        self.connect(self.drillout, QtCore.SIGNAL('triggered()'), self.viewDrillOut)

        self.orient.addAction(self.north)
        self.orient.addAction(self.south)
        self.orient.addAction(self.east)
        self.orient.addAction(self.west)
        self.orient.addAction(self.up)
        self.orient.addAction(self.drillin)
        self.orient.addAction(self.drillout)
        

    def setModel(self,model):
        print 'verticeview set model'
        self.model =  model
        self.layerhandler.setModel(self.model)
        self.scene.setModel(self.model)
        self.model.reset()
    

    def buildingLayerChange(self):
        print 'buildingLayerChange'
        self.layer = self.layerhandler.layer()[1]
        self.scene().z = self.layer


    def snapToPoint(self):
        pass

    def snapToOrth(self):
        pass

    def snapToLine(self):
        pass

    def addToSurface(self):
        pass

    def addToWindow(self):
        pass

    def addToZone(self):
        pass

    def viewNorth(self):
        pass

    def viewSouth(self):
        pass

    def viewEast(self):
        pass

    def viewWest(self):
        pass

    def viewUp(self):
        pass

    def viewDrillIn(self):
        pass

    def viewDrillOut(self):
        pass


















    #logic for viewing.
    #view looks after view angle and depth. The view tells the scene to zoom in or out
    #the scene tells the view if there is any zoom levels either way.

    #When a building is loaded, and all the vertice points are created in the surfaceitems, the tree
    #can be analyzed to extract floor and roof levels. A list is available to display a graphic, and allow
    #selection. If the view is from an angle, zooming isn't allowed. If it is from parallel to the ground,
    #the scene would show the outside layers of the building, and zooming would penetrate layer by layer.