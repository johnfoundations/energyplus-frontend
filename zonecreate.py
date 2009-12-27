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

from PyQt4 import QtCore
import graphicitems
import verticemath
import idfdata
import math
import numpy
from classinfo import *
import pdb

class zoneCreate():
    def __init__(self,model,vertices,height,name):
        self.vertices = vertices
        self.height = height
        self.name = name
        self.vmath = verticemath.verticeMath()
        
    
    def nameCreate(self,zonename,verticelist):
        pass
        
    
    def isAdjacent(self,orig,new):
        #checks if zones are adjacent, returns series of points that are adjacent
#        pdb.set_trace()
#        print 'orig',orig
#        print 'new',new
        reslist = []
        for c,i in enumerate(orig):
            if c == len(orig) - 1:
                p2 = orig[0]
            else:
                p2 = orig[c+1]
            
            uvect = self.vmath.transform(i,p2)
            lres = []
            for ni in new:
                iuvect = self.vmath.transform(i,ni)
                if numpy.cross(numpy.array(uvect),numpy.array(iuvect)).tolist() == [0,0,0]:
                    #lines are parallel.
                    lres.append(ni)
           
            if len(lres) > 0:
                #should have two points
                olen = self.vmath.dist(self.vmath.transform(i,p2))
                nlen = self.vmath.dist(self.vmath.transform(lres[0],lres[1]))
                vect = []
                longest = 0
                for lr in lres:
                    d1 = self.vmath.dist(self.vmath.transform(i,lr))
                    if d1 > longest:
                        longest = d1
                    d2 = self.vmath.dist(self.vmath.transform(p2,lr))
                    if d2 > longest:
                        longest = d2
#                print olen,nlen,longest
                if (olen + nlen) > longest:
                    #we have adjacent sides
                    oline = [i,p2]
                    #align both vectors the same direction
                    turned = False
                    if numpy.dot(numpy.array(self.vmath.transform(oline[0],oline[1])),numpy.array(self.vmath.transform(lres[0],lres[1]))) < 0:
                        nline = [lres[1],lres[0]]
                        turned = True
                    else:
                        nline = [lres[0],lres[1]]
                    #print oline,nline
                    #find intersection at one end
                    #will return two arrays. [0] is series of points in original line marking segments where the two are adjacent
                    #[1] is new line.
                    olinearray = []
                    nlinearray = [] 
                    ostate = [] #0 for interior, 1 for exterior. an entry for each line
                    nstate = []
                    olinearray.append(oline[0])
                    if self.vmath.dist(self.vmath.transform(oline[0],nline[0])) == 0:
                        nlinearray.append(nline[0])
                        ostate.append(0)
                        nstate.append(0)
                    
                    else:
                        if numpy.dot(numpy.array(self.vmath.transform(oline[0],nline[0])),numpy.array(self.vmath.transform(oline[0],oline[1]))) < 0:
                            #opposite directions
                            nlinearray.append(oline[0])
                            nlinearray.append(nline[0])
                            nstate.append(1)
                            nstate.append(0)
                            ostate.append(0)
                        else:
                            olinearray.append(nline[0])
                            nlinearray.append(nline[0])
                            ostate.append(1)
                            ostate.append(0)
                            nstate.append(0)
                    
                    if self.vmath.dist(self.vmath.transform(oline[1],nline[1])) == 0:
                        olinearray.append(oline[1])
                        nlinearray.append(nline[1])
                        
                    else:
                        if numpy.dot(numpy.array(self.vmath.transform(oline[1],nline[1])),numpy.array(self.vmath.transform(oline[0],oline[1]))) < 0:
                            #opposite direction
                            olinearray.append(nline[1])
                            olinearray.append(oline[1])
                            nlinearray.append(nline[1])
                            ostate.append(1)
                            
                        else:
                            nlinearray.append(oline[1])
                            nlinearray.append(nline[1])
                            olinearray.append(oline[1])
                            nstate.append(1)
                    
                    #print olinearray,nlinearray
                    if turned:
                        nlinearray.reverse()
                        nstate.reverse()
                    reslist.append([olinearray,nlinearray,ostate,nstate])


        return reslist
        
        
if __name__ == "__main__":
    z = zoneCreate()
    a = [[0,0,0],[0,8,0],[10,8,0],[10,0,0]]
    b = [[0,8,0],[0,28,0],[14,28,0],[14,8,0]]
    c = [[14,12,0],[14,28,0],[24,28,0],[24,12,0]]
    d = [[24,0,0],[24,14,0],[28,14,0],[28,0,0]]
    e = [[10,0,0],[10,8,0],[14,8,0],[14,12,0],[16,12,0],[16,0,0]]
    print 'a,b',z.isAdjacent(a,b)
    print 'a,c',z.isAdjacent(a,c)
    print 'b,c',z.isAdjacent(b,c)
    print 'c,d',z.isAdjacent(c,d)
    print 'b,e',z.isAdjacent(b,e)
    print 'a,e',z.isAdjacent(a,e)
    print 'c,e',z.isAdjacent(c,e)
