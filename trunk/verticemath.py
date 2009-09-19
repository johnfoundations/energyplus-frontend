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

import math
import iddclass
import numpy

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


class shape():
    def __init__(self,surfaceitem,idfclass):
        self.idfclass = idfclass
        self.surfaceitem = surfaceitem
        self.verticelist = []
        if self.idfclass.getClassnameIDD() in verticeclasses:
            self.buildVerticePolygons()

        if self.idfclass.getClassnameIDD() in surfaceelementclasses:
            self.buildSurfaceElementPolygons()

        if self.idfclass.getClassnameIDD() in azimuthtiltclasses:
            self.buildSimplePolygons()

        if self.idfclass.getClassnameIDD() in zoneclasses:
            self.buildZonePolygons()
      
    def buildVerticePolygons(self):
        #translate into lower left, clockwise
        #first get vertices
        vindex = 0
        vertices = []
        v = []
        for c,f in enumerate(self.idfclass.fieldlist):
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
                

#        print self.idfclass.getName(),vertices

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

            #resort vertices
            print 'resort',dindex,vertices
            if dindex > 0:
                vertices = vertices[dindex:len(vertices)] + vertices[0:dindex]
            print vertices
            self.vertices = vertices

        

    def buildSurfaceElementPolygons(self):
        pass

    def buildZonePolygons(self):
        pass

    def buildSimplePolygons(self):
#        print self.idfclass.getName(), self.idfclass.getClassnameIDD()
        vertices = [[0,0,0],[0,0,0],[0,0,0],[0,0,0]]
#        print 'azimuth', self.idfclass.getFieldDataByName('Azimuth Angle')
        azimuth = self.azimuthtoccw(self.idfclass.getFieldDataByName('Azimuth Angle'))
        if azimuth > 360:
            azimuth = azimuth - 360
#        print azimuth
        azimuth = math.radians(azimuth)
#        print azimuth, 'radians'
        tilt = math.radians(float(self.idfclass.getFieldDataByName('Tilt Angle')))
#        print tilt, 'radians'
        sorigin     = [float(self.idfclass.getFieldDataByName('Starting X Coordinate')), \
                       float(self.idfclass.getFieldDataByName('Starting Y Coordinate')), \
                       float(self.idfclass.getFieldDataByName('Starting Z Coordinate'))]

        vertices[0] = sorigin
        length = float(self.idfclass.getFieldDataByName('Length'))
        height = self.idfclass.getFieldDataByName('Width')
        if height == None:
            height = self.idfclass.getFieldDataByName('Height')
        height = float(height)
        #origin lower left. clockwise
        #calculate lower right
        vertices[3][0] = (math.cos(azimuth)*length)
        vertices[3][1] = (math.sin(azimuth)*length)
        vertices[3][2] = 0.0
        #tilt. 0 faces up, 180 faces down
        vertices[1][0] = (-vertices[3][1] * height / length) * math.cos(tilt)
        vertices[1][1] = (vertices[3][0] * height / length) * math.cos(tilt)
        vertices[1][2] = math.sin(tilt) * height
        #3rd
        vertices[2][0] = vertices[3][0]
        vertices[2][1] = vertices[3][1]
        vertices[2][2] = vertices[1][2]


        #relative vertice
        if self.surfaceitem.getGeometryRules()["Rectangular Surface Coordinate System"] == "Relative":
            origin = self.getZoneOrigin()
        else: origin = [0,0,0]

        print self.idfclass.getClassnameIDD(),self.idfclass.getName()
        print origin
        print '%f,%f,%f' % (origin[0],origin[1],origin[2])
        print '%f,%f,%f' % (vertices[0][0],vertices[0][1],vertices[0][2])
        print '%f,%f,%f' % (vertices[1][0],vertices[1][1],vertices[1][2])
        print '%f,%f,%f' % (vertices[2][0],vertices[2][1],vertices[2][2])
        print '%f,%f,%f' % (vertices[3][0],vertices[3][1],vertices[3][2])


        vertices[0][0] = origin[0] + sorigin[0]
        vertices[0][1] = origin[1] + sorigin[1]
        vertices[0][2] = origin[2] + sorigin[2]
        
        vertices[1][0] = vertices[1][0] + origin[0] + sorigin[0]
        vertices[1][1] = vertices[1][1] + origin[1] + sorigin[1]
        vertices[1][2] = vertices[1][2] + origin[2] + sorigin[2]
        
        vertices[2][0] = vertices[2][0] + origin[0] + sorigin[0]
        vertices[2][1] = vertices[2][1] + origin[1] + sorigin[1]
        vertices[2][2] = vertices[2][2] + origin[2] + sorigin[2]
        
        vertices[3][0] = vertices[3][0] + origin[0] + sorigin[0]
        vertices[3][1] = vertices[3][1] + origin[1] + sorigin[1]
        vertices[3][2] = vertices[3][2] + origin[2] + sorigin[2]

        print '%f,%f,%f' % (vertices[0][0],vertices[0][1],vertices[0][2])
        print '%f,%f,%f' % (vertices[1][0],vertices[1][1],vertices[1][2])
        print '%f,%f,%f' % (vertices[2][0],vertices[2][1],vertices[2][2])
        print '%f,%f,%f' % (vertices[3][0],vertices[3][1],vertices[3][2])

        self.verticelist = vertices

        


    def getZoneOrigin(self):
        zone = self.surfaceitem.getZone(self.idfclass.getFieldDataByName('Zone Name'))
        x = float(zone.getFieldDataByName('X Origin'))
        y = float(zone.getFieldDataByName('Y Origin'))
        z = float(zone.getFieldDataByName('Z Origin'))
        return [x,y,x]



    def azimuthtoccw(self,azimuth):
        a = 180 - float(azimuth)
        if a < 0:
            return a + 360
        else:
            return a


    def transform(self,v1,v2):
        res = [0,0,0]
        res[0] = v2[0] - v1[0]
        res[1] = v2[1] - v1[1]
        res[2] = v2[2] - v1[2]
        return res

    def add(self,v1,v2)  :
        res = [0,0,0]
        res[0] = v2[0] + v1[0]
        res[1] = v2[1] + v1[1]
        res[2] = v2[2] + v1[2]
        return res

    def mult(self,v1,m):
        res = [0,0,0]
        res[0] = v1[0] *m
        res[1] = v1[1] *m
        res[2] = v1[2] *m
        return res


    def getVertices(self,viewpoint):
        return self.vertices
    

if __name__ == "__main__":
    wall = iddclass.Wall_Exterior()
    walldata = ["Wall:Exterior","test","Construction","Zone",90,90,0,0,0,10,20]
    wall.setData(walldata)
    print wall
    s = shape(wall,None)
    
    