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
    print value
    v = value.lower()
    if v == 'autocalculate' :
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
    self.width.setValidator(QtGui.QDoubleValidator(self.width))
    self.height = QtGui.QLineEdit()
    self.height.setValidator(QtGui.QDoubleValidator(self.width))
    hl.addWidget(self.width)
    hl.addWidget(self.height)
    vlayout.addLayout(hl)
    hl = QtGui.QHBoxLayout()
    self.tlxyz = QtGui.QLineEdit()
    rx = QtCore.QRegExp('[0-9]+\.[0-9]+,[0-9]+\.[0-9]+,[0-9]+\.[0-9]+')
    self.tlxyz.setValidator(QtGui.QRegExpValidator(rx,self.tlxyz))
    self.trxyz = QtGui.QLineEdit()
    self.trxyz.setValidator(QtGui.QRegExpValidator(rx,self.trxyz))
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
    self.blxyz.setValidator(QtGui.QRegExpValidator(rx,self.blxyz))
    self.brxyz = QtGui.QLineEdit()
    self.brxyz.setValidator(QtGui.QRegExpValidator(rx,self.brxyz))
    hl.addWidget(self.blxyz)
    hl.addWidget(self.brxyz)
    vlayout.addLayout(hl)
    self.connectSignal()
    self.fieldmatrix = []
    
  def connectSignal(self):
    self.connect(self.verticecount, QtCore.SIGNAL('valueChanged (int)'),self.changedCount)
    self.connect(self.width, QtCore.SIGNAL('editingFinished ()'),self.changedWidth)
    self.connect(self.height, QtCore.SIGNAL('editingFinished ()'),self.changedHeight)
    self.connect(self.tlxyz, QtCore.SIGNAL('editingFinished()'),self.changedtl)
    self.connect(self.trxyz, QtCore.SIGNAL('editingFinished()'),self.changedtr)
    self.connect(self.blxyz, QtCore.SIGNAL('editingFinished()'),self.changedbl)
    self.connect(self.brxyz, QtCore.SIGNAL('editingFinished()'),self.changedbr)
  
  def changedCount(self,i):
    pass

  def buildVerticeString(self,arr):
    stri = '%g,%g,%g'%(arr[0],arr[1],arr[2])
    return stri

  def getFieldMatrix(self):
    vmatrix = []
    vmatrix.append(self.buildVerticeArray(self.blxyz.text()))
    vmatrix.append(self.buildVerticeArray(self.brxyz.text()))
    vmatrix.append(self.buildVerticeArray(self.trxyz.text()))
    vmatrix.append(self.buildVerticeArray(self.tlxyz.text()))
    fill = [0.0,0.0,0.0]
    for c,l in enumerate(vmatrix):
      if len(l) == 0:
        vmatrix[c] = fill
    return vmatrix

  def setFieldMatrix(self,matrix):
    self.blxyz.setText(self.buildVerticeString(matrix[0]))
    self.brxyz.setText(self.buildVerticeString(matrix[1]))
    self.trxyz.setText(self.buildVerticeString(matrix[2]))
    self.tlxyz.setText(self.buildVerticeString(matrix[3]))
    self.fieldmatrix = matrix

  def mstrtofloat(self,m) :
    p = []
    mm = []
    for pt in m:
      for i in pt:
        try:
          t = float(i)
        except:
          try:
            t = int(i)
            t = float(i)
          except:
            t = 0.0
        p.append(t)
      mm.append(p)
    return mm
   

  def setValue(self,m):
    mm = self.mstrtofloat(m)
    wv = self.transform(mm[0],mm[1])
    self.width.setText(str(abs(self.dist(wv))))
    hv = self.transform(mm[0],mm[3])
    self.height.setText(str(abs(self.dist(hv))))
    self.setFieldMatrix(mm)
    
  def dist(self,v):
    return math.sqrt(math.pow(v[0],2) + math.pow(v[1],2) + math.pow(v[2],2))
    

  def getValue(self):
    return self.fieldmatrix


  def buildVerticeArray(self,s):
    l = s.split(',')
    f = []
    try:
      f.append(float(l[0]))
    except:
      return []
    try:
      f.append(float(l[1]))
    except:
      return []
    try:
      f.append(float(l[2]))
    except:
      return []
    return f

  def transform(self,v1,v2):
    res = [0,0,0]
    res[0] = v2[0] - v1[0]
    res[1] = v2[1] - v1[1]
    res[2] = v2[2] - v1[2]
    return res

  def add(self,v1,v2)  :
    res = [0,0,0]
    res[0] = v2[0] + v1[0]
    res[1] = v2[1] + v1[1]
    res[2] = v2[2] + v1[2]
    return res

  def mult(self,v1,m):
    res = [0,0,0]
    res[0] = v1[0] *m
    res[1] = v1[1] *m
    res[2] = v1[2] *m
    return res
    
  def changedWidth(self):
    n = float(self.width.text())
    bla = self.buildVerticeArray(self.blxyz.text())
    if not len(bla) == 3:
      return
    else:
      matrix = self.getFieldMatrix()
      normbr = self.transform(matrix[0],matrix[1])
      dist = self.dist(normbr)
      if dist == 0:
        delta = n
      else:
        delta = n/dist
      br =  self.mult(normbr,delta)
      matrix[1] = self.add(br,matrix[0])
      normbr = self.transform(matrix[3],matrix[2])
      print normbr
      dist = self.dist(normbr)
      print dist
      if dist == 0:
        delta = n
      else:
        delta = n/dist
      print delta
      br =  self.mult(normbr,delta)
      print br
      matrix[2] = self.add(br,matrix[3])
      self.setFieldMatrix(matrix)

  def changedHeight(self):
    n = float(self.height.text())
    bla = self.buildVerticeArray(self.blxyz.text())
    if not len(bla) == 3:
      return
    else:
      matrix = self.getFieldMatrix()
      normbr = self.transform(matrix[0],matrix[3])
      dist = math.sqrt(math.pow(normbr[0],2) + math.pow(normbr[1],2) + math.pow(normbr[2],2))
      if dist == 0:
        delta = n
      else:
        delta = n/dist
      br =  self.mult(normbr,delta)
      matrix[3] = self.add(br,matrix[0])
      normbr = self.transform(matrix[1],matrix[2])
      dist = math.sqrt(math.pow(normbr[0],2) + math.pow(normbr[1],2) + math.pow(normbr[2],2))
      if dist == 0:
        delta = n
      else:
        delta = n/dist
      br =  self.mult(normbr,delta)
      matrix[2] = self.add(br,matrix[1])
      self.setFieldMatrix(matrix)
        
    
  def changedtl(self):
    pass
    
  def changedtr(self):
    pass
    
  def changedbr(self):
    matrix = self.getFieldMatrix()
    if len(self.fieldmatrix) == 0:
      matrix[0] = [0,0,0]
      matrix[2] = [1,0,1]
      matrix[3] = [0,0,1]
      self.setFieldMatrix(matrix)
      self.changedWidth()
      self.changedHeight()
      return
    diff = self.transform(self.fieldmatrix[1],matrix[1])
    matrix[2] = self.add(matrix[2],diff)
    self.setFieldMatrix(matrix)
      
    
  def changedbl(self):
    matrix = self.getFieldMatrix()
    if len(self.fieldmatrix) == 0:
      matrix[1] = [1,0,0]
      matrix[2] = [1,0,1]
      matrix[3] = [0,0,1]
      self.setFieldMatrix(matrix)
      self.changedWidth()
      self.changedHeight()
      return
    diff = self.transform(self.fieldmatrix[0],matrix[0])
    matrix[1] = self.add(matrix[1],diff)
    matrix[2] = self.add(matrix[2],diff)
    matrix[3] = self.add(matrix[3],diff)
    self.setFieldMatrix(matrix)
    





    


if __name__ == "__main__":
  app = QtGui.QApplication(sys.argv)
  view = GVerticeWidget('Test')
  view.buildVerticeArray('38.2,44.5,60.0')
  view.setWindowTitle("Widget test")
  view.show()
  sys.exit(app.exec_())
  
