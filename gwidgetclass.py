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


import idfglobals
from PyQt4 import QtGui, QtCore
import sys
import math



class GEditWidget(QtGui.QLineEdit):
  def __init__(self,parent=None):
    QtGui.QLineEdit.__init__(self,parent)


  def getValue(self) :
    return self.text()

  def setValue(self,value) :
    self.setText(value)


class GTimeWidget(GEditWidget):

  def getEditWidget(self):
    e = QtGui.QLineEdit()
    rx = QtCore.QRegExp('[0-9]{2}:[0-6]{2}')
    e.setValidator(QtGui.QRegExpValidator(rx,e))
    return e



class GFloatSpinboxWidget(GEditWidget):
  def __init__(self,parent = None):
    QtGui.QWidget.__init__(self,parent)
    vert = QtGui.QHBoxLayout(self)
    self.edit = self.getEditWidget()
    vert.addWidget(self.edit)
    valuechanged = False

  def getEditWidget(self):
    return QtGui.QDoubleSpinBox()

  def setMinimum(self,val):
    self.edit.setMinimum(val)

  def setMaximum(self,val):
    self.edit.setMaximum(val)

  def setValue(self,value):
    self.edit.setValue(value)

  def value(self) :
    return self.edit.value()


class GSpinboxWidget(GFloatSpinboxWidget):

  def getEditWidget(self):
    return QtGui.QSpinBox()

class GComboBox(GFloatSpinboxWidget):

  def getEditWidget(self):
    return QtGui.QComboBox()

  def addItems(self,items) :
    self.edit.addItems(items)

  def addItem(self,item):
    self.edit.addItem(item)

  def setCurrentIndex(self,index):
    self.edit.setCurrentIndex(index)

  def connectSignal(self):
    self.connect(self.edit,QtCore.SIGNAL('currentIndexChanged(int)'),self.changed)








class GAutoCalcRealWidget(QtGui.QWidget):
  def __init__(self,parent=None):
    QtGui.QWidget.__init__(self,parent)
    vert = QtGui.QHBoxLayout(self)
    self.cb = QtGui.QCheckBox('Auto')
    self.cb.setChecked(True)
    vert.addWidget(self.cb)
    self.edit = QtGui.QDoubleSpinBox()
    self.edit.setEnabled(False)
    vert.addWidget(self.edit)
    self.valuechanged = False
    self.connect(self.cb, QtCore.SIGNAL('stateChanged (int)'),self.boxChanged)
    self.connect(self.edit,QtCore.SIGNAL('valueChanged(int)'),self.changed)
    
  def boxChanged(self,i) :
    self.edit.setEnabled(not i)
    self.valuechanged = True

  def getValue(self):
    if self.cb.checked():
      return 'autocalculate'
    else:
      return self.edit.value()


  def setValue(self,value):
#    print value
    if not value.__class__.__name__ == 'int':
      v = value.lower()
    else:
      v = value
    if v == 'autocalculate' or v == 'autosize' :
      self.cb.setChecked(True)
    else:
      self.cb.setChecked(False)
      try:
        v = float(v)
      except:
        try:
          v = int(v)
          v = float(v)
        except:
          print value + 'cannot be converted to float'
      self.edit.setValue(v)

  def setMinimum(self,value):
    self.edit.setMinimum(value)
    
  def setMaximum(self,value):
    self.edit.setMaximum(value)


#class GExtensibleWidget(QtGui.QWidget):
 # pass



    


if __name__ == "__main__":
  app = QtGui.QApplication(sys.argv)
  view = GVerticeWidget('Test')
  view.buildVerticeArray('38.2,44.5,60.0')
  view.setWindowTitle("Widget test")
  view.show()
  sys.exit(app.exec_())
  
