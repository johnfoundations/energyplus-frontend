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


class zoneScene(QtGui.QGraphicsScene):
    def __init__(self,parent = None):
        QtGui.QGraphicsScene.__init__(self,parent)
        self.model = None
        #rotation around axis' set by view
        self.viewpoint = [0.0,0.0,0.0]
        #set by view
        self.z = 0

        self.rootgroup = self.createItemGroup([])

    def setViewPoint(self,x,y,z):
        self.viewpoint = [x,y,z]
        

    def setZView(self,z):
        self.z = z


    def setModel(self,model):
        print 'zoneScene.setModel',model
        self.model = model


    def drawItems(self,painter,numItems, items, options,widget = None ):
        print 'drawItems',self.model

        for i in items:
            i.setViewpoint(self.viewpoint)
            i.setZVisible(self.z)

        QtGui.QGraphicsScene.drawItems(self,painter,numItems,items,options,widget)

    def createZoneDelegate(self,index):
        #returns delegate of the right type
        


    def createItems(self,parent,parentindex):
        #recursive
        if self.model == None:
            return

        for r in range(self.model.rowCount(parentindex)):
            index = self.model.index(r,0,parentindex)
            zitem = graphicitems.zoneitem(parent)
            #zoneitem is a graphicsitem. delegate is what handles all the model and data, and sets the graphicitem information
            zitem.setDelegate(createZoneDelegate(index))
            self.createItems(zitem,index)

    def initializeItems(self):
        self.createItems(self.rootgroup,QtCore.QModelIndex())
            
        