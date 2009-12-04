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
import compactschedulewidget


#base class for all the defined objects.
#each one is created as a subclass of ObjectAbstract,
#and it's init will create the fields and append them to the field list
class ObjectAbstract :
    def __init__(self):
        self.minfields = 0
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
        self.parseRawData()

        
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
        self.parseRawData()
        #debug
        #for f in self.fieldlist:
        #    if f.units != '':
        #        print f.units,f.getValue()

    def getData(self) :
        d = []
        for f in self.fieldlist:
            d.append(f.getValue())

        return d

    def getDataDict(self):
        d = dict()
        for f in self.fieldlist:
            d[f.getFieldName()] = f.getValue()

        return d

    def getFieldData(self,index):
        try:
            return self.fieldlist[index].getValue()
        except:
            print "getFieldData error"
            return None

    def getFieldDataByName(self,name):
        for f in self.fieldlist:
            if f.getFieldName() == name:
                return f.getValue()

        return None

    def CreateFields(self) :
        print 'to be subclassed'

    def setRequiredFields(self,flist):
        for f in flist:
            self.fieldlist[f].setRequired()

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
            if c >= self.minfields and field.value == None or '':
                tmplines.append('    , !- %s' % field.fieldname)
            else:
                lines.extend(tmplines)
                tmplines = []
                lines.append('    %s, ! %s' % (field, field.fieldname))

        lines[-1] = lines[-1].replace(',', ';',1)
        return '\n'.join(lines) + '\n'
            

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
        return '\n'.join(self.memo)

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
#        print 'copyField'
        fcopy = copy.copy(orig)
#        print 'copyField copy.copy done'
        fcopy.fieldname = orig.fieldname
        fcopy.parent = orig.parent
        fcopy.default = orig.default
        fcopy.notes = orig.notes
        fcopy.units = orig.units
        return fcopy

    def createExtensibleList(self):
        if self.extensible == -1:
            return
#        print 'createExtensibleList ----------------'
        self.extensiblefieldlist = []
        a = self.extensible * -1
#        print str(a) + 'extensible*-1'
        tlist = self.fieldlist[a:len(self.fieldlist)]
        for i in tlist:
#            print i.fieldname
            fieldcopy = self.copyField(i)
            self.extensiblefieldlist.append(fieldcopy)

        self.extensibletag = 1
#        print "createExtensibleList" + " " + str(len(self.extensiblefieldlist))
            
    def createExtensibleFields(self):
#        print 'createExtensibleFields'
        self.extensibletag = self.extensibletag + 1
        for i in self.extensiblefieldlist:
            newfield = self.copyField(i)
            newfield.fieldname = i.fieldname.replace('1',str(self.extensibletag))
            self.fieldlist.append(newfield)
#            print newfield.fieldname

    def editSignal(self,model,row):
        if row == len(self.fieldlist)-1 and self.extensible > -1:
            model.insertRows(model.rowCount(0),self.extensible,QtCore.QModelIndex())


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
            

    def parseRawData(self) :
 #       print "len fieldlist" , len(self.fieldlist) , self.getClassnameIDD()
        if len(self.rawdatalist) != 0:
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

                if not self.fieldlist[i-1].setValue(fd):
                    print 'parserawdata setvalue false ' + fd + ' ' + self.getClassnameIDD()
                    return

#        print 'after enumerate' , len(self.rawdatalist) , self.minfields
        if self.minfields > 0:
            if len(self.rawdatalist) > self.minfields:
                start = len(self.rawdatalist)-1
            else:
                start = self.minfields

#            print self.getClassnameIDD() , self.minfields , len(self.rawdatalist) , len(self.fieldlist) , start
            for c in range(start,len(self.fieldlist)):
                self.fieldlist[c].setValue(None)


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
        self.extensible = -1
        ObjectAbstract.__init__(self)
        self.fieldlist.pop()
        self.schedulehandler = compactschedulewidget.compactScheduleHandler(self,self.fieldlist)
        
    def parseRawData(self) :
        for i,fd in enumerate(self.rawdatalist) :
            if i == 0:  #first item is classname
                continue

            if i == 1:
                self.fieldlist[0].setValue(fd)

            if i == 2:
                self.fieldlist[1].setValue(fd)
                scheduletypelimits = fd

            if i == 3:
                self.schedulehandler.setValue(self.rawdatalist[3:])



    def editSignal(self,model,row):
        field = self.fieldlist[row]
        self.schedulehandler.setModel(model)
        if field.fieldname == 'Through:':
            self.fieldlist[row].parent.throughEdit(row)

        elif field.fieldname == 'For:':
            self.fieldlist[row].parent.forEdit(row)

        elif field.fieldname == 'Data:':
            self.fieldlist[row].parent.untilEdit(row)

    def __str__(self):
        lines = []
        lines.append(self.getClassnameIDD() + ',')
        tmplines = []
        i = 0
        fieldindex = 1
        while i < len(self.fieldlist):
            if self.fieldlist[i].fieldname == 'For:':
                forstr = 'For: '
                while self.fieldlist[i].fieldname == 'For:':
                    forstr = forstr + ' ' + self.fieldlist[i].value
                    i = i+1
                lines.append('    %s, ! %s' % (forstr,'Field '+str(fieldindex) ))
                fieldindex = fieldindex + 1
                continue

            if self.fieldlist[i].fieldname == 'Until:':
                lines.append('    %s, ! %s' % ('Until: '+self.fieldlist[i].value, 'Field '+ str(fieldindex)))
                i = i+1
                fieldindex = fieldindex + 1
                continue
            
            if self.fieldlist[i].fieldname == 'Data:':
                lines.append('    %s, ! %s' % (self.fieldlist[i].value, 'Field '+ str(fieldindex)))
                i = i+1
                fieldindex = fieldindex + 1
                continue
            
            if self.fieldlist[i].fieldname == 'Through:':
                if not self.fieldlist[i].value == '':
                    lines.append('    %s, ! %s' % ('Through: '+self.fieldlist[i].value, 'Field '+ str(fieldindex)))
                    fieldindex = fieldindex + 1
                i = i+1
                continue

            if self.fieldlist[i].fieldname == 'Interpolate:':
                if not self.fieldlist[i].value == '':
                    lines.append('    %s, ! %s' % ('Interpolate: '+self.fieldlist[i].value, 'Field '+ str(fieldindex)))
                    fieldindex = fieldindex + 1
                i=i+1
                continue

                
            lines.append('    %s, ! %s' % (self.fieldlist[i].value, self.fieldlist[i].fieldname))
            i = i+1

        lines[-1] = lines[-1].replace(',', ';',1)
        return '\n'.join(lines) + '\n'
            
     



















class ObjectSpectral(ObjectAbstract) :
    pass
    
        
            

                
    
