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
import idfzonemodel









class zoneItem(QtGui.QGraphicsPolygonItem):
    def __init__(self,parent=None,scene=None):
        QtGui.QGraphicsPolygonItem.__init__(parent,scene)
        self.delegate = None


    def setDelegate(self,delegate):
        self.delegate = delegate
        self.delegate.setItem(self)

    def setZVisible(self,z):
        #if above z, set invisible, otherwise visible
        print 'setZVisible',z
        if self.delegate != None:
            print 'setZVisible '
            self.setVisible(self.delegate.checkZ(z))
            for c in self.children():
                c.setVisible(c.delegate.checkZ(z))

    def setViewpoint(self,viewpoint):
        if self.delegate:
            print 'setViewpoint',viewpoint
            for c in self.children():
                c.delegate.setViewpoint(viewpoint)
            self.delegate.setViewpoint(viewpoint)



class zoneAbstractDelegate(QtCore.QObject):
    def __init__(self,index,parent = None):
        QtCore.QObject.__init__(self,parent)
        self.item = None
        self.math = None
        self.verticelist = []
        self.rotatedverticelist = []
        self.zorder = zlayers.zLayers(None)
        if index.isValid():
            self.model = index.model()
            self.math = self.model.math
            self.index = QtCore.QPersistentModelIndex(index)
            self.verticelist = self.createVerticeList()
            self.idfclass = index.internalPointer().data
        else:
            self.model = None
            self.idfclass = None
            self.index = QtCore.QPersistentModelIndex()

    def setItem(self,item):
        #link to qgraphicsitem
        self.item = item


    def createVerticeList(self):
        return self.index.data(idfzonemodel.IdfVerticeRole)


    def checkZ(self,z):
        #returns true if equal or less than z
        res = False
        for v in self.rotatedverticelist:
            if v[2] <= z:
                res = True

        return res
        
    def setViewpoint(self,viewpoint):
        print 'delegate setViewpoint',viewpoint
        self.rotate3d(viewpoint)
        self.setPolygon(self.rotatedverticelist)
        


    def setPolygon(self,polygon):
        #reverse y in array
        p = QtGui.QPolygonF()
        for e in polygon:
            e[1] = e[1] * -1
            p.append(QtCore.QPointF(e[0],e[1]))

        self.item.setPolygon(p)


    def rotate3d(self,xyz):
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



class zoneDelegate(zoneAbstractDelegate):
        
        
    def rotate3d(self,xyz):
        print 'zonedelegate rotate3d',xyz
        #rotate children and build z order
        zo = []
        ztree = self.item
        for t in ztree.childItems():
            t.delegate.rotate3d(xyz)
            zo.append(t.delegate.getZ())
            for ch in t.childItems:
                ch.data.rotate3d(xyz)
                zo.append(ch.delegate.getZ())
        self.zorder.setLayers(zo)
        # now build polygon
        top = self.zorder.layer()[1]
        self.rotatedverticelist = []
        for t in ztree[0].childItems:
            self.rotatedverticelist = self.rotatedverticelist + t.item.delegate.getZPoints([top,top])
            for ch in t.childItems:
                self.rotatedverticelist = self.rotatedverticelist + ch.item.delegate.getZPoints([top,top])

        self.setPolygon(self.rotatedverticelist)
        self.model.zhandler.insertZ(self.zorder.layer())

        
            

        
            

class surfacePolygonItem(zoneAbstractDelegate):

    def rotate3d(self,x,y,z):
        self.rotatedverticelist = self.math.rotateVerticeList(self.verticelist,x,y,z)
        self.setPolygon(self.rotatedverticelist)

        


        
    