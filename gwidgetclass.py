# -*- coding: utf-8 -*-


import idfglobals
from PyQt4 import QtGui, QtCore
import sys
import math



class GEditWidget(QtGui.QWidget):
  def __init__(self,label, parent=None):
    QtGui.QWidget.__init__(self,parent)
    vert = QtGui.QHBoxLayout(self)
    vert.addWidget(QtGui.QLabel(label))
    self.edit = self.getEditWidget()
    vert.addWidget(self.edit)
    self.valuechanged = False
    self.connectSignal()

  def getEditWidget(self):
    return QtGui.QLineEdit()

  def connectSignal(self):
    self.connect(self.edit, QtCore.SIGNAL('textChanged (const QString&)'),self.changed)

  def setToolTip(self,tt):
    self.edit.setToolTip(tt)

  def value(self) :
    return self.edit.text()

  def setValue(self,value) :
    self.edit.setText(value)

  def changed(self,string):
    self.valuechanged = True
  
class GTimeWidget(GEditWidget):

  def getEditWidget(self):
    e = QtGui.QLineEdit()
    rx = QtCore.QRegExp('[0-9]{2}:[0-6]{2}')
    e.setValidator(QtGui.QRegExpValidator(rx,e))
    return e



class GFloatSpinboxWidget(GEditWidget):
  def __init__(self,label,parent = None):
    QtGui.QWidget.__init__(self,parent)
    vert = QtGui.QHBoxLayout(self)
    vert.addWidget(QtGui.QLabel(label))
    self.edit = self.getEditWidget()
    vert.addWidget(self.edit)
    valuechanged = False

  def connectSignal(self):
    self.connect(self.edit,QtCore.SIGNAL('valueChanged(int)'),self.changed)

  def getEditWidget(self):
    return QtGui.QDoubleSpinBox()

  def setMinimum(self,val):
    self.edit.setMinimum(val)

  def setMaximum(self,val):
    self.edit.setMaximum(val)

  def setValue(self,value):
    print value
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








class GAutoCalcRealWidget(GEditWidget):
  def __init__(self,label, parent=None):
    QtGui.QWidget.__init__(self,parent)
    vert = QtGui.QHBoxLayout(self)
    vert.addWidget(QtGui.QLabel(label))
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
  