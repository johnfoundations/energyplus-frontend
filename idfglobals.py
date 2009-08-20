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



import re

activeobjects = []
objectlist = []
objectdict = dict()  #populated by iddclass.py
referencedict = dict()  #populated by idfdata.py

#model role definitions

IdfClassRole = 33  #data method returns the idf object instance for the requested row

#idf query flags
IdfQueryAll = 0
IdfQueryClassname = 1
IdfQueryName = 2
IdfQueryGroup = 3
IdfQueryDependancy = 4
IdfQueryReference = 5
IdfQueryFieldname = 6
IdfQueryFieldValue = 7

def getActiveObjectsList(otype) :
  ol = []
  if otype in referencedict:
    for l in referencedict[otype]:
      ol.append(l.getName())
  return ol

def getObjectType(otype) :
  list = []
  for t in objectlist :
    if re.search(otype,t) :
      list.append(t)
  return list

def getObjectTree() :
  return objectdict

def getDepends(name):
    dlist = []
    for o in referencedict[name]:
        dlist.append(o.getName())
    return dlist
    

    
  
    
    
    