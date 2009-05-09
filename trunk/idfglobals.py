# -*- coding: utf-8 -*-
import re

activeobjects = []
objectlist = []
objectdict = dict()
referencedict = dict()

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

    
  
    
    
    