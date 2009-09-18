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
    def __init__(self,idfclass):
        self.idfclass = idfclass
        self.ggrules = globalgeometryrules
        if self.idfclass.getClassnameIDD() in verticeclasses:
            self.buildVerticePolygons()

        if self.idfclass.getClassnameIDD() in surfaceelementclasses:
            self.buildSurfaceElementPolygons()

        if self.idfclass.getClassnameIDD() in azimuthtiltclasses:
            self.buildSimplePolygons()

        if self.idfclass.getClassnameIDD() in zoneclasses:
            self.buildZonePolygons()
      
    def buildVerticePolygons(self):
        pass

    def buildSurfaceElementPolygons(self):
        pass

    def buildZonePolygons(self):
        pass

    def buildSimplePolygons(self):
        vertices = [[0,0,0],[0,0,0],[0,0,0],[0,0,0]]
        print 'azimuth', self.idfclass.fieldlist[3].getValue()
        azimuth = self.azimuthtoccw(self.idfclass.fieldlist[3].getValue())
        if azimuth > 360:
            azimuth = azimuth - 360
        print azimuth
        azimuth = math.radians(azimuth)
        print azimuth, 'radians'
        tilt = math.radians(self.idfclass.fieldlist[4].getValue())
        print tilt, 'radians'
        vertices[0] = [self.idfclass.fieldlist[5].getValue(),self.idfclass.fieldlist[6].getValue(),self.idfclass.fieldlist[7].getValue()]
        length = self.idfclass.fieldlist[8].getValue()
        height = self.idfclass.fieldlist[9].getValue()
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

        print '%f,%f,%f' % (vertices[0][0],vertices[0][1],vertices[0][2])
        print '%f,%f,%f' % (vertices[1][0],vertices[1][1],vertices[1][2])
        print '%f,%f,%f' % (vertices[2][0],vertices[2][1],vertices[2][2])
        print '%f,%f,%f' % (vertices[3][0],vertices[3][1],vertices[3][2])

        
        
    def buildSimpleHorizontalPolygons(self):
        pass


    def azimuthtoccw(self,azimuth):
        a = 180 - azimuth
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


if __name__ == "__main__":
    wall = iddclass.Wall_Exterior()
    walldata = ["Wall:Exterior","test","Construction","Zone",90,90,0,0,0,10,20]
    wall.setData(walldata)
    print wall
    s = shape(wall,None)
    
    