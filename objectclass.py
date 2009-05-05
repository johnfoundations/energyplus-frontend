# -*- coding: utf-8 -*-
import idfglobals

import pdb
from PyQt4 import QtGui, QtCore


#base class for all the defined objects.
#each one is created as a subclass of ObjectAbstract,
#and it's init will create the fields and append them to the field list
class ObjectAbstract :
  def __init__(self):
    self.classn = ''
    self.name = ''
    self.fieldlist = []
    self.required = False
    self.referencelist = []
    self.rawdatalist = []
    self.group = ''
    self.extensible = False
    self.editwidget = None
    self.memo = []
    self.CreateFields()
    
  def setName(self,name):
    self.name = name

  def getName(self):
    if self.name == '':
      return self.getClassnameIDD()
    else:
      return self.name

  def setClassnameIDD(self,name):
    self.classn = name

  def getClassnameIDD(self):
    return self.classn
  
  def InsertField(self,field):
    self.fieldlist.append(field)
  
  def setData(self,data):
    self.rawdatalist = data
    self.ParseRawData()

  def getData(self) :
    print self.getClassnameIDD() + ' getData not implemented'
    
  def CreateEditWidget(self) :
    self.editwidget = QtGui.QWidget()
    vlayout = QtGui.QVBoxLayout(self.editwidget)
    label = QtGui.QLabel(self.getClassnameIDD())
    ms = ''
    for m in self.memo:
      ms = ms + m + '\n'
    ms = ms.strip()
    label.setToolTip(ms)
    vlayout.addWidget(label)
    for f in self.fieldlist:
      vlayout.addWidget(f.CreateEditor())
      f.setEditorValue()
    vlayout.addStretch()
    return self.editwidget

  def closeWidget(self):
    if self.editwidget :
      self.editwidget.close()

  def CreateFields(self) :
    print 'to be subclassed'

  def PrintIDF(self,fh) :
    print(self.getClassnameIDD() + ',\n')
    for c,fn in enumerate(self.fieldlist):
      if c < len(self.fieldlist)-1:
        sep = ','
      else:
        sep= ';'
      fn.printIDF(sep)
      


  def setRequired(self,req) :
    self.required = req
  
  def getRequired(self):
    return self.required

  def setMinfields(self,num):
    self.minfields = num

  def getMinfields(self):
    return self.minfields

  def insertMemo(self,memo):
    self.memo = memo

  def getMemo(self) :
    return self.memo

  def addReference(self,ref):
    self.referencelist.append(ref)

  def getReference(self) :
    return self.referencelist

  def setGroup(self,g) :
    self.group = g

  def getGroup(self):
    return self.group

  def setExtensible(self,num) :
    self.extensible = num

  def getDepends(self):
    dependslist = []
    for f in self.fieldlist :
      if f.getFieldDepends():
        dependslist.append(f.getFieldDepends())
    return dependslist

  def ParseRawData(self) :
    remainder = []
    remainder = self.rawdatalist[:]
#    print remainder
#    pdb.set_trace()
    for i in range(len(self.rawdatalist)):
      if i == 0:
        del remainder[0]
        continue

      if i <= len(self.fieldlist):
        f = self.fieldlist[i-1]
      else:
        if not self.extensible:
          pdb.set_trace()
          print 'ran out of fieldlists ' + self.getClassnameIDD()
          return
      d = self.rawdatalist[i]
      del remainder[0]
      if not f.setValue(d,remainder):
        print 'parserawdata setvalue false ' + d + ' ' + self.getClassnameIDD()
        return


class ObjectVertice(ObjectAbstract):
  pass
    
      

class ObjectViewFactor(ObjectAbstract):
  pass
    
     

class ObjectFluidProperty(ObjectAbstract) :
  pass
    
      

class ObjectSingleLine(ObjectAbstract) :
  pass
    
      

class ObjectCompactSchedule(ObjectAbstract) :
  pass
    
      

class ObjectSpectral(ObjectAbstract) :
  pass
  
    
      

        
  