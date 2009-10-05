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

import graphicitems
import verticemath
import idfdata
import math
import numpy


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


#data in treeItem points to a surfaceItem
class surfaceItem():
    def __init__(self,idfclass,surfacemodel):
        self.idfclass = idfclass
        self.model = surfacemodel
        self.math = self.model.math
        self.verticelist = []
        if self.idfclass.getClassnameIDD() in verticeclasses:
            self.buildVerticePolygons()

        if self.idfclass.getClassnameIDD() in surfaceelementclasses:
            self.buildSurfaceElementPolygons()

        if self.idfclass.getClassnameIDD() in azimuthwallclasses:
            self.buildWallPolygons()

        if self.idfclass.getClassnameIDD() in azimuthflatclasses:
            self.buildFlatPolygons()


    def getGeometryRules(self):
        return self.surfacemodel.getGeometryRules()


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

        if self.surfaceitem.getGeometryRules()["Vertex Entry Direction"] == "Counterclockwise":
            vertices.reverse()
            first = vertices.pop()
            vertices.insert(0,first)

        rules = self.surfaceitem.getGeometryRules()["Starting Vertex Position"]
        if rules == "UpperLeftCorner" or "UpperRightCorner" or "LowerRightCorner":
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

            if dindex > 0:
                vertices = vertices[dindex:len(vertices)] + vertices[0:dindex]

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

    def buildWallPolygons(self):
        azimuth = self.azimuthtoccw(self.idfclass.getFieldDataByName('Azimuth Angle'))
        if azimuth > 360:
            azimuth = azimuth - 360
        azimuth = math.radians(azimuth)
        tilt = math.radians(float(self.idfclass.getFieldDataByName('Tilt Angle')))
        sorigin     = numpy.array([float(self.idfclass.getFieldDataByName('Starting X Coordinate')), \
                                   float(self.idfclass.getFieldDataByName('Starting Y Coordinate')), \
                                   float(self.idfclass.getFieldDataByName('Starting Z Coordinate'))])

        length = float(self.idfclass.getFieldDataByName('Length'))
        height = float(self.idfclass.getFieldDataByName('Height'))
        self.calculateVertices(sorigin,azimuth,tilt,length,height)


    def buildFlatPolygons(self):
        azimuth = math.radians(0)
        tilt = math.radians(float(self.idfclass.getFieldDataByName('Tilt Angle')))
        sorigin     = numpy.array([float(self.idfclass.getFieldDataByName('Starting X Coordinate')), \
                                   float(self.idfclass.getFieldDataByName('Starting Y Coordinate')), \
                                   float(self.idfclass.getFieldDataByName('Starting Z Coordinate'))])

        length = float(self.idfclass.getFieldDataByName('Length'))
        width = float(self.idfclass.getFieldDataByName('Width'))
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
        if self.model.getGeometryRules()["Rectangular Surface Coordinate System"] == "Relative":
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
        zone = self.model.getZone(self.idfclass.getFieldDataByName('Zone Name'))
        if zone[1] == None:
            return [0.0,0.0,0.0]
        x = float(zone[1].getFieldDataByName('X Origin'))
        y = float(zone[1].getFieldDataByName('Y Origin'))
        z = float(zone[1].getFieldDataByName('Z Origin'))
        return [x,y,x]

    def azimuthtoccw(self,azimuth):
        a = 180 - float(azimuth)
        if a < 0:
            return a + 360
        else:
            return a






        