# -*- coding: utf-8 -*-
import idfglobals
import pdb


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
  
  def CreateEditWidget(self) :
    print 'not implemented'

  def CreateFields(self) :
    print 'to be subclassed'

  def PrintIDF(self,fh) :
    print 'not implemented'

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
#    pdb.set_trace()
    for i in range(len(self.rawdatalist)):
      if i == 0:
        del remainder[0]
        continue

      if i <= len(self.fieldlist):
        f = self.fieldlist[i-1]
      else:
 #       pdb.set_trace()
        print 'ran out of fieldlists ' + self.getClassnameIDD()
        return
      d = self.rawdatalist[i]
      del remainder[0]
      if not f.setValue(d,remainder):
        print 'parserawdata setvalue false ' + d + ' ' + self.getClassnameIDD()
        return


class ObjectVertice(ObjectAbstract):
  def CreateEditWidget(self) :
    print 'not implemented'
    
  def CreateFields(self) :
    print 'to be subclassed'
      
  def PrintIDF(self,fh) :
    print 'not implemented'

class ObjectViewFactor(ObjectAbstract):
  def CreateEditWidget(self) :
    print 'not implemented'
    
  def CreateFields(self) :
    print 'to be subclassed'
     
  def PrintIDF(self,fh) :
    print 'not implemented'

class ObjectFluidProperty(ObjectAbstract) :
  def CreateEditWidget(self) :
    print 'not implemented'
    
  def CreateFields(self) :
    print 'to be subclassed'
      
  def PrintIDF(self,fh) :
    print 'not implemented'

class ObjectSingleLine(ObjectAbstract) :
  def CreateEditWidget(self) :
    print 'not implemented'
    
  def CreateFields(self) :
    print 'to be subclassed'
      
  def PrintIDF(self,fh) :
    print 'not implemented'

class ObjectCompactSchedule(ObjectAbstract) :
  def CreateEditWidget(self) :
    print 'not implemented'
    
  def CreateFields(self) :
    print 'to be subclassed'
      
  def PrintIDF(self,fh) :
    print 'not implemented'

class ObjectSpectral(ObjectAbstract) :
  def CreateEditWidget(self) :
    print 'not implemented'
  
  def CreateFields(self) :
    print 'to be subclassed'
    
  def PrintIDF(self,fh) :
    print 'not implemented'
      

        
  