# -*- coding: utf-8 -*-


import idfglobals
from PyQt4 import QtGui, QtCore
import sys



class GEditWidget(QtGui.QWidget):
  def __init__(self,label, parent=None):
    QtGui.QWidget.__init__(self,parent)
    vert = QtGui.QVBoxLayout(self)
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
  

class GFloatSpinboxWidget(GEditWidget):
  def __init__(self,label,parent = None):
    QtGui.QWidget.__init__(self,parent)
    vert = QtGui.QVBoxLayout(self)
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

  def setCurrentIndex(self,index):
    self.edit.setCurrentIndex(index)

  def connectSignal(self):
    self.connect(self.edit,QtCore.SIGNAL('currentIndexChanged(int)'),self.changed)








class GAutoCalcRealWidget(GEditWidget):
  def __init__(self,label, parent=None):
    QtGui.QWidget.__init__(self,parent)
    vert = QtGui.QVBoxLayout(self)
    self.cb = QtGui.QCheckBox('AutoCalculate')
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
    if value == 'autocalculate' :
      self.cb.setChecked(True)
    else:
      self.cb.setChecked(False)
      self.edit.setValue(value)



#class GExtensibleWidget(QtGui.QWidget):
 # pass


class GVerticeWidget(QtGui.QWidget):
  def __init__(self,label,parent=None) :
    QtGui.QWidget.__init__(self,parent)
    vlayout = QtGui.QVBoxLayout(self)
    self.verticecount = QtGui.QSpinBox()
    hl = QtGui.QHBoxLayout()
    hl.addWidget(QtGui.QLabel('Number of Vertices'))
    hl.addWidget(self.verticecount)
    vlayout.addLayout(hl)
    hl = QtGui.QHBoxLayout()
    hl.addWidget(QtGui.QLabel('Width'))
    hl.addWidget(QtGui.QLabel('Height'))
    vlayout.addLayout(hl)
    hl = QtGui.QHBoxLayout()
    self.width = QtGui.QLineEdit()
    self.width.setInputMask('0000.0')
    self.height = QtGui.QLineEdit()
    self.height.setInputMask('0000.0')
    hl.addWidget(self.width)
    hl.addWidget(self.height)
    vlayout.addLayout(hl)
    hl = QtGui.QHBoxLayout()
    self.tlxyz = QtGui.QLineEdit()
    self.tlxyz.setInputMask('0000.0,0000.0,0000.0')
    self.trxyz = QtGui.QLineEdit()
    self.trxyz.setInputMask('0000.0,0000.0,0000.0')
    hl.addWidget(self.tlxyz)
    hl.addWidget(self.trxyz)
    vlayout.addLayout(hl)
    hl = QtGui.QHBoxLayout()
    hl.addStretch()
    hl.addWidget(QtGui.QLabel("X,Y,Z"))
    hl.addStretch()
    vlayout.addLayout(hl)
    hl = QtGui.QHBoxLayout()
    self.blxyz = QtGui.QLineEdit()
    self.blxyz.setInputMask('0000.0,0000.0,0000.0')
    self.brxyz = QtGui.QLineEdit()
    self.brxyz.setInputMask('0000.0,0000.0,0000.0')
    hl.addWidget(self.blxyz)
    hl.addWidget(self.brxyz)
    vlayout.addLayout(hl)
    self.connectSignal()
    
  def connectSignal(self):
    self.connect(self.verticecount, QtCore.SIGNAL('valueChanged (int)'),self.changedCount)
    self.connect(self.width, QtCore.SIGNAL('editingFinished ()'),self.changedWidth)
    self.connect(self.height, QtCore.SIGNAL('textChanged (const QString&)'),self.changedHeight)
    self.connect(self.tlxyz, QtCore.SIGNAL('textChanged (const QString&)'),self.changedtl)
    self.connect(self.trxyz, QtCore.SIGNAL('textChanged (const QString&)'),self.changedtr)
    self.connect(self.blxyz, QtCore.SIGNAL('textChanged (const QString&)'),self.changedbl)
    self.connect(self.brxyz, QtCore.SIGNAL('textChanged (const QString&)'),self.changedbr)
  
  def changedCount(self,i):
    pass

  def changedWidth(self):
    n = float(self.width.text())
    print self.blxyz.text()
    if self.blxyz.text() == '':
      self.blxyz.setText('0.0.0')
    print n
    
  def changedHeight(self,i):
    n = float(i)
    print n
    
  def changedtl(self,i):
    print i
    
  def changedtr(self,i):
    print i
    
  def changedbr(self,i):
    print i
    
  def changedbl(self,i):
    print i





    


if __name__ == "__main__":
  app = QtGui.QApplication(sys.argv)
  view = GVerticeWidget('Test')
  view.setWindowTitle("Widget test")
  view.show()
  sys.exit(app.exec_())
  
