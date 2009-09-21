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

class surfaceItem():
    def __init__(self,idfclass,surfacemodel):
        self.idfclass = idfclass
        self.surfacemodel = surfacemodel
        self.shape = verticemath.shape(self,self.idfclass)
        self.graphicitem = graphicitems.surfacePolygonItem()
        

    def getGeometryRules(self):
        return self.surfacemodel.getGeometryRules()


    def getZone(self,zname):
        return self.surfacemodel.getZone(zname)

    def setPolygon(self,x,y,z):
        self.graphicitem.setToolTip(self.idfclass.getClassnameIDD() + self.idfclass.getName())
        self.graphicitem.setPolygon(self.shape.getVertices(x,y,z))