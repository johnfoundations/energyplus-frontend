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

from PyQt4 import QtCore,QtGui
import graphicitems
import zonecreate
import conversion
import verticemath

class zoneCreateDialog(QtGui.QDialog):
    def __init__ (self, model,parent = None):
        QtGui.QDialog.__init__(self,parent)
        self.model = model
        mainlayout = QtGui.QVBoxLayout(self)
        zl = QtGui.QGridLayout()
        self.zonename = QtGui.QLineEdit()
        zl.addWidget(QtGui.QLabel("Zone Name"),0,0)
        zl.addWidget(self.zonename,0,1)
        zl.addWidget(QtGui.QLabel("Units"),0,2)
        self.units = QtGui.QComboBox()
        self.units.addItems(('SI','IP'))
        zl.addWidget(self.units,0,3)
        zl.addWidget(QtGui.QLabel('Zone Origin x,y,z'),1,0)
        self.origin = QtGui.QLineEdit()
        orx = QtCore.QRegExp("[0-9]*(\\.[0-9]*)?,[0-9]*(\\.[0-9]*)?,[0-9]*(\\.[0-9]*)?");
        ovalidator = QtGui.QRegExpValidator(orx, None);
        self.origin.setValidator(ovalidator)
        zl.addWidget(self.origin,1,1)
        zl.addWidget(QtGui.QLabel('Zone Height Z axis'),2,0)
        self.zoneheight = QtGui.QLineEdit()
        self.zoneheight.setValidator(QtGui.QDoubleValidator(None))
        zl.addWidget(self.zoneheight,2,1)
        mainlayout.addLayout(zl)
        self.buttongroup = QtGui.QButtonGroup()
        self.bywidthlength = QtGui.QRadioButton('By Width and Length')
        self.widthlengthgroupbox = QtGui.QGroupBox()
        lwl = QtGui.QHBoxLayout()
        lwl.addWidget(QtGui.QLabel('Width, X axis'))
        self.widthlengthwidth = QtGui.QLineEdit()
        self.widthlengthwidth.setValidator(QtGui.QDoubleValidator(None))
        lwl.addWidget(self.widthlengthwidth)
        lwl.addWidget(QtGui.QLabel('Length, Y axis'))
        self.widthlengthlength = QtGui.QLineEdit()
        self.widthlengthlength.setValidator(QtGui.QDoubleValidator(None))
        lwl.addWidget(self.widthlengthlength)
        self.widthlengthgroupbox.setLayout(lwl)
        mainlayout.addWidget(self.bywidthlength)
        mainlayout.addWidget(self.widthlengthgroupbox)
        self.bypoints = QtGui.QRadioButton('By Points, Start at bottom left, clockwise. x,y,z')
        mainlayout.addWidget(self.bypoints)
        self.buttongroup.addButton(self.bywidthlength,0)
        self.buttongroup.addButton(self.bypoints,1)
        self.bypointsgroupbox = QtGui.QGroupBox()
        ptl = QtGui.QHBoxLayout()
        ptlc = QtGui.QVBoxLayout()
        self.fromorigin = QtGui.QCheckBox('Relative to origin')
        self.fromorigin.setChecked(True)
        ptlc.addWidget(self.fromorigin)
        ptlc.addWidget(QtGui.QLabel('Point coordinates:'))
        self.pcoord = QtGui.QLineEdit()
        rx = QtCore.QRegExp("[0-9]*,[0-9]*,[0-9]*");
        validator = QtGui.QRegExpValidator(orx, None);
        self.pcoord.setValidator(validator)
        ptlc.addWidget(self.pcoord)
        ptlc.addStretch()
        ptl.addLayout(ptlc)
        ptlbutt = QtGui.QVBoxLayout()
        self.addbutton = QtGui.QPushButton('&Add Point')
        self.delbutton = QtGui.QPushButton('Delete Point')
        self.delbutton.setEnabled(False)
        self.addbutton.setEnabled(False)
        ptlbutt.addWidget(self.addbutton)
        ptlbutt.addWidget(self.delbutton)
        ptlbutt.addStretch()
        ptl.addLayout(ptlbutt)
        self.pointlist = QtGui.QListWidget()
        ptl.addWidget(self.pointlist)
        self.bypointsgroupbox.setLayout(ptl)
        mainlayout.addWidget(self.bypointsgroupbox)
        self.connect(self.buttongroup, QtCore.SIGNAL('buttonClicked ( int)'),self.bybuttonclicked)
        self.connect(self.addbutton, QtCore.SIGNAL('clicked(bool)'), self.addbuttonclicked)
        self.connect(self.delbutton, QtCore.SIGNAL('clicked(bool)'), self.delbuttonclicked)
        self.connect(self.pcoord,QtCore.SIGNAL('textChanged (QString)'),self.editchanged)
        self.connect(self.pointlist,QtCore.SIGNAL('itemSelectionChanged ()'),self.pointlistselected)
        self.buttonBox = QtGui.QDialogButtonBox(QtGui.QDialogButtonBox.Ok | QtGui.QDialogButtonBox.Cancel)

        self.connect(self.buttonBox, QtCore.SIGNAL('accepted()'),self.accepttest)
        self.connect(self.buttonBox, QtCore.SIGNAL('rejected()'),self.reject)
        mainlayout.addWidget(self.buttonBox)
        self.color = self.pcoord.palette().color(QtGui.QPalette.Base)
        
        self.connect(self.origin,QtCore.SIGNAL('editingFinished ()'),self.originedited)
        self.connect(self.widthlengthwidth,QtCore.SIGNAL('editingFinished ()'),self.widthedited)
        self.connect(self.widthlengthlength,QtCore.SIGNAL('editingFinished ()'),self.lengthedited)
        self.connect(self.zoneheight,QtCore.SIGNAL('editingFinished ()'),self.zoneheightedited)
#        self.connect(self.pointlist,QtCore.SIGNAL('editingFinished ()'),self.pointlistselected)
        
        self.bywidthlength.click()
        

        
        
    def bybuttonclicked(self,i):
        print 'bybuttonclicked',i
        if i == 0:
            self.bypointsgroupbox.setEnabled(False)
            self.widthlengthgroupbox.setEnabled(True)
        else:
            self.bypointsgroupbox.setEnabled(True)
            self.widthlengthgroupbox.setEnabled(False)
            #check if list has any elements
            if self.pointlist.count() == 0:
                self.pointlist.addItem('0,0,0')

#                if (self.origin.text() != ''):
#                    if self.origin.validator().validate(self.origin.text(),len(self.origin.text()))[0] == 2:
#                        self.pointlist.addItem(self.origin.text())
        
    def addbuttonclicked(self):
        self.pointlist.addItem(self.pcoord.text())
        self.pcoord.setText("")
        
    def pointlistselected(self):    
        self.delbutton.setEnabled(True)
    
    def delbuttonclicked(self):
        item = self.pointlist.takeItem(self.pointlist.currentRow())
        item = None
        
    def lineEditRed(self,lineedit,setred):
        if setred:
            p = lineedit.palette()
            p.setColor(QtGui.QPalette.Base, QtGui.QColor(255,62,62))
            lineedit.setPalette(p)
        else:
            p = lineedit.palette()
            p.setColor(QtGui.QPalette.Base, self.color)
            lineedit.setPalette(p)
        
    def editchanged(self):
        self.addbutton.setEnabled(True)

    def originedited(self):
        self.lineEditRed(self.origin,False)
    
    def widthedited(self):
        self.lineEditRed(self.widthlengthwidth,False)

    def lengthedited(self):
        self.lineEditRed(self.widthlengthlength,False)

    def zoneheightedited(self):
        self.lineEditRed(self.zoneheight,False)
    
    
    def createVList(self):
        #get stuff from dialog and create a list of 3d points defining outside perimeter of zone
        vlist = []
        if self.origin.validator().validate(self.origin.text(),len(self.origin.text()))[0] == 2:
            o = self.origin.text()
            os = o.split(',')
            ol = []
            #convert to float
            ol.append(float(os[0]))
            ol.append(float(os[1]))
            ol.append(float(os[2]))
        else:
            print 'float failed. origin'
            self.lineEditRed(self.origin,True)
            return False
            
        vlist.append(ol)
        
        if self.bywidthlength.isChecked():
            if self.widthlengthwidth.validator().validate(self.widthlengthwidth.text(),len(self.widthlengthwidth.text()))[0] == 2:
                w = float(self.widthlengthwidth.text())
            else:
                print 'float failed, width'
                self.lineEditRed(self.widthlengthwidth)
                return False
                
            if self.widthlengthlength.validator().validate(self.widthlengthlength.text(),len(self.widthlengthlength.text()))[0] == 2:
                l = float(self.widthlengthlength.text())
            else:
                print 'float failed, length'
                self.lineEditRed(self.widthlengthlength)
                return False
                
            o = []
            o.append(vlist[0][0])
            o.append(vlist[0][1] + l)
            o.append(vlist[0][2])
            vlist.append(o)
            o = []
            o.append(vlist[0][0] + w)
            o.append(vlist[0][1] + l)
            o.append(vlist[0][2])
            vlist.append(o)
            o = []
            o.append(vlist[0][0] + w)
            o.append(vlist[0][1])
            o.append(vlist[0][2])
            vlist.append(o)
        
        else:
            pvlist = []
            for i in self.pointlist.items():
                o = i.data().toPyObject()
                ol = o.split(',')
                #convert to float
                try:
                    ol[0] = float(ol[0])
                    ol[1] = float(ol[1])
                    ol[2] = float(ol[2])
                except:
                    print 'float failed, pointlist',ol
                    return False
                pvlist.append(ol)
                
            if self.fromorigin.checkState() == 2:
                for v in pvlist:
                    vlist.append([[verticemath.add(v[0],vlist[0][0])],
                                  [verticemath.add(v[1],vlist[0][1])],
                                  [verticemath.add(v[2],vlist[0][2])]])
                                  
            else:
                for v in pvlist:
                    vlist.append(v)
            
        
        if self.units.currentIndex() == 1:
            #ip units
            iplist = []
            for v in vlist:
                ipitem = []
                ipitem.append(conversion.convertFrom('m',v[0])[1])
                ipitem.append(conversion.convertFrom('m',v[1])[1])
                ipitem.append(conversion.convertFrom('m',v[2])[1])
                iplist.append(ipitem)
            return iplist
        else:
            return vlist
        

    def accepttest(self):
        vlist = self.createVList()
        print vlist
        if vlist == False:
            return
        
        if self.zoneheight.validator().validate(self.zoneheight.text(),len(self.zoneheight.text()))[0] == 2:
            zh = float(self.zoneheight.text())
        else:
            print 'float failed, length'
            self.lineEditRed(self.zoneheight)
            return

        zc = zonecreate.zoneCreate(self.model,vlist,zh,self.zonename.text())
        self.accept()
        

if __name__ == "__main__":
    import sys
    from PyQt4 import QtGui

    app = QtGui.QApplication(sys.argv)
    view = zoneCreateDialog(None)
    view.show()
    sys.exit(app.exec_())
        
        
        