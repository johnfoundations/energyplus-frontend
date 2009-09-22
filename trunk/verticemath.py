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

azimuthwallclasses = "Wall:Exterior","Wall:Adiabatic","Wall:Underground","Wall:Interzone","Shading:Site",\
                     "Shading:Building"
        #azimuth,tilt,xyz,length,width

azimuthflatclasses = "Ceiling:Adiabatic","Ceiling:Interzone","Floor:GroundContact","Floor:Adiabatic","Floor:Interzone",\
                     "Roof"


class shape():
    def __init__(self,surfaceitem,idfclass):
        self.idfclass = idfclass
        self.surfaceitem = surfaceitem
        self.verticelist = []
        if self.idfclass.getClassnameIDD() in verticeclasses:
            self.buildVerticePolygons()

        if self.idfclass.getClassnameIDD() in surfaceelementclasses:
            self.buildSurfaceElementPolygons()

        if self.idfclass.getClassnameIDD() in azimuthwallclasses:
            self.buildWallPolygons()

        if self.idfclass.getClassnameIDD() in azimuthflatclasses:
            self.buildFlatPolygons()

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
                

        print self.idfclass.getName()
        print vertices

        if self.surfaceitem.getGeometryRules()["Vertex Entry Direction"] == "Counterclockwise":
            vertices.reverse()
            first = vertices.pop()
            vertices.insert(0,first)

        print 'direction corrected',
        self.printVerticeList(vertices)
        
        rules = self.surfaceitem.getGeometryRules()["Starting Vertex Position"]
        if rules == "UpperLeftCorner" or "UpperRightCorner" or "LowerRightCorner":
            print rules
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
            self. printVerticeList(vertices)

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
        azimuth = self.azimuthtoccw(self.idfclass.getFieldDataByName('Azimuth Angle'))
        if azimuth > 360:
            azimuth = azimuth - 360
#        print azimuth
        azimuth = math.radians(azimuth)
        print azimuth, 'radians'
        tilt = math.radians(float(self.idfclass.getFieldDataByName('Tilt Angle')))
#        print tilt, 'radians'
        sorigin     = numpy.array([float(self.idfclass.getFieldDataByName('Starting X Coordinate')), \
                                   float(self.idfclass.getFieldDataByName('Starting Y Coordinate')), \
                                   float(self.idfclass.getFieldDataByName('Starting Z Coordinate'))])

        length = float(self.idfclass.getFieldDataByName('Length'))
        height = float(self.idfclass.getFieldDataByName('Height'))
        self.calculateVertices(sorigin,azimuth,tilt,length,height)


    def buildFlatPolygons(self):
        azimuth = math.radians(0)
#        print azimuth, 'radians'
        tilt = math.radians(float(self.idfclass.getFieldDataByName('Tilt Angle')))
#        print tilt, 'radians'
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

#        print 'vertices 1'
#        self.printVerticeList(vertices)
#        print
        #relative vertice
        if self.surfaceitem.getGeometryRules()["Rectangular Surface Coordinate System"] == "Relative":
            origin = self.getZoneOrigin()
        else:
            origin = [0,0,0]
            
        print self.idfclass.getClassnameIDD(),self.idfclass.getName()
        self.verticelist = self.rotateVerticeList(vertices,tilt,0.0,azimuth)

        print self.verticelist
#        print 'rotated matrix'
#        self.printVerticeList(vertices)
#        print vertices

#        for v in vertices:
#            self.verticelist.append(self.matrixAsVertice(v))

#        self.printVerticeList(self.verticelist)


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
        
#        print self.idfclass.getClassnameIDD(),self.idfclass.getName()
#        print 'length',length, 'height',height,'tilt', tilt,'azimuth', azimuth
#        self.printVertice(origin)
#        self.printVertice(scoords)
#        print
#        self.printVerticeList(self.verticelist)
#        print
#        print

    def getZoneOrigin(self):
        zone = self.surfaceitem.getZone(self.idfclass.getFieldDataByName('Zone Name'))
        if zone[1] == None:
            return [0.0,0.0,0.0]
        x = float(zone[1].getFieldDataByName('X Origin'))
        y = float(zone[1].getFieldDataByName('Y Origin'))
        z = float(zone[1].getFieldDataByName('Z Origin'))
        print 'getZoneOrigin',x,y,z
        return [x,y,x]

    def printVerticeList(self,v):
        for vv in v:
            print '%f,%f,%f' % (vv[0],vv[1],vv[2])

    def printVertice(self,vv):
            print '%f,%f,%f' % (vv[0],vv[1],vv[2])
            
    def printMatrix(self,m):
        pass
#        for mm in m:
#            print '%f,%f,%f,%f' % (mm[0],mm[1],mm[2],mm[3])


    def azimuthtoccw(self,azimuth):
        a = 180 - float(azimuth)
        if a < 0:
            return a + 360
        else:
            return a

    def identityMatrix(self):
        m = numpy.asmatrix(numpy.array([[1,0,0,0],[0,1,0,0],[0,0,1,0],[0,0,0,1]]))
        return m

    def rotationMatrix(self,x,y,z):
        m = numpy.array([[math.cos(z)*math.cos(y)+math.sin(z)*math.sin(x)*math.sin(y), \
                          math.sin(z)*math.cos(y)-math.sin(x)*math.sin(y),            \
                          math.cos(x)*math.sin(z),                                    \
                          0],                                                          \
                         [-math.sin(z)*math.cos(x),                                    \
                          math.sin(z)*math.cos(x),                                     \
                          math.sin(x),                                                 \
                          0],                                                          \
                         [math.sin(z)*math.sin(x)*math.cos(y)-math.cos(z)*math.sin(y), \
                          -math.cos(z)*math.sin(x)*math.cos(y)-math.sin(z)*math.sin(y),\
                          math.cos(x)*math.cos(y),                                     \
                          0],                                                          \
                         [0,0,0,1]])
        return m

    def xmatrix(self,x):
        m = numpy.matrix([[1.0,0.0,0.0,0.0], \
                         [0.0,math.cos(x),math.sin(x),0.0], \
                         [0.0,-math.sin(x),math.cos(x),0.0],  \
                         [0.0,0.0,0.0,1.0]])

        return m

    def ymatrix(self,):
        m = numpy.matrix([[math.cos(y),0.0,-math.sin(y),0.0], \
                         [0.0,1.0,0.0,0.0], \
                         [math.sin(y),0.0,math.cos(y),0.0],  \
                         [0.0,0.0,0.0,1.0]])

        return m

    def zmatrix(self,z):
        m = numpy.matrix([[math.cos(z),math.sin(z),0.0,0.0], \
                         [-math.sin(z),math.cos(z),0.0,0.0], \
                         [0.0,0.0,1.0,0.0],  \
                         [0.0,0.0,0.0,1.0]])

        return m

    def identity(self):
        return numpy.matrix([[1.0,0.0,0.0,0.0],[0.0,1.0,0.0,0.0],[0.0,0.0,1.0,0.0],[0.0,0.0,0.0,1.0]])


            
    def rotateVerticeList(self,vlist,x,y,z):
        print 'rotateVerticeList ',x,y,z
        self.printVerticeList(vlist)
        if x != 0:
            xm = self.xmatrix(x)

        if y != 0:
            ym = self.ymatrix(y)

        if z != 0:
            zm = self.zmatrix(z)

        rlist = []
        for v in vlist:
            vm = self.verticeAsMatrix(v)
            print 'as matrix',vm
            if x != 0:
                vm = numpy.dot(vm,xm)
                print '*xm',xm
                self.printMatrix(vm)
            if y != 0:
                vm = numpy.dot(vm,ym)
                print '*ym',ym
                self.printMatrix(vm)
            if z != 0:
                vm = numpy.dot(vm,zm)
                print '*zm',zm
                self.printMatrix(vm)

            print vm
            a = vm.tolist()
            rlist.append(a[0])

        return rlist


        
        
    def verticeAsMatrix(self,xyz):
        m = numpy.matrix([xyz[0],xyz[1],xyz[2],1.0])
#        m = numpy.asmatrix(m)
        return m

    def matrixAsVertice(self,m):
        return  [m[0][0],m[1][1],m[2][2]]
        

    def getVertices(self,xrot,yrot,zrot):
        xylist = []
        for xyz in self.verticelist:
            xy = [xyz[0],xyz[1]]
            if xy not in xylist:
                xylist.append(xy)
#        print 'getVertices',self.idfclass.getName(),self.idfclass.getClassnameIDD()
#        self.printVerticeList(self.verticelist)
#        print xylist
        return xylist
    

if __name__ == "__main__":
    wall = iddclass.Wall_Exterior()
    walldata = ["Wall:Exterior","test","Construction","Zone",90,90,0,0,0,20,10]
    wall.setData(walldata)
    print wall
    s = shape(None,wall)
    
    