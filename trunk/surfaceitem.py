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

import graphicsitem
import verticemath
import idfdata

class surfaceItem():
    def __init__(self,treeitem,idfclass,surfacemodel):
        self.treeitem = treeitem
        self.idfclass = idfclass
        self.surfacemodel = surfacemodel
        self.shape = verticemath.shape(self.idfclass)
        self.graphicsitem = graphicsitem.surfacePolygonItem()
        self.geometryrules = dict()

    def getGeometryRules(self):
        if len(self.geometryrules) == 0:
            if treeitem.parentItem != None:
                self.geometryrules = treeitem.parentItem.data.getGeometryRules()
            else:
                self.geometryrules = self.surfacemodel.getGeometryRules()
        return self.geometryrules
            