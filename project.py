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

import projectwizard
from PyQt4 import QtGui, QtCore

class Project():
  def __init__(self):
    self.projectdir = '~/EPProjects'
    self.results = dict()


  def openProject(self,projectname):
    if projectname == '':
      self.createNewProject()
    else:
      self.openProject(projectname)

  def createNewProject(self):
    wiz = projectwizard.projectwizard()
    res = wiz.exec_()
    print res
    if res == 1:
      print 'finished wizard'
      self.results = wiz.getData()
      print self.results
      self.createOutlineArray(self.results['Dimensions'],self.results['Shape'])
      

    if res == 2:
      print 'open project'
      fd= QtGui.QFileDialog()
      if fd.exec_():
        print fd.selectedFiles()
        

    if res == 3:
      fd= QtGui.QFileDialog()
      if fd.exec_():
        print fd.selectedFiles()


  def getOutlineArray(self):
    return self.outlinearray

  def getProjectDetails(self):
    print self.results
    res = dict()
    if 'Details' in self.results:
      res['Details'] = self.results['Details']
    else:
      res['Details'] = ''
    if 'Units' in self.results:
      res['Units']   = self.results['Units']
    else:
      res['Units'] = ''
    if 'Name' in self.results:
      res['Name']    = self.results['Name']
    else:
      res['Name'] = ''
    return res

  def openProject(self,name):
    pass


  def saveProject(self):
    pass

  def createOutlineArray(self,data,shape):
    self.outlinearray = []
    print data
    if len(data) < 4:
      return
    ndata = []
    for d in data:
      if d == '_':
        return
      try:
        t = float(d)
      except:
        try:
          t = int(d)
          t = float(t)
        except:
          return
      ndata.append(t)
                
    if shape == 'L':
      pass
    if shape == 'L90':
      self.outlinearray.append([0,0])
      self.outlinearray.append([ndata[0],0])
      self.outlinearray.append([0,ndata[1]-ndata[3]])
      self.outlinearray.append([ndata[2]-ndata[0],0])
      self.outlinearray.append([0,-ndata[1]])
      self.outlinearray.append([-ndata[2],0])
      self.outlinearray.append([0,ndata[3]])
      return
        
    if shape == 'L180':
      pass
    if shape == 'L270':
      pass
    if shape == 'H':
      pass
    if shape == 'H90':
      pass
    if shape == 'T':
      pass
    if shape == 'T90':
      pass
    if shape == 'T180':
      pass
    if shape == 'T270':
      pass
    if shape == 'U':
      pass
    if shape == 'U90':
      pass
    if shape == 'U180':
      pass
    if shape == 'U270':
      pass
    
    