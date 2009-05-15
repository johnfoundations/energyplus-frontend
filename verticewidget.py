# -*- coding: utf-8 -*-

from PyQt4 import QtGui, QtCore
from gwidgetclass import *

class GVerticeWidget(QtGui.QWidget):
  def __init__(self,label,parent=None) :
    QtGui.QWidget.__init__(self,parent)
    vlayout = QtGui.QVBoxLayout(self)
    self.verticecount = GAutoCalcRealWidget('Vertice Count')
    vlayout.addWidget(self.verticecount)
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
    self.calcbutton = QtGui.QPushButton("X,Y,Z")
    self.calcbutton.setToolTip('Press to calculate.\nEnter the width and height, starting point in bottom left.')
    hl.addWidget(self.calcbutton)
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
#    self.connect(self.width, QtCore.SIGNAL('editingFinished ()'),self.changedWidth)
#    self.connect(self.height, QtCore.SIGNAL('editingFinished ()'),self.changedHeight)
#    self.connect(self.tlxyz, QtCore.SIGNAL('editingFinished()'),self.changedtl)
#    self.connect(self.trxyz, QtCore.SIGNAL('editingFinished()'),self.changedtr)
#    self.connect(self.blxyz, QtCore.SIGNAL('editingFinished()'),self.changedbl)
#    self.connect(self.brxyz, QtCore.SIGNAL('editingFinished()'),self.changedbr)
    self.connect(self.calcbutton,QtCore.SIGNAL('clicked (bool)'),self.calcpushed)


  def calcpushed(self):
    w = float(self.width.text())
    h = float(self.height.text())
    bla = self.buildVerticeArray(self.blxyz.text())
    if not len(bla) == 3:
      return
     
    matrix = self.getFieldMatrix()
    normbr = self.transform(matrix[1],matrix[2])
    dist = self.dist(normbr)
    if dist == 0:
      delta = w
    else:
      delta = w/dist
    br =  self.mult(normbr,delta)
    matrix[2] = self.add(br,matrix[1])
    normtl = self.transform(matrix[1],matrix[0])
    dist = self.dist(normtl)
    if dist == 0:
      delta = h
    else:
      delta = h/dist
    tl =  self.mult(normtl,delta)
    matrix[0] = self.add(tl,matrix[1])
    normtr = self.transform(matrix[2],matrix[3])
    dist = self.dist(normtr)
    if dist == 0:
      delta = h
    else:
      delta = h/dist
    tr =  self.mult(normtr,delta)
    matrix[3] = self.add(tr,matrix[2])
    self.setFieldMatrix(matrix)
              


    
      
  def changedCount(self,i):
    pass

  def buildVerticeString(self,arr):
    stri = '%g,%g,%g'%(arr[0],arr[1],arr[2])
    return stri
    
  def getFieldMatrix(self):
    vmatrix = []
    vmatrix.append(self.buildVerticeArray(self.tlxyz.text()))
    vmatrix.append(self.buildVerticeArray(self.blxyz.text()))
    vmatrix.append(self.buildVerticeArray(self.brxyz.text()))
    vmatrix.append(self.buildVerticeArray(self.trxyz.text()))
    fill = [0.0,0.0,0.0]
    for c,l in enumerate(vmatrix):
      if len(l) == 0:
        vmatrix[c] = fill
    return vmatrix
            
  def setFieldMatrix(self,matrix):
    self.tlxyz.setText(self.buildVerticeString(matrix[0]))
    self.blxyz.setText(self.buildVerticeString(matrix[1]))
    self.brxyz.setText(self.buildVerticeString(matrix[2]))
    self.trxyz.setText(self.buildVerticeString(matrix[3]))
    self.fieldmatrix = matrix

  def mstrtofloat(self,m) :
    p = []
    mm = []
    c = 0
    for i in m:
      try:
        t = float(i)
      except:
        try:
          t = int(i)
          t = float(i)
        except:
          t = 0.0
      p.append(t)
      c = c+1
      if c == 3 :
        c = 0
        mm.append(p)
        p = []
    return mm
                              
                              
  def setValue(self,m):
    print m[0]
    print m[1]
    self.verticecount.setValue(m[0])
    mm = self.mstrtofloat(m[1])
    print mm
    wv = self.transform(mm[1],mm[2])
    print wv
    self.width.setText(str(abs(self.dist(wv))))
    hv = self.transform(mm[1],mm[0])
    print hv
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
                                                                                            
                                                                                            
                                                                                            
                                                                                            
                                                                                            
                                                                                            