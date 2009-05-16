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


from gwidgetclass import *
import re
import pdb

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


class GCompactScheduleWidget(QtGui.QWidget):
  def __init__(self,label,parent=None) :
    QtGui.QWidget.__init__(self,parent)
    self.throughwidgetlist = []
    self.throughwidgetlist.append(GThroughWidget())
    self.vlayout = QtGui.QVBoxLayout(self)
    self.vlayout.addWidget(self.throughwidgetlist[0])

    
  def setValue(self,value):
    #print value
    throughdata = []
    for v in value:
      v = v.strip()
      res = re.match(r"^Through:(.*)",v)
      if res:
        t = res.group(1)
        if len(throughdata) == 0:
          throughdata.append(t)
          continue
        else:
          self.throughwidgetlist[-1].setValue(throughdata)
          throughdata = []
          throughdata.append(t)
          self.throughwidgetlist.append(GThroughWidget())
          self.vlayout.addWidget(self.throughwidgetlist[-1])
          continue
      throughdata.append(v)
    self.throughwidgetlist[-1].setValue(throughdata)
    self.throughwidgetlist.append(GThroughWidget())
    self.vlayout.addWidget(self.throughwidgetlist[-1])



class GThroughWidget(QtGui.QWidget):
  def __init__(self,parent=None):
    QtGui.QWidget.__init__(self,parent)
    self.vlayout = QtGui.QVBoxLayout(self)
    self.throughedit = GEditWidget('Through')
    self.vlayout.addWidget(self.throughedit)
    self.forwidgetlist = []
    self.forwidgetlist.append(GForWidget())
    self.vlayout.addWidget(self.forwidgetlist[0])

  def setValue(self,value):
    #value is an array of for, until and data lines
    print value
    widgetindex = 0
    ds = []
    self.throughedit.setValue(value[0])
    for i in value:
      if widgetindex == 0:
        widgetindex = 1
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
          self.forwidgetlist[-1].setValue(ds)
          self.forwidgetlist.append(GForWidget())
          self.vlayout.addWidget(self.forwidgetlist[-1])
          ds = []
          ds.append('For:')
          ds = ds + ta
          #print ds
      ds.append(i)
    self.forwidgetlist[-1].setValue(ds)




class GForWidget(QtGui.QWidget):
  def __init__(self,parent=None) :
    QtGui.QWidget.__init__(self,parent)
    self.vlayout = QtGui.QVBoxLayout(self)
    self.fordatalist = [' ','AllDays','Weekdays','Weekends','Sunday','Monday','Tuesday','Wednesday','Thursday','Friday','Saturday','Holiday',\
                        'SummerDesignDay','WinterDesignDay','AllOtherDays']
    self.lfordatalist =[]
    for fd in self.fordatalist:
      self.lfordatalist.append(fd.lower())
    self.fdlist = self.fordatalist[:]
    self.forcombolist = []
    self.forcombovlayout = QtGui.QVBoxLayout()
    self.forcombolist.append(QtGui.QComboBox())
    self.vlayout.addLayout(self.forcombovlayout)
    self.interpolatewidget = GComboBox('Interpolate')
    self.interpolatewidget.addItems(['No','Yes'])
    self.vlayout.addWidget(self.interpolatewidget)
    self.signalmapper = QtCore.QSignalMapper(self)
    self.connect(self.signalmapper,QtCore.SIGNAL('mapped(int)'),self.forChanged)
    self.populateForCombo()
    self.lastuntilwidget = None
#    self.insertUntil(['',''])
    self.lock = False
    
    

  def populateForCombo(self):
    for c,i in enumerate(self.forcombolist):
      self.insertFor(i,c)
      
  def insertFor(self,widget,c) :
    widget.addItems(self.fordatalist)
    self.connect(widget, QtCore.SIGNAL('currentIndexChanged ( const QString)'),self.signalmapper, QtCore.SLOT('map()'))
    self.signalmapper.setMapping(widget,c)
    hlayout = QtGui.QHBoxLayout()
    hlayout.addWidget(QtGui.QLabel('For:'))
    hlayout.addWidget(widget)
    self.forcombovlayout.addLayout(hlayout)

  def insertUntil(self,vals):
    #print vals
    if len(vals) < 2:
      vals = ['','']
    tw = GTimeWidget('Until:')
    tw.setValue(vals[0])
    self.vlayout.addWidget(tw)
    if not self.lastuntilwidget == None:
      #print self.lastuntilwidget
      self.disconnect(self.lastuntilwidget,QtCore.SIGNAL('editingFinished ()'),self.untilEdit)
    self.lastuntilwidget = GEditWidget('Data:')
    self.lastuntilwidget.setValue(vals[1])
    self.connect(self.lastuntilwidget,QtCore.SIGNAL('editingFinished ()'),self.untilEdit)
    self.vlayout.addWidget(self.lastuntilwidget)
    

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
    print v
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
        self.forcombolist[-1].setCurrentIndex(index)
        #print self.forcombolist
        w = QtGui.QComboBox()
        self.forcombolist.append(w)
        self.insertFor(w,len(self.forcombolist))
      else:
        untilar.append(l)
    self.insertUntil(untilar)    
    self.lock = False    
      
      
      
       
  



if __name__ == "__main__":
  app = QtGui.QApplication(sys.argv)
  view = GCompactScheduleWidget('Test')
  schedarray = ["For: Weekdays Weekends SummerDesignDay",\
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
  
    
