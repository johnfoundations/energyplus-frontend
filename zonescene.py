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

from PyQt4 import QtCore, QtGui
import zlayers
import graphicitems
import classinfo

class zoneScene(QtGui.QGraphicsScene):
    def __init__(self,parent = None):
        QtGui.QGraphicsScene.__init__(self,parent)
        self.model = None
        self.itemwithfocus = None
        self.statusbar = None
        #rotation around axis' set by view
        self.rotation = [0.0,0.0,0.0]
        #set by view
        self.z = 0

        self.rootgroup = None
        


    def setRotation(self,xyz):
        self.rotation = [xyz[0],xyz[1],xyz[2]]
        

    def setZView(self,inc):
        if self.itemwithfocus != None:
            self.itemwithfocus.item.setZVisible(inc)
            
        else:
            self.rootgroup.item.setZVisible(inc)
            



    def setModel(self,model):
#        print 'zoneScene.setModel',model
        self.model = model
        self.connect(self.model, QtCore.SIGNAL('modelreset()'), self.initializeItems)


#    def drawItems(self, painter, items, options, widget = None):
#        print 'scene drawItems'
#        for i in items:
#            i.setViewpoint(self.viewpoint)
            
#        for i in items.childItems():
#            i.setZVisible(self.z)
#        print 'drawItems qgraphicsscene.................................................'
#        QtGui.QGraphicsScene.drawItems(self,painter,items,options,widget)

    def createZoneDelegate(self,index):
        #returns delegate of the right type
        t = classinfo.constructionType(index.internalPointer().data.idfclass)
        
        if t == 'Zone':
            return graphicitems.zoneDelegate(index)
            
        if t == 'Wall':
            return graphicitems.wallDelegate(index)
        
        if t == 'Floor':
            return graphicitems.floorDelegate(index)
        
        if t == 'Window':
            return graphicitems.windowDelegate(index)
        
        if t == 'Door':
            return graphicitems.doorDelegate(index)
        
        if t == 'RoofCeiling':
            return graphicitems.ceilingDelegate(index)
        
        return graphicitems.surfacePolygonDelegate(index)
        


    def createItems(self,parent,parentindex):
        #recursive
        if self.model == None:
            return
        
        for r in range(self.model.rowCount(parentindex)):
            index = self.model.index(r,0,parentindex)
            zitem = graphicitems.zoneItem(parent,self)
            self.createItems(zitem,index)
            zitem.setDelegate(self.createZoneDelegate(index))


    def initializeItems(self):
        self.clear()
        self.rootgroup = graphicitems.zoneItem(None,self)
        self.rootgroup.setDelegate(graphicitems.buildingDelegate(QtCore.QModelIndex()))
        self.createItems(self.rootgroup,QtCore.QModelIndex())
        self.rootgroup.delegate.buildZ()
        
        
    def setViewPoint(self,rotation,z):
        self.rootgroup.delegate.setRotation(rotation)
        self.setRotation(rotation)
        self.rootgroup.setZVisible(z)
        self.setZView(z)
        self.rootgroup.doPolygon()
        
    def focusInEvent(self,event):
        print 'zoneScene focusInEvent'
        QtGui.QGraphicsScene.focusInEvent(self,event)


