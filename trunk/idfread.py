# -*- coding: utf-8 -*-


import iddclass
import string
import re
import pdb

class idfRead :
  def __init__(self,filename) :
    self.fh = open(filename, 'r')
    self.active = []
    self.activetree = []
    self.comment = ''
    self.referencedict = dict()
    self.parseFile()
    self.buildDependsTree()

  def getActivelist(self):
    return self.active

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
          
