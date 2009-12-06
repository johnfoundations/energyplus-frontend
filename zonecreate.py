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
    def __init__(self):
        self.vertices = []
        self.vmath = verticemath.verticeMath()
    
    
    def isAdjacent(self,orig,new):
        #checks if zones are adjacent, returns series of points that are adjacent
        pdb.set_trace()
        reslist = []
        for c,i in enumerate(orig):
            if c == len(orig) - 1:
                continue
            
            uvect = self.vmath.transform(i,orig[c+1])
            for ni in new:
                iuvect = self.vmath.transform(i,ni)
                if numpy.cross(numpy.array(uvect),numpy.array(iuvect)).tolist() == [0,0,0]:
                    #lines are parallel. Now find if they are adjacent
                    reslist.append(ni)
        return reslist
        
        
if __name__ == "__main__":
    z = zoneCreate()
    a = [[0,0,0],[0,8,0],[10,8,0],[10,0,0]]
    b = [[0,8,0],[0,28,0],[14,28,0],[14,8,0]]
    l = z.isAdjacent(a,b)
    print l
