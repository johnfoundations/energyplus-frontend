# -*- coding: utf-8 -*-


from gwidgetclass import *

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
    self.forwidget = GForWidget()
    self.vlayout = QtGui.QVBoxLayout(self)
    self.vlayout.addWidget(self.forwidget)
    
        
        


class GForWidget(QtGui.QWidget):
  def __init__(self,parent=None) :
    QtGui.QWidget.__init__(self,parent)
    self.vlayout = QtGui.QVBoxLayout(self)
    self.fordatalist = [' ','AllDays','Weekdays','Weekends','Sunday','Monday','Tuesday','Wednesday','Thursday','Friday','Saturday','Holiday',\
                        'SummerDesignDay','WinterDesignDay','AllOtherDays']
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
    self.insertUntil()
    
    

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

  def insertUntil(self):
    self.vlayout.addWidget(GTimeWidget('Until:'))
    if not self.lastuntilwidget == None:
      print self.lastuntilwidget
      self.disconnect(self.lastuntilwidget,QtCore.SIGNAL('editingFinished ()'),self.untilEdit)
    self.lastuntilwidget = QtGui.QLineEdit()
    self.connect(self.lastuntilwidget,QtCore.SIGNAL('editingFinished ()'),self.untilEdit)
    self.vlayout.addWidget(self.lastuntilwidget)
    

  def untilEdit(self):
    s = self.lastuntilwidget.text()
    if not s == '':
      self.insertUntil()
  

  def forChanged(self,i):
    s = self.forcombolist[i].currentText()
    print s
    if i == len(self.forcombolist)-1:
      #last
      w = QtGui.QComboBox()
      self.forcombolist.append(w)
      self.insertFor(w,i+1)
        
  



if __name__ == "__main__":
  app = QtGui.QApplication(sys.argv)
  view = GCompactScheduleWidget('Test')
  view.setWindowTitle("Widget test")
  view.show()
  sys.exit(app.exec_())
  
    