# -*- coding: utf-8 -*-

from PyQt4 import QtGui
import idfglobals
import pdb


class FieldAbstract :
  def __init__(self,parent,fieldname,default,notes):
    self.fieldeditor = 0
    self.fieldname = fieldname
    self.parent = parent
    self.value = ''
    self.restoflist = []
    self.default = default
    self.notes = notes
    

  def createEditor(self):
    pass

  def getEditorValue(self) :
    return self.fieldeditor.Value()

  def setEditorValue(self):
    print self.fieldname
    self.fieldeditor.setValue(self.value)
  

  
  def setToolTips(self,notes) :
    tts = ''
    for n in notes:
      tts = tts + n + '\n'
    tts = tts.strip()
    self.fieldeditor.setToolTip(tts)

  def setValue(self,value,restoflist) :
    #pdb.set_trace()
    if self.Validate(value) :
      self.value = value
      self.restoflist = restoflist
      if self.fieldname == 'Name':
        self.parent.setName(self.value)
      
      return True
    else:
      print 'erroneous data in ' + self.fieldname
      return False

  def getValue(self):
    return self.value

  def printIDF(self,sep) :
    #pdb.set_trace()
    v = self.value
    print(self.value + sep + '! ' + self.fieldname)

  def getFieldDepends(self):
    return ''

  def Validate(self,val) :
    return True
  



class FieldReal(FieldAbstract) :
  def __init__(self,parent,fieldname,default,notes,minv,maxv,mingtv,maxltv) :
    FieldAbstract.__init__(self,parent,fieldname,default,notes)
    self.minv = minv
    self.maxv = maxv
    self.mingtv = mingtv
    self.maxltv = maxltv
    
  def CreateEditor(self)  :
    self.fieldeditor = QtGui.QDoubleSpinBox()
    if self.minv:
      self.fieldeditor.setMinimum(self.minv)
    elif self.mingtv:
      self.fieldeditor.setMinimum(self.mingtv)
    if self.maxv:  
      self.fieldeditor.setMaximum(self.maxv)
    elif self.maxltv:
      self.fieldeditor.setMaximum(self.maxltv)
    if not self.default:
      self.fieldeditor.setValue(self.default)
    self.setToolTips(self.notes)
    return self.fieldeditor

  def getEditorValue(self) :
    return self.fieldeditor.Value()

  def setEditorValue(self):
    v = float(self.value)
    self.fieldeditor.setValue(v)
  

  def Validate(self,val):
    #pdb.set_trace()
    localmin = False
    localmax = False

    if not self.minv == '':
      localmin = self.minv
    if not self.mingtv == '':
      localmin = self.mingtv
    if not self.maxv == '':
      localmax = self.maxv
    if not self.maxltv == '':
      localmax = self.maxltv
    if not localmax or not localmin or val == '':
      return True

    try:
      rval = float(val)
    except:
      print 'fieldreal validate error. Cannot convert to float' + val
      return False
    
      
    if localmax:
      if rval > localmax:
        return False
    if localmin:
      if rval < localmin:
        return False
    return True
      
    
class FieldRealAutocalculate(FieldReal) :

  def Validate(self,val):
    v = val.lower()
    if v == 'autocalculate' or v == 'autosize' :
      return True
    else:
      return FieldReal.Validate(self,val)
  
class FieldInt(FieldAbstract) :
    def __init__(self,parent,fieldname,default,notes,minv,maxv,mingtv,maxltv) :
      FieldAbstract.__init__(self,parent,fieldname,default,notes)
      self.minv = minv
      self.maxv = maxv
      self.mingtv = mingtv
      self.maxltv = maxltv

    def CreateEditor(self) : 
      self.fieldeditor = QtGui.QSpinBox()
      if self.minv:
        self.fieldeditor.setMinimum(self.minv)
      elif self.mingtv:
        self.fieldeditor.setMinimum(self.mingtv)
      if self.maxv:
        self.fieldeditor.setMaximum(self.maxv)
      elif self.maxltv:
        self.fieldeditor.setMaximum(self.maxltv)
      self.setToolTips(self.notes)
      if not self.default:
        self.fieldeditor.setValue(self.default)
      return self.fieldeditor
                  
                    
    def getEditorValue(self) :
      return self.fieldeditor.Value()

    def setEditorValue(self):
      try:
        v = int(self.value)
      except:
        try:
          v = float(self.value)
          v = int(v)
        except:
          print 'value wront for int'
      self.fieldeditor.setValue(v)


    def Validate(self,val):
      localmin = False
      localmax = False

      if not self.minv == '':
        localmin = self.minv
      if not self.mingtv == '':
        localmin = self.mingtv
      if not self.maxv == '':
        localmax = self.maxv
      if not self.maxltv == '':
        localmax = self.maxltv
      if not localmax or not localmin or val == '':
        return True
      try:
        rval = int(val)
      except:
        try:
          rval = float(val)
        except:
          print 'fieldint validate error. Cannot convert to int ' + val
          return False
        
      if localmax:
        if rval > localmax:
          return False
      if localmin:
        if rval < localmin:
          return False
      return True
                            
                        
    
class FieldText(FieldAbstract) :
  def __init__(self,parent,fieldname,default,notes):
    FieldAbstract.__init__(self,parent,fieldname,default,notes)
    self.value = ''

  def CreateEditor(self) :
    self.fieldeditor = QtGui.QLineEdit()
    if self.default:
      self.fieldeditor.setText(self.default)
    self.setToolTips(self.notes)
    return self.fieldeditor


  def getEditorValue(self) :
    return self.fieldeditor.getText()

  def setEditorValue(self):
    self.fieldeditor.setText(self.value)
      



class FieldChoice(FieldAbstract)  :
  def __init__(self,parent,fieldname,default,notes,choices):
    FieldAbstract.__init__(self,parent,fieldname,default,notes)
    self.choices = choices

  def CreateEditor(self)  :
    self.fieldeditor = QtGui.QComboBox()
    self.fieldeditor.addItems(self.choices)
    self.fieldeditor.setCurrentIndex(self.choices.index(self.default))
    self.setToolTips(self.notes)
    return self.fieldeditor

  def setEditorValue(self):
    self.fieldeditor.setCurrentIndex(self.choices.index(self.value))
  
  def getEditorValue(self):
    return self.fieldeditor.currentText()


class FieldOnOff(FieldAbstract) :
  def __init__(self,parent,fieldname,default,notes,choices) :
    FieldAbstract.__init__(self,parent,fieldname,default,notes)

  def CreateEditor(self)  :
    self.fieldeditor = QtGui.QCheckBox(self.fieldname)
    if self.default :
      self.fieldeditor.setCheckState(2)
    else:
      self.fieldeditor.setCheckState(QtGui.Qt.Unchecked)
    self.setToolTips(self.notes)
    return self.fieldeditor

  def setEditorValue(self) :
    if self.value == 'On':
      self.fieldeditor.setChecked(2)
    else:
      self.fieldeditor.setChecked(0)

  def getEditorValue(self):
    if self.fieldeditor.isChecked() :
      return 'On'
    else:
      return 'Off'

class FieldYesNo(FieldOnOff):

  def getEditorValue(self):
    if self.fieldeditor.isChecked() :
      return 'Yes'
    else:
      return 'No'

  def setEditorValue(self) :
    if self.value == 'Yes':
      self.fieldeditor.setChecked(2)
    else:
      self.fieldeditor.setChecked(0)
            

class FieldObjectlist(FieldAbstract):
  def __init__(self,parent,fieldname,default,notes,objectlistname) :
    FieldAbstract.__init__(self,parent,fieldname,default,notes)
    self.objectlistname = objectlistname

  def CreateEditor(self) :  
    self.fieldeditor = QtGui.QComboBox()
    self.choices = getActiveObjectsList(self.objectlistname)
    self.fieldeditor.addItems(self.choices)
    self.setToolTips(self.notes)
    return self.fieldeditor

  def setEditorValue(self):
    self.fieldeditor.setCurrentIndex(self.choices.index(self.value))
  
  def getEditorValue(self):
    return self.fieldeditor.currentText()

  def getFieldDepends(self):
    return self.objectlistname
    
    
class FieldVertice(FieldAbstract):
  def __init__(self,parent,fieldname,default,notes) :
    FieldAbstract.__init__(self,parent,fieldname,default,notes)

  def CreateEditor(self):
    pass





