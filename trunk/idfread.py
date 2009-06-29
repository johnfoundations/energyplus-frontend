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


import iddclass
import string
import re
import pdb

class idfRead :
  def __init__(self,filename) :
    self.active = []
    self.activetree = []
    self.comment = ''
    self.referencedict = dict()
    self.filename = filename
    
    try:
      self.fh = open(filename, 'r')
    except:
      return
    self.parseFile()
    self.buildDependsTree()

  def getActivelist(self):
    return self.active

  def getFilteredList(self,f):
    #filters on iddclass
    flist = []
    for i in self.active:
      if i.getClassnameIDD() == f:
        flist.append(i)
    return flist


  def getActiveReferences(self):
    return self.referencedict

  def buildDependsTree(self):
    for i in self.active:
      #first get a list of depend from object
      dl = i.getDepends()
      rl = i.getReference()
      #look through references and build dict
      for ref in rl:
        if not ref in self.referencedict:
          l = []
          l.append(i)
          self.referencedict[ref] = l
        else:
          self.referencedict[ref].append(i)
          
  
  def parseFile(self) :
    #pdb.set_trace()
    start = 1
    inclass = 0
    classblock = ''
    for line in self.fh:
      inclass = 0
      sline = string.strip(line)
      if re.match(r"^!\*.*",sline) :
        continue
      
      res = re.match(r"^!\s(.*)",sline)
      if res and start:
        self.comment = self.comment + res.group(1)
        continue
      #pdb.set_trace()
      dat = line.split('!')

      if re.search(",",dat[0]):
        inclass = 1
        start = 0
        classblock = classblock + dat[0].strip()

      if re.search(";",dat[0]):
        if not inclass:
          classblock = classblock + dat[0].strip()
        self.parseBlock(classblock)
        classblock = ''

  def parseBlock(self,textblock) :
    
    blocklines = textblock.split(',')
#    print textblock
#    pdb.set_trace()
    classname = ''
    itemlist = []
    
    for bline in blocklines:
      bline = bline.strip()
      items = re.split(r',|;',bline)
      if classname == '':
        #pdb.set_trace()
        classname = items[0]
        itemlist.append(classname)
        continue

      itemlist.append(items[0])
    #pdb.set_trace()
    evalstr =   'iddclass.'+ re.sub(r'[:-]','_',classname) +'()'
#    print evalstr
    classinstance = eval (evalstr)
#    if classname == 'BuildingSurface:Detailed':
#      print itemlist
#      print textblock
#      print blocklines
    classinstance.setData(itemlist)
    self.active.append(classinstance)
    

      
      
        
if __name__ == "__main__":
  c = idfRead('Singlezonetemplate.idf')
  alist = c.getActivelist()
  for o in alist:
    if o.getClassnameIDD() == 'Zone':
      print o.getClassnameIDD()
      print o.getName()
          
