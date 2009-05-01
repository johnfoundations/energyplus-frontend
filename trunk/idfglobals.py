# -*- coding: utf-8 -*-
import re

activeobjects = []
objectlist = []
objectdict = dict()

def getActiveObjectsList(type) :
  list = []
  for t in activeobjects:
    if t.classname == type:
      list.append(t.name)
  return list

def getObjectType(type) :
  list = []
  for t in objectlist :
    if re.search(type,t) :
      list.append(t)
  return list

def getObjectTree() :
  return objectdict

    
  
    
    
    