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


class Project():
  def __init__(self,projectname):
    if projectname == '':
      self.createNewProject()
    else:
      self.openProject(projectname)

  def createNewProject(self):
    wiz = projectwizard.projectwizard()
    if wiz.exec_():
      print 'finished wizard'
      results = wiz.getData()
      print results
      self.createOutlineArray(results['Dimensions'],results['Shape'])
      


  def getOutlineArray(self):
    return self.outlinearray

  def openProject(self,name):
    pass


  def saveProject(self):
    pass

  def createOutlineArray(data,shape):
    self.outlinearray = []
    if shape == 'L':
      pass
    if shape == 'L90':
      self.outlinearray.append([0,0])
      self.outlinearray.append([data[0],0])
      self.outlinearray.append([0,data[1]-data[3]])
      self.outlinearray.append([data[2]-data[0],0])
      self.outlinearray.append([0,data[1]])
      self.outlinearray.append([-data[2],0])
      self.outlinearray.append([0,data[3]])
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
    
    