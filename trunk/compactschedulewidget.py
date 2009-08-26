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


from  PyQt4 import QtGui,QtCore
import re
#import pdb
import sys
from fieldclasses import *

    #rules:
      #Through: 12/31 means only one through field
      #otherwise repeat
      #For:
        #if selection is AllDays, then just one
        #if otherwise, insert a second one for selecting
        #if selection AllOtherDays, then it's over
        #Interpolate: yes,no
        #Time: hh:mm
        #followed by
        #Numeric value based on limit name type of data, including range
        #if time is 24:00
        #numeric value, then done



class compactScheduleHandler():
    def __init__(self,parent,fieldlist) :
        self.throughlist = []
        self.flist = fieldlist
        self.parent = parent
        self.model = None
        self.throughlist.append(throughSection(parent,self.flist))
        

    
    def setValue(self,value):
        
        #print value
        throughdata = []
        for v in value:
            v = v.strip()
            res = re.match(r"^Through:(.*)",v)
            if res:
                if len(throughdata) == 0:
                    throughdata.append(v)
                    continue

                else:
                    self.throughlist[-1].setValue(throughdata)
                    throughdata = []
                    throughdata.append(v)
                    self.throughlist.append(throughSection(self.parent,self.flist))
                    continue

            throughdata.append(v)

        self.throughlist[-1].setValue(throughdata)
        self.throughlist.append(throughSection(self.parent,self.flist))

    def setModel(self,model):
        if not self.model == model:
            self.model = model
            for t in self.throughlist:
                t.setModel(model)


class throughSection():
    def __init__(self,parent,fieldlist):
        self.flist = fieldlist
        self.forlist = []
        self.parent = parent
        self.model = None
        self.throughfield = FieldThrough(self,'Through:','','')
        self.insertField([self.throughfield],len(self.flist))
  #      


    def insertField(self,fields,index):
        if self.model:
            self.model.beginInsertRows(QtCore.QModelIndex(),index,index+len(fields))
        for c,f in enumerate(fields):
            self.flist.insert(index+c,f)
        if self.model:
            self.model.endInsertRows()


    def setValue(self,value):
       
        #value is an array of for, until and data lines
        #print value
        index = 0
        ds = []
        self.throughfield.setValue(value[0])
        for i in value:
            if index == 0:
                index = 1
                continue

            #pdb.set_trace()
            i = i.strip()
            res = re.match(r"^For:(.*)",i)
            if res:
                t = res.group(1)
                #pdb.set_trace()
                ta = t.split()
                if len(ds) == 0:
                    ds.append('For:')
                    ds = ds + ta
                    #print ds
                    continue

                else:
                    fsec = ForSection(self,self.flist,self.model)
                    fsec.setValue(ds)
                    self.forlist.append(fsec)
                    ds = []
                    ds.append('For:')
                    ds = ds + ta
                    continue
                    #print ds

            ds.append(i)

        fsec = ForSection(self,self.flist,self.model)
        fsec.setValue(ds)
        self.forlist.append(fsec)

    def setModel(self,model):
        self.model = model
        for f in self.forlist:
            f.setModel(model)

    def throughEdit(self,row):
        if len(self.forlist) == 0:
            self.forlist.append(ForSection(self,self.flist,self.model))
            self.forlist[-1].insertUntil(['',''])


class ForSection():
    def __init__(self,parent,fieldlist,model) :
        self.parent = parent
        self.model = model
        self.flist = fieldlist
        self.fordatalist = ['','AllDays','Weekdays','Weekends','Sunday','Monday','Tuesday','Wednesday','Thursday','Friday','Saturday','Holidays',\
                            'SummerDesignDay','WinterDesignDay','AllOtherDays']
        self.lfordatalist =[]
        for fd in self.fordatalist:
            self.lfordatalist.append(fd.lower())

        self.fdlist = self.fordatalist[:]
        self.forfieldlist = []
        self.insertFor(FieldChoice(self,'For:','','',self.fordatalist))
        self.lastuntilfieldinstance = None
        if self.model:
            self.model.beginInsertRows(QtCore.QModelIndex(),self.lastForField()+1,self.lastForField()+1)
        self.interpolatefield = FieldYesNo(self,'Interpolate:','','',['No','Yes'])
        self.flist.append(self.interpolatefield)
        if self.model:
            self.model.endInsertRows()
        


    
    def forEdit(self,row):
        if row == self.lastForField() -1 and not self.flist[self.lastForField()-1].value == '':
            self.insertFor(FieldChoice(self,'For:','','',self.fordatalist))

    def untilEdit(self,row):
        if row == self.lastUntilField() -1 and not self.flist[self.lastUntilField()-1].value == '':
            self.insertUntil(['',''])

    def lastForField(self):
        if len(self.forfieldlist) > 0:
            return self.flist.index(self.forfieldlist[-1]) + 1
        else:
            if len(self.parent.forlist) > 0:
                return self.parent.forlist[-1].lastUntilField() + 1
            else:
                return self.flist.index(self.parent.throughfield) + 1

            

    def lastUntilField(self):
        if self.lastuntilfieldinstance == None:
            return self.flist.index(self.interpolatefield) + 1
        else:
            return self.flist.index(self.lastuntilfieldinstance) + 1


    def insertFor(self,field) :
        if self.model:
            self.model.beginInsertRows(QtCore.QModelIndex(),self.lastForField(),self.lastForField())

        self.flist.insert(self.lastForField(),field)
        self.forfieldlist.append(field)
        if self.model:
            self.model.endInsertRows()

    def insertUntil(self,vals):
        #print vals
        if len(vals) < 2:
            vals = ['','']
        if self.model:
            self.model.beginInsertRows(QtCore.QModelIndex(),self.lastUntilField(),self.lastUntilField()+1)

        f = FieldTime(self,'Until:','','')
        t = vals[0].lstrip('Until:')
        f.setValue(t)
        self.flist.insert(self.lastUntilField(),f)
        d = FieldText(self,'Data:','','')
        d.setValue(vals[1])
        self.flist.insert(self.lastUntilField() + 1,d)
        self.lastuntilfieldinstance = d
        if self.model:
            self.model.endInsertRows()

        
    def setValue(self,v):
        #print v
        self.lock = True
        fori = False
        untilar = []
        for l in v:
            print l
            if not l.find('For:') == -1 :
                #pdb.set_trace()
                fori = True
                first = True
                continue

            if not l.find('Until:') == -1:
                fori = False
                if len(untilar) > 0:
                    self.insertUntil(untilar)
                    untilar= []
                    ll = l.split(':')
                    untilar.append(ll[1]+':'+ll[2])
                    continue

            if fori:
                try:
                    index = self.lfordatalist.index(l.lower())
                except:
                    index = 0

                if not first:
                    self.insertFor(FieldChoice(self,'For:','','',self.fordatalist))
                else:
                    first = False
                self.forfieldlist[-1].setValue(self.fordatalist[index])
                continue

            else:
                untilar.append(l)

        self.insertUntil(untilar)

    def setModel(self,model):
        self.model = model
        
      
       
  



if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    view = GCompactScheduleWidget('Test')
    schedarray = ["Through: 12/31",\
    "For: Weekdays Weekends SummerDesignDay",\
    "Until: 05:00",\
    "0.05",\
    "Until: 07:00",\
    "0.1",\
    "Until: 08:00",\
    "0.3",\
    "Until: 17:00",\
    "0.9",\
    "Until: 18:00",\
    "0.5",\
    "Until: 20:00",\
    "0.3",\
    "Until: 22:00",\
    "0.2",\
    "Until: 23:00",\
    "0.1",\
    "Until: 24:00",\
    "0.05",\
    "For: SummerDesignDay",\
    "Until: 24:00",\
    "1.0",\
    "For: Saturday",\
    "Until: 06:00",\
    "0.05",\
    "Until: 08:00",\
    "0.1",\
    "Until: 12:00",\
    "0.3",\
    "Until: 17:00",\
    "0.15",\
    "Until: 24:00",\
    "0.05",\
    "For: WinterDesignDay",\
    "Until: 24:00",\
    "0.0",\
    "For: Sunday Holidays AllOtherDays",\
    "Until: 24:00",\
    "0.05"]
    view.setValue(schedarray)
    view.setWindowTitle("Widget test")
    view.show()
    sys.exit(app.exec_())


