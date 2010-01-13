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

from PyQt4 import QtGui
import idfglobals
import pdb
from gwidgetclass import *
from verticewidget import *
import conversion


class FieldAbstract :
    def __init__(self,parent,fieldname,default,notes,units):
        self.fieldeditor = 0
        self.fieldname = fieldname
        self.parent = parent
        self.value = None
        self.default = default
        self.notes = notes
        self.units = units
        self.required = False
        

    def createEditor(self,parent,index):
        pass

    def getEditorValue(self,editor) :
        return editor.Value()

    def setEditorValue(self,editor,data):
        editor.setValue(data)
    
    def getNotes(self) :
        return '\n'.join(self.notes)

    def setValue(self, value,convert=False) :
        #pdb.set_trace()
        if self.Validate(value) :
            self.value = self.valueTweak(value,convert)
            if self.fieldname == 'Name':
                self.parent.setName(self.value)
            return True
        else:
            print 'erroneous data in ' + self.fieldname
            return False

    def valueTweak(self,value,convert=False):
        return value

    def getValue(self,convert=False):
        if convert and conversion.convertable(self.value):
#            print 'convert', self.value,convert
            r = conversion.convertTo(self.units,self.value)
            return r[1]
        else:
            return self.value

    def __str__(self):
        return str(self.value)

    def getUnits(self,convert=False):
        if convert:
            r = conversion.convertTo(self.units,1)
            return r[0]
        else:
            return self.units

    def getFieldDepends(self):
        return ''

    def Validate(self,val) :
        return True
    
    def getFieldName(self):
        return self.fieldname

    def setRequired(self):
        self.required = True
        

class FieldReal(FieldAbstract) :
    def __init__(self,parent,fieldname,default,notes,units,minv,maxv,mingtv,maxltv) :
        FieldAbstract.__init__(self,parent,fieldname,default,notes,units)
        if minv == '':
            self.minv = -20000
        else:
            self.minv = minv
        if maxv == '':
            self.maxv = 1000000000000
        else:
            self.maxv = maxv
        self.mingtv = mingtv
        self.maxltv = maxltv
        
    def createEditor(self,parent,index)  :
        self.fieldeditor = QtGui.QDoubleSpinBox(parent)
        self.fieldeditor.setDecimals(4)
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
        return self.fieldeditor

    def getEditorValue(self,editor) :
        print 'getEditorValue FieldReal',editor
        if editor.cleanText() == '':
            return None
        else:
            return editor.value()

    def setEditorValue(self,editor,data):
        if data != None:
            editor.setValue(data)
        #try:
            #v = float(self.value)
        #except:
            #try:
                #v = int(self.value)
                #v = float(v)
            #except:
                #if self.value == None:
                    #vtxt = 'None'
                #else:
                    #vtxt = self.value
                #print 'setEditorValue float conversion failed ' + self.fieldname + ' ' +vtxt
                #v = float(self.default)
        #editor.setValue(v)
    

    def Validate(self,val):
        #pdb.set_trace()
        if val == None:
            return True
            
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
                print rval,localmax
                return False
        if localmin:
            if rval < localmin:
                print rval,localmin
                return False
        return True
            
    def valueTweak(self,value,convert=False):
        try:
            l = float(value)
        except:
            return value
            
        if convert:
            res = conversion.convertFrom(self.units,l)
            return res[1]
        else:
            return l
        
class FieldRealAutocalculate(FieldReal) :

    def Validate(self,val):
        if val == None:
            return True
        v = str(val).lower()
        if v == 'autocalculate' or v == 'autosize' :
            return True
        else:
            return FieldReal.Validate(self,val)

    def createEditor(self,parent,index)  :
        self.fieldeditor = GAutoCalcRealWidget(parent)
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
        return self.fieldeditor

    def setEditorValue(self,editor,data):
        editor.setValue(data)

    def getEditorValue(self,editor) :
        return editor.value()

    def valueTweak(self,value,convert=False):
        try:
            l = float(value)
        except:
            return value
            
        if convert:
            res = conversion.convertFrom(self.units,l)
            return res[1]
        else:
            return l
       
    
class FieldInt(FieldAbstract) :
    def __init__(self,parent,fieldname,default,notes,units,minv,maxv,mingtv,maxltv) :
        FieldAbstract.__init__(self,parent,fieldname,default,notes,units)
        if minv == '':
            self.minv = -20000
        else:
            self.minv = minv
        if maxv == '':
            self.maxv = 100000000
        else:
            self.maxv = maxv
        self.mingtv = mingtv
        self.maxltv = maxltv

    def createEditor(self,parent,index) :
        self.fieldeditor = QtGui.QSpinBox(parent)
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
        return self.fieldeditor


    def getEditorValue(self,editor) :
        return editor.value()

    def setEditorValue(self,editor,data):
        editor.setValue(data)
        #try:
            #v = int(self.value)
        #except:
            #try:
                #v = float(self.value)
                #v = int(v)
            #except:
                #print 'value wront for int'
        #editor.setValue(v)


    def Validate(self,val):
        if val == None:
            return True
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

    def valueTweak(self,value,convert=False):
        try:
            l = int(value)
        except:
            return value
            
        if convert:
            res = conversion.convertFrom(self.units,l)
            return res[1]
        else:
            return l
       
        
class FieldText(FieldAbstract) :
    def __init__(self,parent,fieldname,default,notes,units):
        FieldAbstract.__init__(self,parent,fieldname,default,notes,units)
        self.value = default

    def createEditor(self,parent,index) :
        self.fieldeditor = QtGui.QLineEdit(parent)
        if self.default:
            self.fieldeditor.setText(self.default)
        return self.fieldeditor


    def getEditorValue(self,editor) :
        return editor.text()

    def setEditorValue(self,editor,data):
        editor.setText(data)
            
class FieldTime(FieldText):

    def createEditor(self,parent,index):
        self.fieldeditor = QtGui.QLineEdit(parent)
        rx = QtCore.QRegExp('[0-9]{2}:[0-6]{2}')
        self.fieldeditor.setValidator(QtGui.QRegExpValidator(rx,self.fieldeditor))
        if self.default:
            self.fieldeditor.setText(self.default)
        return self.fieldeditor
            

class FieldChoice(FieldAbstract)    :
    def __init__(self,parent,fieldname,default,notes,units,choices):
        FieldAbstract.__init__(self,parent,fieldname,default,notes,units)
        self.choices = choices
        self.lchoices = []
        for lc in self.choices:
            self.lchoices.append(lc.lower())

    def createEditor(self,parent,index)  :
        self.fieldeditor = QtGui.QComboBox(parent)
        self.fieldeditor.addItems(self.choices)
        if self.default in self.choices:
            index = self.lchoices.index(self.default.lower())
            self.fieldeditor.setCurrentIndex(index)
        else:
            if not self.default == '':
                print self.default + 'no default in choices'
                
        return self.fieldeditor

    def setEditorValue(self,editor,data):
        if not ((data == '') or (data == None)):
            editor.setCurrentIndex(self.lchoices.index(str(data).lower()))
    
    def getEditorValue(self,editor):
        return str(editor.currentText())


class FieldOnOff(FieldChoice) :
    def __init__(self,parent,fieldname,default,notes,units,choices) :
        FieldChoice.__init__(self,parent,fieldname,default,notes,units,choices)


class FieldYesNo(FieldChoice):
    def __init__(self,parent,fieldname,default,notes,units,choices) :
        FieldChoice.__init__(self,parent,fieldname,default,notes,units,choices)

                        

class FieldObjectlist(FieldAbstract):
    def __init__(self,parent,fieldname,default,notes,units,objectlistname) :
        FieldAbstract.__init__(self,parent,fieldname,default,notes,units)
        self.objectlistname = objectlistname

    def createEditor(self,parent,index) :
        self.fieldeditor = QtGui.QComboBox(parent)
        try:
            self.choices = index.model().parentmodel.idfsource.getDepends(self.objectlistname)
        except:
            self.choices = []
        self.fieldeditor.addItem("None")
        self.fieldeditor.addItems(self.choices)
        return self.fieldeditor

    def setEditorValue(self,editor,data):
        try:
            editor.setCurrentIndex(self.choices.index(data) + 1)
        except:
            editor.setCurrentIndex(0)
    
    def getEditorValue(self,editor):
        return editor.currentText()

    def getFieldDepends(self):
        return self.objectlistname
        
         
#class FieldVertice(FieldAbstract):
    #def __init__(self,parent,fieldname,default,notes) :
        #FieldAbstract.__init__(self,parent,fieldname,default,notes)

    #def createEditor(self,parent):
        #self.fieldeditor = GVerticeWidget('')
        #return self.fieldeditor

    #def setEditorValue(self,editor):
        #val = []
        #val.append(self.value)
        #val.append(self.restoflist)
        #editor.setValue(val)

##  def setValue(self,value,restoflist):
##        print value
##        print restoflist
##        self.value = value
##        self.restoflist = restoflist
##        return True

#class FieldCompactSchedule(FieldAbstract):
    #def __init__(self,parent,fieldname,default,notes):
        #FieldAbstract.__init__(self,parent,fieldname,default,notes)
        #self.widgetlist = []

    #def createEditor(self,parent):
        #self.fieldeditor = GCompactScheduleWidget(self.fieldname)
        #return self.fieldeditor


    #def setEditorValue(self,editor):
        ##array of values
        #v = []
        #v.append(self.value)
        #v = v + self.restoflist
        #editor.setValue(v)

class FieldThrough(FieldAbstract):
    def __init__(self,parent,fieldname,default,notes,units):
        FieldAbstract.__init__(self,parent,fieldname,default,notes,units)

    def createEditor(self,parent,index):
        self.fieldeditor = QtGui.QLineEdit(parent)
        return self.fieldeditor

    def setValue(self,value):
        s = value.split(':')
        if len(s) == 2:
            self.value = s[1]
        else:
            self.value = value

    def setEditorValue(self,editor,data):
        editor.setText(data)

    def getEditorValue(self,editor):
        return editor.text()

        