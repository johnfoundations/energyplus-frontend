# -*- coding: utf-8 -*-
"""************************************************************************
*   Copyright (C) 2009 by Derek Kite                                      *
*   dkite@shaw.ca                                                         *
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



import idfglobals

import copy
from PyQt4 import QtGui, QtCore
from fieldclasses import *


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
        self.scrollarea = None
        self.memo = []
        self.CreateFields()
        self.createExtensibleList()
        
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

    def fieldCount(self):
        return len(self.fieldlist)
    
    def setData(self,data):
        self.rawdatalist = data
        self.ParseRawData()

    def getData(self) :
        print self.getClassnameIDD() + ' getData not implemented'

    def getFieldData(self,index):
        try:
            return self.fieldlist[index].getValue()
        except:
            print "getFieldData error"
            return None
        
    def CreateEditWidget(self) :
        self.editwidget = QtGui.QWidget()
        vlayout = QtGui.QVBoxLayout(self.editwidget)
#        hlayout = QtGui.QVBoxLayout()
        label = QtGui.QLabel(self.getClassnameIDD())
        ms = ''
        for m in self.memo:
            ms = ms + m + '\n'
        ms = ms.strip()
        label.setToolTip(ms)
        vlayout.addWidget(label)
        count = 0
        for f in self.fieldlist:
            count = count + 1
            vlayout.addWidget(f.CreateEditor())
            f.setEditorValue()
            if count > 2:
                count = 0
#            vlayout.addStretch()
#            hlayout.addLayout(vlayout)
#            vlayout = QtGui.QVBoxLayout()
#            vlayout.addStretch()
#            hlayout.addLayout(vlayout)
        vlayout.addStretch()
        self.scrollarea = QtGui.QScrollArea()
        self.scrollarea.setWidget(self.editwidget)
        self.scrollarea.setWidgetResizable(True)
        return self.scrollarea

    def closeWidget(self):
        if self.scrollarea :
            self.scrollarea.close()

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

    def __str__(self):            
        lines = []
        lines.append(self.getClassnameIDD() + ',')
        tmplines = []
        for c, field in enumerate(self.fieldlist):
            if c > self.minfields and field.value == '':
                tmplines.append('    , !- %s' % field.fieldname)
            else:
                lines.extend(tmplines)
                tmplines = []
                lines.append('    %s, ! %s' % (field, field.fieldname))
#                if field.restoflist:
#                    print 'restoflist', field.fieldname, len(field.restoflist)
        if self.extensible and field.restoflist:
            newlines = []
            for i in range(0, len(field.restoflist), self.extensible):
                line = ''
                for idx in range(self.extensible):
                    line += str(field.restoflist[i+idx]) + ','
                newlines.append(line)
            try:
                newlines[-1] = newlines[-1][:-1] + ';'
                lines.extend(newlines)
            except IndexError:
                pass
        else:
            lines[-1] = lines[-1].replace(',', ';',1)
        return '\n'.join(lines) + '\n'
            
#        for c, field in enumerate(self.fieldlist):
#            if c < len(self.fieldlist)-1 :
#                sep = ','
#            else:
#                sep= ';'
#            s += '    %s%s ! %s\n' % (str(field), sep, field.fieldname)
        return s


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

    def empty_copy(self,object):
        class Empty: pass
        newcopy = Empty()
        newcopy.__class__ = object.__class__
        return newcopy

    def copyField(self,orig) :
        fcopy = copy.copy(orig)
        fcopy.fieldname = orig.fieldname
        fcopy.parent = orig.parent
        fcopy.default = orig.default
        fcopy.notes = orig.notes
        return fcopy

    def createExtensibleList(self):
        if self.extensible == -1:
            return
        print 'createExtensibleList ----------------'
        self.extensiblefieldlist = []
        a = self.extensible * -1
        print str(a) + 'extensible*-1'
        tlist = self.fieldlist[a:len(self.fieldlist)]
        for i in tlist:
            print i.fieldname
            fieldcopy = self.copyField(i)
            self.extensiblefieldlist.append(fieldcopy)

        self.extensibletag = 1
        print "createExtensibleList" + " " + str(len(self.extensiblefieldlist))
            
    def createExtensibleFields(self):
        print 'createExtensibleFields'
        self.extensibletag = self.extensibletag + 1
        for i in self.extensiblefieldlist:
            newfield = self.copyField(i)
            newfield.fieldname = i.fieldname.replace('1',str(self.extensibletag))
            self.fieldlist.append(newfield)
            print newfield.fieldname



    def getDepends(self):
        dependslist = []
        for f in self.fieldlist :
            if f.getFieldDepends():
                dependslist.append(f.getFieldDepends())
        return dependslist

    def getObjectDepend(self):
        for f in self.fieldlist:
            if f.getFieldDepends() :
                if f.getFieldName() == 'Zone Name':
                    return f.getValue()
            

    def ParseRawData(self) :
        print "len fieldlist"  + str(len(self.fieldlist)) + self.getClassnameIDD()
        for i,fd in enumerate(self.rawdatalist) :
            if i == 0:  #first item is classname
                continue

            if i > len(self.fieldlist) :
                if self.extensible == -1 :
#                    pdb.set_trace()
                    print 'ran out of fieldlists ' + self.getClassnameIDD()
                    return
                else :
                    self.createExtensibleFields()

            print i
            if not self.fieldlist[i-1].setValue(fd):
                print 'parserawdata setvalue false ' + fd + ' ' + self.getClassnameIDD()
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
    def __init__(self):
        ObjectAbstract.__init__(self)
        f = self.fieldlist.pop()
        del f
        self.InsertField(FieldCompactSchedule(self,"Schedule","",""))
        

class ObjectSpectral(ObjectAbstract) :
    pass
    
        
            

                
    
