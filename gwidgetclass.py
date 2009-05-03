# -*- coding: utf-8 -*-


import idfglobals
from PyQt4 import QtGui, QtCore pyqt

class GEditWidget(QWidget):
  def __init__(self,label, parent=None):
    QWidget.__init__(self,parent)
    vert = QtGui.QVBoxLayout(self)
    vert.addWidget(QtGui.QLabel(label))
    self.edit = QtGui.QLineEdit()
    self.valuechanged = False
    self.connect(self.edit, QtCore.SIGNAL('textChanged (const QString&)'),self.changed)
    self.activeObjectChanged)

  def setToolTip(self,tt):
    self.edit.setToolTip(tt)

  def value(self) :
    return self.edit.text()

  def setValue(self,value) :
    self.edit.setText(value)

  def changed(self,string):
    self.valuechanged = True
  


class GAutoCalcRealWidget(QWidget):
  pass





class GExtensibleWidget(QWidget):
  pass


class GVerticeWidget(QWidget):
  pass