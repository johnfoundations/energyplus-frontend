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



class throughSection():
    def __init__(self,parent,fieldlist):
        self.flist = fieldlist
        self.forlist = []
        self.parent = parent
        self.throughfield = FieldThrough('','Through:','','')
        self.flist.append(self.throughfield)
        self.forlist.append(ForSection(parent,self.flist))
        print self.flist


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
                    self.forlist[-1].setValue(ds)
                    self.forlist.append(ForSection(self.parent,self.flist))
                    ds = []
                    ds.append('For:')
                    ds = ds + ta
                    continue
                    #print ds

            ds.append(i)

        self.forlist[-1].setValue(ds)




class ForSection():
    def __init__(self,parent,fieldlist) :
        self.parent = parent
        self.flist = fieldlist
        self.fordatalist = [' ','AllDays','Weekdays','Weekends','Sunday','Monday','Tuesday','Wednesday','Thursday','Friday','Saturday','Holiday',\
                            'SummerDesignDay','WinterDesignDay','AllOtherDays']
        self.lfordatalist =[]
        self.lastuntilfield = len(self.flist)
        for fd in self.fordatalist:
            self.lfordatalist.append(fd.lower())

        self.fdlist = self.fordatalist[:]
        self.forfieldlist = []
        self.forfieldlist.append(FieldChoice('','For:','','',self.fordatalist))
        self.lastforfield = len(self.flist)
        self.populateForCombo()
        
        self.interpolatefield = FieldYesNo('','Interpolate:','','',['No','Yes'])
        self.flist.append(self.interpolatefield)
        self.lastuntilfield = len(self.flist)
        self.lock = False
    
    

    def populateForCombo(self):
        for i in self.forfieldlist:
            self.insertFor(i)
      
    def insertFor(self,field) :
        self.flist.insert(self.lastforfield,field)
        self.lastforfield = self.lastforfield + 1
        self.lastuntilfield = self.lastuntilfield + 1

    def insertUntil(self,vals):
        #print vals
        if len(vals) < 2:
            vals = ['','']

        f = FieldTime(self,'Until:','','')
        t = vals[0].lstrip('Until:')
        f.setValue(t)
        self.flist.insert(self.lastuntilfield,f)
        self.lastuntilfield = self.lastuntilfield + 1
        d = FieldText(self,'Data:','','')
        d.setValue(vals[1])
        self.flist.insert(self.lastuntilfield,d)
        self.lastuntilfield = self.lastuntilfield + 1

    def untilEdit(self):
        s = self.lastuntilwidget.text()
        if not s == '':
            self.insertUntil(['',''])
  

    def forChanged(self,i):
        if self.lock:
            return

        s = self.forcombolist[i].currentText()
        #print s
        if i == len(self.forcombolist)-1:
            #last
            w = QtGui.QComboBox()
            self.forcombolist.append(w)
            self.insertFor(w,i+1)
        
    def setValue(self,v):
        #pdb.set_trace()
        #print v
        self.lock = True
        fori = False
        untilar = []
        for l in v:
            #print l
            if not l.find('For:') == -1 :
                #pdb.set_trace()
                fori = True
                continue

            if not l.find('Until:') == -1:
                if len(untilar) > 0:
                    self.insertUntil(untilar)
                    untilar= []
                    ll = l.split(':')
                    untilar.append(ll[1]+':'+ll[2])
                    fori = False
                    continue

            if fori:
                try:
                    index = self.lfordatalist.index(l.lower())
                except:
                    index = 0

                self.forfieldlist[-1].setValue(self.fordatalist[index])
                #print self.forcombolist
                w = FieldChoice('','For:','','',self.fordatalist)
                self.forfieldlist.append(w)
                self.insertFor(w)
                fori = False

            else:
                untilar.append(l)

        self.insertUntil(untilar)
        self.lock = False

      
      
       
  



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


