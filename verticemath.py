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
import numpy



class verticeMath():
    def __init__(self):
        matrixcache = dict()


    def printVerticeList(self,v):
        for vv in v:
            print '%f,%f,%f' % (vv[0],vv[1],vv[2])

    def printVertice(self,vv):
            print '%f,%f,%f' % (vv[0],vv[1],vv[2])
            
    def printMatrix(self,m):
        pass
#        for mm in m:
#            print '%f,%f,%f,%f' % (mm[0],mm[1],mm[2],mm[3])




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

    def eq(self,v1,v2):
        #checks whether the vertices are close enough to be equal
        if len(v1) != len(v2):
            return False

        res = True
        for c,d in enumerate(v1):
            if abs(v1[c] - v2[c]) > 0.0001:
                res = False
        return res

    def fin(self,v,l):
        #checks whether v is eq() any items in l
        res = False
        for i in l:
            if self.eq(v,i):
                res = True

        return res
        
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
    
    