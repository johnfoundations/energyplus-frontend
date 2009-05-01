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
    

  def createEditor(self):
    pass
    
  def setToolTips(self,notes) :
    tts = ''
    for n in notes:
      tts = tts + n
      self.fieldeditor.setTooltip(tts)

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

  def PrintIDF(self,fh) :
    v = self.getValue()
    fh.write(v + '! ' + self.fieldname)

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

  def Validate(self,val):
    localmin = False
    localmax = False
    try:
      rval = val.real
    except:
      return False
    
    if not self.minv == '':
      localmin = self.minv
    if not self.mingtv == '':
      localmin = self.mingtv
    if not self.maxv == '':
      localmax = self.maxv
    if not self.maxltv == '':
      localmax = self.maxltv
    if localmax:
      if rval > localmax:
        return False
    if localmin:
      if rval < localmin:
        return False
    return True
      
    
 
  
class FieldInt(FieldAbstract) :
    def __init__(self,parent,fieldname,default,notes,minv,maxv,mingtv,maxltv) :
      FieldAbstract.__init__(self,parent,fieldname,default,notes)
      self.minv = minv
      self.maxv = maxv
      self.mingtv = mingtv
      self.maxltv = maxltv

    def CreateEditor(self) : 
      self.fieldeditor = QtGui.QIntSpinBox()
      if self.minv:
        self.fieldeditor.setMinimum(self.minv)
      elif self.mingtv:
        self.fieldeditor.setMinimum(self.mingtv)
      if self.maxv:
        self.fieldeditor.setMaximum(self.maxv)
      elif self.maxltv:
        self.fieldeditor.setMaximum(self.maxltv)
      self.setTooltip(self.notes)
      if not self.default:
        self.fieldeditor.setValue(self.default)
      return self.fieldeditor
                  
                    
    def getEditorValue(self) :
      return self.fieldeditor.Value()

    def Validate(self,val):
      localmin = False
      localmax = False
      try:
        rval = val.real
      except:
        return False
            
      if not self.minv == '':
        localmin = self.minv
      if not self.mingtv == '':
        localmin = self.mingtv
      if not self.maxv == '':
        localmax = self.maxv
      if not self.maxltv == '':
        localmax = self.maxltv
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

  def createEditor(self) :
    self.fieldeditor = QtGui.QLineEdit()
    if default:
      self.fieldeditor.setText(default)
    self.setToolTips(notes)
    return self.fieldeditor


  def getEditorValue(self) :
    return self.fieldeditor.getText()
      



class FieldChoice(FieldAbstract)  :
  def __init__(self,parent,fieldname,default,notes,choices):
    FieldAbstract.__init__(self,parent,fieldname,default,notes)
    self.choices = choices

  def CreateEditor(self)  :
    self.fieldeditor = QtGui.QComboBox()
    self.fieldeditor.addItems(self.choices)
    self.fieldeditor.setCurrentIndex(choices.index(self.default))
    self.setToolTips(self.notes)
    return self.fieldeditor

  def setEditorValue(self,value,restoflist):
    self.fieldeditor.setCurrentIndex(self.choices.index(value))
  
  def getEditorValue(self):
    return self.fieldeditor.currentText()


class FieldOnOff(FieldAbstract) :
  def __init__(self,parent,fieldname,default,notes) :
    FieldAbstract.__init__(parent,fieldname,default,notes)

  def CreateEditor(self)  :
    self.fieldeditor = QtGui.QCheckBox(self.fieldname)
    if default :
      self.fieldeditor.setCheckedState(2)
    else:
      self.fieldeditor.setCheckedState(QtGui.Qt.Unchecked)
    self.setToolTips(notes)
    return self.fieldeditor

  def setEditorValue(self,value,restoflist) :
    if value:
      self.fieldeditor.setChecked(1)
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

  def setEditorValue(self,value,restoflist):
    self.fieldeditor.setCurrentIndex(self.choices.index(value))
  
  def getEditorValue(self):
    return self.fieldeditor.currentText()

  def getFieldDepends(self):
    return self.objectlistname
    
    
class FieldVertice(FieldAbstract):
  def __init__(self,parent,fieldname,default,notes) :
    FieldAbstract.__init__(self,parent,fieldname,default,notes)

  def CreateEditor(self):
    pass





