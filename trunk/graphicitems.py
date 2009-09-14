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

verticeclasses = "BuildingSurface:Detailed","Wall:Detailed","RoofCeiling:Detailed","Floor:Detailed","FenestrationSurface:Detailed",\
                 "Shading:Zone:Detailed","Shading:Site:Detailed","Shading:Building:Detailed"
        #all have vertices

zoneclasses = ("Zone",)

surfaceelementclasses = "GlazedDoor:Interzone","GlazedDoor","Door","Door:Interzone","Window:Interzone","Window"
        #multiplier,xy,length,height

azimuthtiltclasses = "Ceiling:Adiabatic","Ceiling:Interzone","Floor:GroundContact","Floor:Adiabatic","Floor:Interzone",\
                     "Roof","Wall:Exterior","Wall:Adiabatic","Wall:Underground","Wall:Interzone","Shading:Site",\
                     "Shading:Building"
        #azimuth,tilt,xyz,length,width


class surfacePolygonItem(QtGui.QGraphicsPolygon):
    def __init__(self,parent,treeitem):
        QtGui.GraphicsPolygonItem.__init__ (self,parent=0)
        self.treeitem = treeitem
        self.polygonlist = []
        self.buildPolygons()

    def buildPolygons(self):
        #builds an array of polygons representing the view of the surface from the 5 views
        if self.treeitem.data.getClassnameIDD() in verticeclasses:
            self.buildVerticePolygons()

        if self.treeitem.data.getClassnameIDD() in surfaceelementclasses:
            self.buildSurfaceElementPolygons()

        if self.treeitem.data.getClassnameIDD() in azimuthtiltclasses:
            self.buildAzimuthTiltPolygons()

        if self.treeitem.data.getClassnameIDD() in zoneclasses:
            self.buildZonePolygons()


    def setActivePolygon(self, surfaceview = 0):
        self.setPolygon(self.polygonlist[surfaceView])


    def buildVerticePolygons(self):

    def buildSurfaceElementPolygons(self):

    def buildZonePolygons(self):

    def buildAzimuthTiltPolygons(self):
        





        
    