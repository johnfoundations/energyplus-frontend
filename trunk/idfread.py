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
    self.parseFile()

  def getActivelist(self):
    return self.active
  
  def parseFile(self) :
  #  pdb.set_trace()
    start = 1
    inclass = 0
    classblock = ''
    for line in self.fh:
      sline = string.strip(line)
      if re.match(r"^!\*.*",sline) :
        continue
      
      res = re.match(r"^!\s(.*)",sline)
      if res and start:
        self.comment = self.comment + res.group(1)
        continue

      dat = line.split('!')

      if re.search(",",dat[0]):
        inclass = 1
        start = 0
        classblock = classblock + dat[0]

      if re.search(";",dat[0]):
        classblock = classblock + dat[0]
        inclass = 0
        self.parseBlock(classblock)
        classblock = ''

  def parseBlock(self,textblock) :
    blocklines = textblock.splitlines()
    classname = ''
    itemlist = []
    
    for bline in blocklines:
      bline = bline.strip()
      items = bline.split(',')
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
    classinstance.setData(itemlist)
    self.active.append(classinstance)
    

      
      
        
if __name__ == "__main__":
  c = idfRead('Singlezonetemplate.idf')
  alist = c.getActivetree()
  print alist.__class__.__name__
 # for k,v in alist.iteritems() :
  #  print k
  #  for li in v:
  #    print '   ' +li.__class__.__name__
      #getName()
      
          
