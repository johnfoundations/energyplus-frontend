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
        self.setFlag(QtGui.QGraphicsItem.ItemIsFocusable)
        print self.type()

    def focusInEvent (self, event):
        print 'zoneItem focusInEvent'
        if self.delegate:
            self.delegate.focusIn()
    
    def focusOutEvent (self,event):
        print 'zoneItem focusOutEvent'
        if self.delegate:
            self.delegate.focusOut()
        

    def showItems(self,show):
#        QtCore.pyqtRemoveInputHook() 
#        import pdb 
#        pdb.set_trace() 

#        print 'showItems',show,self,self.delegate
        self.setVisible(show)
        for c in self.children():
#            print c,c.zValue(),c.delegate
            c.showItems(show)


    def setDelegate(self,delegate):
        self.delegate = delegate
        self.delegate.setItem(self)

    def setZVisible(self,inc):
        if self.delegate != None:
            self.delegate.setZ(inc)


    def setRotation(self,viewpoint):
#        print 'zoneItem setRotation'
        if self.delegate:
#            print 'setViewpoint',self,viewpoint
            for c in self.children():
                c.setRotation(viewpoint)
            self.delegate.setRotation(viewpoint)

    def doPolygon(self):
#        print 'zoneItem doPolygon'
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
        self.zorder = zlayers.zLayers()
        self.lastrotate = []
        if index.isValid():
            self.model = index.model()
            self.math = self.model.math
            self.index = QtCore.QPersistentModelIndex(index)
            self.verticelist = self.createVerticeList()
            self.rotatedverticelist = self.verticelist[:]
            self.idfclass = index.internalPointer().data.idfclass
        else:
            self.model = None
            self.idfclass = None
            self.index = QtCore.QPersistentModelIndex()

    def focusIn(self):
        pass
    
    def focusOut(self):
        pass


    def setStyle(self):
        pen = self.item.pen()
        pen.setColor(QtCore.Qt.black)
        pen.setWidthF(0.1)
        pen.setJoinStyle(QtCore.Qt.MiterJoin)
        self.item.setPen(pen)

    def setZ(self,inc):
#        print 'setZ',inc,self
        if inc:
            value = self.zorder.inc()
        else:
            value = self.zorder.dec()
            
        for i in self.item.childItems():
#            print i.delegate,i.delegate.getZAvg()
            i.setVisible(i.delegate.getZAvg() > value)

        
    def getZAvg(self):
        za = 0.0
        for v in self.rotatedverticelist:
            za = za + v[2]
            
        return za/len(self.rotatedverticelist)

    def setItem(self,item):
        #link to qgraphicsitem
#        print 'zoneAbstractDelegate setItem'
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
#        print 'delegate setViewpoint',viewpoint,self
        self.rotate3d(viewpoint)
        


    def setPolygon(self,polygon):
        #reverse y in array

        self.setStyle()
        p = QtGui.QPolygonF()
        d = [0,0]
        za = 0
        for e in polygon:
            d[1] = e[1] * -1
            d[0] = e[0]
#            print 'setPolygon',d,self.idfclass.getName()
            p.append(QtCore.QPointF(d[0],d[1]))
            za = za + e[2]

        self.item.setPolygon(p)
        if len(polygon) > 0:
            a = za / len(polygon)
            self.item.setZValue(a)



    def rotate3d(self,xyz):
        print 'rotate3d to be subclassed'


    def getZPoints(self,zrange):
        #zrange is a array
        #if array is empty, all points returned
        #otherwise points within and equal to either values
        if len(zrange) == 0:
            return self.rotatedverticelist
        zpts = []
        for v in self.rotatedverticelist:
            if zrange[0] >= v[2] or zrange[1] <= v[2]:
                zpts.append(v)

        return zpts



class zoneDelegate(zoneAbstractDelegate):
        


    def setStyle(self):
        pen = self.item.pen()
        pen.setColor(QtCore.Qt.black)
        pen.setWidthF(0.1)
        pen.setJoinStyle(QtCore.Qt.MiterJoin)
        self.item.setPen(pen)
        
    def setItem(self,item):
        print 'zoneDelegate setItem'
        self.item = item
        self.buildZoneOutline()
        self.setPolygon(self.verticelist)
        
        
    def buildZoneOutline(self):
        print self.idfclass.getName()
        self.verticelist = self.getOutline(self.item)
        #find lowest z
        lz = 3000
        for v in self.verticelist:
            if v[2] < lz:
                lz = v[2]
                
        #now set all z values to lz
        for v in self.verticelist:
            v[2] = lz

    def getOutline(self,item):
        vlist = []
        nonfit = []
        for t in item.childItems():
            
            clist = t.delegate.getZPoints([])
            za = 0.0
            for c in clist:
                za = za + c[2]
                
            self.zorder.insertZ(za/len(clist))
                
            
            clean = self.removeDups(clist)
            
            if len(clean) > 2:
                #is it floor or ceiling, slanted wall, what?
                continue
                
                    
            if len(vlist) == 0:
                vlist.append(clean[0])
                vlist.append(clean[1])
                continue
            
#            print 'getOutline',vlist,clean
            if self.compareXY(vlist[len(vlist)-1],clean[0]):
                vlist.append(clean[1])
                continue
            
            if self.compareXY(vlist[len(vlist)-1], clean[1]):
                vlist.append(clean[0])
                continue
            
            nonfit.append(clean)
            
        while len(nonfit) > 0:
            for i in nonfit:
                if self.compareXY(vlist[len(vlist)-1],i[0]):
                    vlist.append(i[1])
                    nonfit.remove(i)
                    break
            
                if self.compareXY(vlist[len(vlist)-1],i[1]):
                    vlist.append(i[0])
                    nonfit.remove(i)
                    break
                    
        return vlist
        
    def removeDups(self,vlist):
        llist = [vlist[0]]
        exists = False
        for v in vlist:
            #print 'removeDups',v
            for l in llist:
#                print l
                if (abs(l[0] - v[0]) < 0.001) and (abs(l[1]-v[1]) < 0.001):
                    exists = True

            #print 'exists',exists
            if exists == False:
                llist.append(v)
                
            exists = False
            
        return llist
                    
        
    def compareXY(self,v1, v2):
        
        if (abs(v1[0]-v2[0]) < 0.001) and (abs(v1[1]-v2[1]) < 0.001):
            return True
        else:
            return False
        
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

    def focusIn(self):
#        if self.item.scene().itemwithfocus != None:
#            self.item.scene().itemwithfocus.focusOut()
           
        self.item.scene().itemwithfocus = self
        self.item.showItems(True)

    def focusOut(self):
         self.item.showItems(False)
         self.item.setVisible(True)



        
class buildingDelegate(zoneAbstractDelegate):
    
    def rotate3d(self,xzy):
        print 'buildingDelegate rotate3d'
    
    def buildZ(self):
        for i in self.item.childItems():
            za = 0.0
            for v in i.delegate.rotatedverticelist:
                za = za + v[2]
            
            if len(i.delegate.rotatedverticelist) > 0:
                self.zorder.insertZ(za/len(i.delegate.rotatedverticelist))

        
            

class surfacePolygonDelegate(zoneAbstractDelegate):

    
    def setStyle(self):
        pen = self.item.pen()
        pen.setColor(QtCore.Qt.gray)
        pen.setWidthF(0.2)
        pen.setJoinStyle(QtCore.Qt.MiterJoin)
        self.item.setPen(pen)


    def rotate3d(self,xyz):
        print 'surfacePolygonItem rotate3d'
        if self.lastrotate == xyz:
            print 'lastrotate',xyz,self.lastrotate
            return
        self.rotatedverticelist = self.math.rotateVerticeList(self.verticelist,xyz[0],xyz[1],xyz[2])
        self.setPolygon(self.rotatedverticelist)

    def setItem(self,item):
        #link to qgraphicsitem
        print 'surfacePolygonDelegate setItem'
        self.item = item
        self.setPolygon(self.verticelist)
        self.item.setVisible(False)
 
class wallDelegate(surfacePolygonDelegate):
    
    def setStyle(self):
        pen = self.item.pen()
        pen.setColor(QtCore.Qt.darkBlue)
        pen.setWidthF(0.3)
   #     pen.setJoinStyle(QtCore.Qt.MiterJoin)
   #     pen.setMiterLimit(1)
        self.item.setPen(pen)
    

    
class windowDelegate(surfacePolygonDelegate):
    
    def setStyle(self):
        pen = self.item.pen()
        pen.setColor(QtCore.Qt.yellow)
        pen.setWidthF(0.3)
        pen.setJoinStyle(QtCore.Qt.MiterJoin)
        self.item.setPen(pen)
    
class doorDelegate(surfacePolygonDelegate):
    
    def setStyle(self):
        pen = self.item.pen()
        pen.setColor(QtCore.Qt.darkMagenta)
        pen.setWidthF(0.3)
        pen.setJoinStyle(QtCore.Qt.MiterJoin)
        self.item.setPen(pen)
    
class ceilingDelegate(surfacePolygonDelegate):
    
    def setStyle(self):
        pen = self.item.pen()
        pen.setColor(QtCore.Qt.darkGreen)
        pen.setWidthF(0.1)
        pen.setJoinStyle(QtCore.Qt.MiterJoin)
        self.item.setPen(pen)
        brush = self.item.brush()
        brush.setColor(QtCore.Qt.green)
        brush.setStyle(QtCore.Qt.SolidPattern)
        self.item.setBrush(brush)
    
    
class floorDelegate(surfacePolygonDelegate):
    
    def setStyle(self):
        pen = self.item.pen()
        pen.setColor(QtCore.Qt.darkGray)
        pen.setWidthF(0.1)
        pen.setJoinStyle(QtCore.Qt.MiterJoin)
        self.item.setPen(pen)
        brush = self.item.brush()
        brush.setColor(QtCore.Qt.gray)
        brush.setStyle(QtCore.Qt.SolidPattern)
        self.item.setBrush(brush)
    
 
    