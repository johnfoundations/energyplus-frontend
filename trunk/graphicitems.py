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
import math
import numpy
import zlayers

verticeclasses = "BuildingSurface:Detailed","Wall:Detailed","RoofCeiling:Detailed","Floor:Detailed","FenestrationSurface:Detailed",\
                 "Shading:Zone:Detailed","Shading:Site:Detailed","Shading:Building:Detailed"
        #all have vertices

zoneclasses = ("Zone",)

surfaceelementclasses = "GlazedDoor:Interzone","GlazedDoor","Door","Door:Interzone","Window:Interzone","Window"
        #multiplier,xy,length,height

azimuthwallclasses = "Wall:Exterior","Wall:Adiabatic","Wall:Underground","Wall:Interzone","Shading:Site",\
                     "Shading:Building"
        #azimuth,tilt,xyz,length,width

azimuthflatclasses = "Ceiling:Adiabatic","Ceiling:Interzone","Floor:GroundContact","Floor:Adiabatic","Floor:Interzone",\
                     "Roof"








class zoneItem(QtGui.QGraphicsPolygonItem):
    def __init__(self,parent=None):
        QtGui.QGraphicsPolygonItem.__init__ (self,parent)
        self.delegate = None


    def setDelegate(self,delegate):
        self.delegate = delegate
        self.delegate.setItem(self)

    def setZVisible(self,z):
        #if above z, set invisible, otherwise visible
        if self.delegate != None:
            self.setVisible(self.delegate.checkZ(z))

    def.setViewpoint(self,viewpoint):
        if self.delegate:
            self.delegate.setViewpoint(viewpoint)

class zoneAbstractDelegate(QtCore.QObject):
    def __init__(self,index,parent = None)
        QtCore.QObject.__init__(self,parent)
        self.item = None
        self.math = None
        self.verticelist = []
        self.rotatedverticelist = []
        if index.isValid():
            self.model = index.model()
            self.math = self.model.getMath()
            self.verticelist = self.createVerticeList()
            self.idfclass = index.internalPointer().data
            self.index = QtCore.QPersistentModelIndex(index)

        else:
            self.model = None
            self.idfclass = None
            self.index = QtCore.QPersistentModelIndex()

    def setItem(self,item):
        #link to qgraphicsitem
        self.item = item

    def createVerticeList(self):
        return self.model.data(index,idfzonemodel.IdfVerticeRole


    def.checkZ(self,z):
        #returns true if equal or less than z
        res = False
        for v in self.rotatedverticelist:
            if v[2] <= z:
                res = True

        return res
        
    def setViewpoint(self,viewpoint):
        
    def setPolygon(self,polygon):
        #reverse y in array
        p = QtGui.QPolygonF()
        for e in polygon:
            e[1] = e[1] * -1
            p.append(QtCore.QPointF(e[0],e[1]))

        self.item.setPolygon(p)


    def rotate3d(self,x,y,z):
        pass


    def getZPoints(self,zrange):
        #z is a number, any points at z are returned
        #above is boolean. if true then any points = and above, or higher are returned.
        #if false, any points equal and below
        zpts = []
        for v in self.rotatedverticelist:
            if zrange[0] >= v[2] or zrange[1] <= v[2]:
                zpts.append(v)

        return zpts

    def setZVisible(self,zrange):
        visible = False
        for v in self.rotatedverticelist:
            if v[2] < zrange[1]:
                visible = True
        print 'setZVisible', zrange,visible,self.rotatedverticelist
        self.setVisible(visible)
        self.setZValue(zrange[1])


class zoneDelegate(zoneAbstractDelegate):
        
        
    def rotate3d(self,x,y,z):
        print 'zoneitem rotate3d',x,y,z
        #rotate children and build z order
        zo = []
        ztree = self.treeparent.getZone(self.treeparent.idfclass.getName())
        for t in ztree[0].childItems:
            t.data.setPolygon([x,y,z])
            zo.append(t.data.getZ())
            for ch in t.childItems:
                ch.data.setPolygon([x,y,z])
                zo.append(ch.data.getZ())
        self.zorder.setLayers(zo)
        # now build polygon
        top = self.zorder.layer()[1]
        self.rotatedverticelist = []
        for t in ztree[0].childItems:
            self.rotatedverticelist = self.rotatedverticelist + t.graphicitem.getZPoints([top,top])
            for ch in t.childItems:
                self.rotatedverticelist = self.rotatedverticelist + ch.graphicitem.getZPoints([top,top])

        self.setPolygon(self.rotatedverticelist)

        
            

        
            

class surfacePolygonItem(abstractItem):
    def __init__(self,treeParent,math,parent=None):
        abstractItem.__init__(self,treeParent,math,parent)
        

        #x,y,z coordinates after rotation or any transformation
        self.rotatedverticelist = []
        if self.treeparent.idfclass.getClassnameIDD() in verticeclasses:
            self.buildVerticePolygons()

        if self.treeparent.idfclass.getClassnameIDD() in surfaceelementclasses:
            self.buildSurfaceElementPolygons()

        if self.treeparent.idfclass.getClassnameIDD() in azimuthwallclasses:
            self.buildWallPolygons()

        if self.treeparent.idfclass.getClassnameIDD() in azimuthflatclasses:
            self.buildFlatPolygons()

        if self.treeparent.idfclass.getClassnameIDD() in zoneclasses:
            self.buildZonePolygons()
      


    def buildVerticePolygons(self):
        #translate into lower left, clockwise
        #first get vertices
        vindex = 0
        vertices = []
        v = []
        for c,f in enumerate(self.treeparent.idfclass.fieldlist):
            if f.getFieldName() == 'Number of Vertices':
                vindex = c + 1
                ei = 0
                vi = 0
                continue

            if vindex > 0:
                v.append(float(f.getValue()))
                if ei == 2:
                    vertices.append(v)
                    v = []
                    ei = 0
                    continue
                ei = ei + 1


#        print self.idfclass.getName()
#        print vertices

        if self.surfaceitem.getGeometryRules()["Vertex Entry Direction"] == "Counterclockwise":
            vertices.reverse()
            first = vertices.pop()
            vertices.insert(0,first)

#        print 'direction corrected',
#        self.printVerticeList(vertices)

        rules = self.surfaceitem.getGeometryRules()["Starting Vertex Position"]
        if rules == "UpperLeftCorner" or "UpperRightCorner" or "LowerRightCorner":
#            print rules
            v1 = numpy.subtract(vertices[1],vertices[0])
            v2 = numpy.subtract(vertices[-1],vertices[0])
            v3 = numpy.cross(v1,v2)

            d = numpy.square(v3)
            lv3 = numpy.divide(v3,numpy.sqrt(numpy.sum(d)))
            d = numpy.square(v1)
            lv1 = numpy.divide(v1,numpy.sqrt(numpy.sum(d)))

            dot =  numpy.dot(lv1,[-0.7,-0.7,0])

            v4 = numpy.add(v3,[-0.7*v3[2]*numpy.sign(dot),-0.7*v3[2],-1*v3[2]])

            base = vertices[0]
            dist = 0
            #calculate largest distance between points
            for v in vertices:
                d = numpy.subtract(base,v)
                s = numpy.square(d)
                l = numpy.sqrt(numpy.sum(s))
                if l > dist:
                    dist = l

            bl = numpy.multiply(v4,dist)
            bottomleft = numpy.add(vertices[0],bl)
            dist = 0
            dindex = 0
            #find closest to bottom right
            for c,v in enumerate(vertices):
                d = numpy.subtract(base,v)
                s = numpy.square(d)
                l = numpy.sqrt(numpy.sum(s))
                if l > dist:
                    dist = l
                    dindex = c

            #resort vertices
 #           print 'resort',dindex,vertices
            if dindex > 0:
                vertices = vertices[dindex:len(vertices)] + vertices[0:dindex]
#            self. printVerticeList(vertices)

        if self.surfaceitem.getGeometryRules()["Coordinate System"] == "Relative" or "World":
            origin = self.getZoneOrigin()
        else:
            origin = [0.0,0.0,0.0]

        for v in vertices:
            print v,origin
            v[0] = v[0] + origin[0]
            v[1] = v[1] + origin[1]
            v[2] = v[2] + origin[2]

        self.verticelist = vertices



    def buildSurfaceElementPolygons(self):
        pass

    def buildZonePolygons(self):

        pass

    def buildWallPolygons(self):
        azimuth = self.azimuthtoccw(self.treeparent.idfclass.getFieldDataByName('Azimuth Angle'))
        if azimuth > 360:
            azimuth = azimuth - 360
#        print azimuth
        azimuth = math.radians(azimuth)
#        print azimuth, 'radians'
        tilt = math.radians(float(self.treeparent.idfclass.getFieldDataByName('Tilt Angle')))
#        print tilt, 'radians'
        sorigin     = numpy.array([float(self.treeparent.idfclass.getFieldDataByName('Starting X Coordinate')), \
                                   float(self.treeparent.idfclass.getFieldDataByName('Starting Y Coordinate')), \
                                   float(self.treeparent.idfclass.getFieldDataByName('Starting Z Coordinate'))])

        length = float(self.treeparent.idfclass.getFieldDataByName('Length'))
        height = float(self.treeparent.idfclass.getFieldDataByName('Height'))
        self.calculateVertices(sorigin,azimuth,tilt,length,height)


    def buildFlatPolygons(self):
        azimuth = math.radians(0)
#        print azimuth, 'radians'
        tilt = math.radians(float(self.treeparent.idfclass.getFieldDataByName('Tilt Angle')))
#        print tilt, 'radians'
        sorigin     = numpy.array([float(self.treeparent.idfclass.getFieldDataByName('Starting X Coordinate')), \
                                   float(self.treeparent.idfclass.getFieldDataByName('Starting Y Coordinate')), \
                                   float(self.treeparent.idfclass.getFieldDataByName('Starting Z Coordinate'))])

        length = float(self.treeparent.idfclass.getFieldDataByName('Length'))
        width = float(self.treeparent.idfclass.getFieldDataByName('Width'))
        self.calculateVertices(sorigin,azimuth,tilt,length,width)


    def calculateVertices(self,scoords,azimuth,tilt,length,height):
        #origin lower left. clockwise
        vertices = numpy.array([[0.0,0.0,0.0],[0.0,0.0,0.0],[0.0,0.0,0.0],[0.0,0.0,0.0]])
        vertices[1][0] = vertices[0][0]
        vertices[1][1] = vertices[0][1] + height
        vertices[1][2] = vertices[0][2]

        vertices[2][0] = vertices[0][0] + length
        vertices[2][1] = vertices[0][1] + height
        vertices[2][2] = vertices[0][2]

        vertices[3][0] = vertices[0][0] + length
        vertices[3][1] = vertices[0][1]
        vertices[3][2] = vertices[0][2]

        #relative vertice
        if self.treeparent.getGeometryRules()["Rectangular Surface Coordinate System"] == "Relative":
            origin = self.getZoneOrigin()
        else:
            origin = [0,0,0]

        self.verticelist = self.math.rotateVerticeList(vertices,tilt,0.0,azimuth)

        self.verticelist[0][0] = origin[0] + scoords[0]
        self.verticelist[0][1] = origin[1] + scoords[1]
        self.verticelist[0][2] = origin[2] + scoords[2]

        self.verticelist[1][0] = self.verticelist[1][0] + origin[0] + scoords[0]
        self.verticelist[1][1] = self.verticelist[1][1] + origin[1] + scoords[1]
        self.verticelist[1][2] = self.verticelist[1][2] + origin[2] + scoords[2]

        self.verticelist[2][0] = self.verticelist[2][0] + origin[0] + scoords[0]
        self.verticelist[2][1] = self.verticelist[2][1] + origin[1] + scoords[1]
        self.verticelist[2][2] = self.verticelist[2][2] + origin[2] + scoords[2]

        self.verticelist[3][0] = self.verticelist[3][0] + origin[0] + scoords[0]
        self.verticelist[3][1] = self.verticelist[3][1] + origin[1] + scoords[1]
        self.verticelist[3][2] = self.verticelist[3][2] + origin[2] + scoords[2]


    def getZoneOrigin(self):
        zone = self.treeparent.getZone(self.treeparent.idfclass.getFieldDataByName('Zone Name'))
        if zone[1] == None:
            return [0.0,0.0,0.0]
        x = float(zone[1].getFieldDataByName('X Origin'))
        y = float(zone[1].getFieldDataByName('Y Origin'))
        z = float(zone[1].getFieldDataByName('Z Origin'))
#        print 'getZoneOrigin',x,y,z
        return [x,y,x]

    def azimuthtoccw(self,azimuth):
        a = 180 - float(azimuth)
        if a < 0:
            return a + 360
        else:
            return a

    def rotate3d(self,x,y,z):
        self.rotatedverticelist = self.math.rotateVerticeList(self.verticelist,x,y,z)
        self.setPolygon(self.rotatedverticelist)

    def getZ(self):
        #returns range of z based on current viewpoint
        zmin = 0
        zmax = 0
        for v in rotatedverticelist:
            if v[2] > zmax:
                zmax = v[2]

            if v[2] < zmin:
                zmin = v[2]

        return zmin,zmax
        


        
    