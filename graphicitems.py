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
        QtGui.QGraphicsPolygonItem.__init__(self,parent,scene)
        self.delegate = None
        print self.type()


    def setDelegate(self,delegate):
        self.delegate = delegate
        self.delegate.setItem(self)

    def setZVisible(self,z):
        return
        #if above z, set invisible, otherwise visible
        print 'setZVisible',z
        if self.delegate != None:
            print 'setZVisible '
            self.setVisible(self.delegate.checkZ(z))
            for c in self.children():
                c.setVisible(c.delegate.checkZ(z))

    def setRotation(self,viewpoint):
        if self.delegate:
            print 'setViewpoint',self,viewpoint
            for c in self.children():
                c.setRotation(viewpoint)
            self.delegate.setRotation(viewpoint)

    def doPolygon(self):
        if self.delegate:
            for c in self.childItems():
                c.doPolygon()
            self.delegate.setPolygon(self.delegate.rotatedverticelist)


class zoneAbstractDelegate(QtCore.QObject):
    def __init__(self,index,parent = None):
        QtCore.QObject.__init__(self,parent)
        self.item = None
        self.math = None
        self.verticelist = []
        self.rotatedverticelist = []
        self.zorder = zlayers.zLayers(None)
        self.lastrotate = []
        if index.isValid():
            self.model = index.model()
            self.math = self.model.math
            self.index = QtCore.QPersistentModelIndex(index)
            self.verticelist = self.createVerticeList()
            self.rotatedverticelist = self.verticelist[:]
            self.idfclass = index.internalPointer().data
        else:
            self.model = None
            self.idfclass = None
            self.index = QtCore.QPersistentModelIndex()

    def setItem(self,item):
        #link to qgraphicsitem
        self.item = item
        self.setPolygon(self.verticelist)


    def createVerticeList(self):
        return self.index.data(idfzonemodel.IdfVerticeRole).toPyObject()


    def checkZ(self,z):
        #returns true if equal or less than z
        res = False
        for v in self.rotatedverticelist:
            if v[2] <= z:
                res = True

        return res
        
    def setRotation(self,viewpoint):
        print 'delegate setViewpoint',viewpoint,self
        self.rotate3d(viewpoint)
        


    def setPolygon(self,polygon):
        #reverse y in array
        print 'Polygon',polygon
        p = QtGui.QPolygonF()
        d = [0,0]
        for e in polygon:
            d[1] = e[1] * -1
            d[0] = e[0]
            p.append(QtCore.QPointF(d[0],d[1]))

        self.item.setPolygon(p)


    def rotate3d(self,xyz):
        print 'rotate3d to be subclassed'


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
        
        
    def setItem(self,item):
        self.item = item
        self.buildZoneOutline()
        self.setPolygon(self.verticelist)
        
        
    def buildZoneOutline(self):
        self.rotatedverticelist = []
        
        
        
        
        for t in ztree[0].childItems:
            self.rotatedverticelist = self.rotatedverticelist + t.item.delegate.getZPoints([top,top])
            for ch in t.childItems:
                self.rotatedverticelist = self.rotatedverticelist + ch.item.delegate.getZPoints([top,top])

        
        
    def rotate3d(self,xyz):
        print 'zonedelegate rotate3d',xyz
        if self.lastrotate == xyz:
            print 'lastrotate',xyz,self.lastrotate
            return
        #rotate children and build z order
        zo = []
        ztree = self.item
        for t in ztree.childItems():
            t.delegate.rotate3d(xyz)
            zo.append(t.delegate.getZ())
            for ch in t.childItems:
                ch.data.rotate3d(xyz)
                zo.append(ch.delegate.getZ())
                
        print 'zonedelegate about to setLayers'
        self.zorder.setLayers(zo)
        # now build polygon
        print 'zonedelegate about to cycle through childitems'
        top = self.zorder.layer()[1]
        self.rotatedverticelist = []
        for t in ztree[0].childItems:
            self.rotatedverticelist = self.rotatedverticelist + t.item.delegate.getZPoints([top,top])
            for ch in t.childItems:
                self.rotatedverticelist = self.rotatedverticelist + ch.item.delegate.getZPoints([top,top])

        print 'zonedelegate about to setPolygon'
#        self.setPolygon(self.rotatedverticelist)
        self.model.zhandler.insertZ(self.zorder.layer())

        
class buildingDelegate(zoneAbstractDelegate):
    
    def rotate3d(self,xzy):
        print 'buildingDelegate rotate3d'
    
    

        
            

class surfacePolygonDelegate(zoneAbstractDelegate):

    def rotate3d(self,xyz):
        print 'surfacePolygonItem rotate3d'
        if self.lastrotate == xyz:
            print 'lastrotate',xyz,self.lastrotate
            return
        self.rotatedverticelist = self.math.rotateVerticeList(self.verticelist,xyz[0],xyz[1],xyz[2])
        self.setPolygon(self.rotatedverticelist)

        


        
    