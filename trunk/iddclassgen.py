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
import string
import pdb
#from PyQt4 import QtGui


#globals

activeobjects = []
objectlist = []

IDD_Version = ''



class IddField :
    def __init__(self,fieldname):
        self.Fieldattr = dict()
        self.Fieldattr['Field'] = fieldname
        self.fieldeditor = ''

    def insertAttr(self,key,attr)  :
        self.Fieldattr[key]= attr

    def getFieldName(self):
        return self.Fieldattr['Field']
        integer

   #types real,alpha,choice,object-list

    def createWidgetInitLine(self):
        self.fieldeditor = ''
        if 'units' in self.Fieldattr:
            unitstr = 'Units: ' + self.Fieldattr['units']
        else:
            unitstr = ''
            
        if self.Fieldattr['type'] == 'alpha':
            #(self,parent,fieldname,default,notes):
            if 'units' in self.Fieldattr:
                if self.Fieldattr['units'] == 'hh:mm':
                    self.fieldeditor = 'FieldTime(self,'
            if self.fieldeditor == '':
                self.fieldeditor = 'FieldText(self,'
            if 'Field' in self.Fieldattr :
                self.fieldeditor = self.fieldeditor + '"' + self.Fieldattr['Field'] + '",'
            else:
                self.fieldeditor = self.fieldeditor + '"Field",'
            if 'default' in self.Fieldattr:
                self.fieldeditor = self.fieldeditor + '"' + self.Fieldattr['default'] + '",'
            else:
                self.fieldeditor = self.fieldeditor + '"",'
            if 'notes' in self.Fieldattr:
                note = '('
                for n in self.Fieldattr['notes'] :
                    n = re.sub(r'"','*',n)
                    note = note + '"' + n + '",'
                note = note + '"' + unitstr + '",'
                self.fieldeditor = self.fieldeditor + note + '))'
            else:
                self.fieldeditor = self.fieldeditor + '"")'
      
      
        
      
      
        elif self.Fieldattr['type'] == 'real':
            #self,parent,fieldname,default,notes,min,max,mingt,maxlt
            if 'default' in self.Fieldattr :
                if self.Fieldattr['default'] == 'autocalculate':
                    self.fieldeditor = 'FieldRealAutocalculate(self,'
            if 'autosizable' in self.Fieldattr:
                #  pdb.set_trace()
                self.fieldeditor = 'FieldRealAutocalculate(self,'
            if self.fieldeditor == '':
                self.fieldeditor = 'FieldReal(self,'
            if 'Field' in self.Fieldattr :
                self.fieldeditor = self.fieldeditor + '"' + self.Fieldattr['Field'] + '",'
            else:
                self.fieldeditor = self.fieldeditor + '"Field",'
            if 'default' in self.Fieldattr:
                self.fieldeditor = self.fieldeditor + '"' + self.Fieldattr['default'] + '",'
            else:
                self.fieldeditor = self.fieldeditor + '0,'
            if 'notes' in self.Fieldattr:
                note = '('
                for n in self.Fieldattr['notes'] :
                    n = re.sub(r'"','*',n)
                    note = note + '"' + n + '",'
                note = note + '"' + unitstr + '",'
                self.fieldeditor = self.fieldeditor + note + '),'
            else:
                self.fieldeditor = self.fieldeditor + '"",'

            if 'minimum' in self.Fieldattr :
                self.fieldeditor = self.fieldeditor + self.Fieldattr['minimum'] + ','
            else:
                self.fieldeditor = self.fieldeditor + '"",'
            if 'maximum' in self.Fieldattr :
                self.fieldeditor = self.fieldeditor + self.Fieldattr['maximum'] + ','
            else:
                self.fieldeditor = self.fieldeditor + '"",'
            if 'minimum>' in self.Fieldattr :
                self.fieldeditor = self.fieldeditor + self.Fieldattr['minimum>'] + ','
            else:
                self.fieldeditor = self.fieldeditor + '"",'
            if 'maximum<' in self.Fieldattr :
                self.fieldeditor = self.fieldeditor + self.Fieldattr['maximum<'] + ')'
            else:
                self.fieldeditor = self.fieldeditor + '"")'

      
        elif self.Fieldattr['type'] == 'integer':
            #(self,parent,fieldname,default,notes,min,max,mingt,maxlt)
            self.fieldeditor = 'FieldInt(self,'
            if 'Field' in self.Fieldattr :
                self.fieldeditor = self.fieldeditor + '"' +self.Fieldattr['Field'] + '",'
            else:
                self.fieldeditor = self.fieldeditor + '"Field",'
            if 'default' in self.Fieldattr:
                self.fieldeditor = self.fieldeditor + '"' + self.Fieldattr['default'] + '",'
            else:
                self.fieldeditor = self.fieldeditor + '0,'
            if 'notes' in self.Fieldattr:
                note = '('
                for n in self.Fieldattr['notes'] :
                    n = re.sub(r'"','*',n)
                    note = note + '"' + n + '",'
                note = note + '"' + unitstr + '",'
                self.fieldeditor = self.fieldeditor + note + '),'
            else:
                self.fieldeditor = self.fieldeditor + '"",'

            if 'minimum' in  self.Fieldattr :
                self.fieldeditor = self.fieldeditor + self.Fieldattr['minimum'] + ','
            else:
                self.fieldeditor = self.fieldeditor + '"",'
            if 'maximum' in self.Fieldattr :
                self.fieldeditor = self.fieldeditor + self.Fieldattr['maximum'] + ','
            else:
                self.fieldeditor = self.fieldeditor + '"",'
            if 'minimum>' in self.Fieldattr :
                self.fieldeditor = self.fieldeditor + self.Fieldattr['minimum>'] + ','
            else:
                self.fieldeditor = self.fieldeditor + '"",'
            if 'maximum<' in self.Fieldattr :
                self.fieldeditor = self.fieldeditor + self.Fieldattr['maximum<'] + ')'
            else:
                self.fieldeditor = self.fieldeditor + '"")'
                                
              
        elif self.Fieldattr['type'] == 'choice':
            #(self,parent,fieldname,default,notes,choices):
            if 'default' in self.Fieldattr:
                if self.Fieldattr['default'] == 'On' or self.Fieldattr['default'] == 'Off' :
                    self.fieldeditor = 'FieldOnOff(self,'
                elif self.Fieldattr['default'] == 'Yes' or self.Fieldattr['default'] == 'No' :
                    self.fieldeditor = 'FieldYesNo(self,'
                else:
                    self.fieldeditor = 'FieldChoice(self,'
            else:
                self.fieldeditor = 'FieldChoice(self,'
            if 'Field' in self.Fieldattr :
                self.fieldeditor = self.fieldeditor + '"' +self.Fieldattr['Field'] + '",'
            else:
                self.fieldeditor = self.fieldeditor + '"Field",'
            if 'default' in self.Fieldattr:
                self.fieldeditor = self.fieldeditor + '"' +self.Fieldattr['default'] + '",'
            else:
                self.fieldeditor = self.fieldeditor + '"",'
            if 'notes' in self.Fieldattr:
                note = '('
                for n in self.Fieldattr['notes'] :
                    n = re.sub(r'"','*',n)
                    note = note + '"' + n + '",'
                note = note + '"' + unitstr + '",'
                self.fieldeditor = self.fieldeditor + note + '),'
            else:
                self.fieldeditor = self.fieldeditor + '"",'
            choice = '['
            if 'choices' in self.Fieldattr :
                for c in self.Fieldattr['choices'] :
                    choice = choice + '"' + c + '",'
                choice = choice + ']'
            else:
                choice = choice + '"]'
            self.fieldeditor = self.fieldeditor + choice + ')'
      
        elif self.Fieldattr['type'] == 'object-list':
            #self,parent,fieldname,default,notes,objectlistname)
            self.fieldeditor = 'FieldObjectlist(self,'
            if 'Field' in self.Fieldattr :
                self.fieldeditor = self.fieldeditor + '"' +self.Fieldattr['Field'] + '",'
            else:
                self.fieldeditor = self.fieldeditor + '"Field",'
            if 'default' in self.Fieldattr:
                self.fieldeditor = self.fieldeditor + '"' +self.Fieldattr['default'] + '",'
            else:
                self.fieldeditor = self.fieldeditor + '"",'
            if 'notes' in self.Fieldattr:
                note = '('
                for n in self.Fieldattr['notes'] :
                    n = re.sub(r'"','*',n)
                    note = note + '"' + n + '",'
                note = note + '"' + unitstr + '",'
                self.fieldeditor = self.fieldeditor + note + '),'
            else:
                self.fieldeditor = self.fieldeditor + '"",'

            if 'object_list' in self.Fieldattr :
                self.fieldeditor = self.fieldeditor + '"' +self.Fieldattr['object_list'] + '")'
            else:
                self.fieldeditor = self.fieldeditor + '"")'

        elif self.Fieldattr['type'] == 'vertice':
            self.fieldeditor = 'FieldVertice(self,'
            if 'Field' in self.Fieldattr :
                self.fieldeditor = self.fieldeditor + '"' +self.Fieldattr['Field'] + '",'
            else:
                self.fieldeditor = self.fieldeditor + '"Field",'
            if 'default' in self.Fieldattr:
                self.fieldeditor = self.fieldeditor + '"' +self.Fieldattr['default'] + '",'
            else:
                self.fieldeditor = self.fieldeditor + '"",'
            if 'notes' in self.Fieldattr:
                note = '('
                for n in self.Fieldattr['notes'] :
                    n = re.sub(r'"','*',n)
                    note = note + '"' + n + '",'
                note = note + '"' + unitstr + '",'
                self.fieldeditor = self.fieldeditor + note + '))'
            else:
                self.fieldeditor = self.fieldeditor + '"")'



      
        else:
            print 'not object line in ' + self.Fieldattr['Field'] + 'of type ' + self.Fieldattr['type']
      

      

    def Print(self) :
        print
        for f,a in self.Fieldattr.iteritems() :
            print f, a

    def PrintFieldInit(self) :
        #returns line that will be included in the class init.
        return self.fieldeditor
  


class IddObject :
    def __init__(self,classname) :
        self.iddValues = dict()
        self.insertValue('classname',classname)
        self.fields = []


    def insertValue(self,key,value):
        self.iddValues[key]=value

    def insertField(self,field) :
        self.fields.append(field)

    def getClassname(self):
        return self.iddValues['classname']

    def getGroupname(self):
        return self.iddValues['group']

    def getClassnamePy(self):
        s = re.sub(r'[:-]','_',self.iddValues['classname'])
        s = s.lower()
        #pdb.set_trace()
        return s

    def objectFixup(self) :
        pass
        # fix up certain classes or objects
        #any vertice class make extensible
    #    if 'format' in self.iddValues:
    #      if self.iddValues['format'] == 'vertices':
    #        if 'extensible' in self.iddValues:
    #          pass
    #        else:
    #          self.iddValues['extensible'] = '4'






    def adjustFieldList(self,num):
        #extensible.
        #Rules:
        #if vertice, then stop at vertice count and insert vertice as field type
        #look for numbered, such as day name 1
    #   pdb.set_trace()
        newlist = []
        c = 1
        watch = 0
        numb = int(num)
        for n in self.fields :
    #      if re.search("Number of Vertices",n.getFieldName()):
    #        f = IddField(n.getFieldName())
    #        f.insertAttr('type','vertice')
    #        newlist.append(f)
    #        break
            if re.search(str(c),n.getFieldName()) :
                if watch <= numb :
                    watch = watch + 1
                    if watch == numb:
                        c = c+1
                    elif watch > numb:
                        break
            elif watch > 0:
                watch = 0
            newlist.append(n)
        self.fields = newlist




    def Print(self):
        print
        print self.iddValues
        for f in self.fields :
            f.Print()
      
    def createClass(self,fh)  :
        fh.write("\n\n")
        if 'format' in self.iddValues:
            if self.iddValues['format'] == 'vertices':
                fh.write("class " + self.getClassnamePy() + "(ObjectVertice):\n")
            elif self.iddValues['format'] == 'ViewFactor':
                fh.write("class " + self.getClassnamePy() + "(ObjectViewFactor):\n")
            elif self.iddValues['format'] == 'FluidProperty':
                fh.write("class " + self.getClassnamePy() + "(ObjectFluidProperty):\n")
            elif self.iddValues['format'] == 'singleLine':
                fh.write("class " + self.getClassnamePy() + "(ObjectSingleLine):\n")
            elif self.iddValues['format'] == 'compactSchedule':
                fh.write("class " + self.getClassnamePy() + "(ObjectCompactSchedule):\n")
            elif self.iddValues['format'] == 'Spectral':
                fh.write("class " + self.getClassnamePy() + "(ObjectSpectral):\n")
            else:
                print self.iddValues['format']
        else:
            fh.write("class " + self.getClassnamePy() + "(ObjectAbstract):\n")
        self.objectFixup()
        fh.write("    def CreateFields(self) :\n")
        if 'extensible' in self.iddValues:
            self.adjustFieldList(self.iddValues['extensible'])

        requiredfieldlist = []
        for c,f in enumerate(self.fields):
            if 'required-field' in f.Fieldattr:
                requiredfieldlist.append(c)
            f.createWidgetInitLine()
            fh.write('        self.InsertField(' + f.PrintFieldInit() + ")\n")

        fh.write("\n\n")

        if len(requiredfieldlist) > 0:
            fh.write('        self.setRequiredFields(' + requiredfieldlist.__str__() + ')\n')
            
        if 'memo' in self.iddValues :
            memolist = self.iddValues['memo']
            memostr = ''
            for m in memolist:
                m = re.sub(r'"','*',m)
                memostr = memostr + '"' + m + '",'
            fh.write('        self.insertMemo((' + memostr + '))\n')

        if 'reference' in self.iddValues:
            reflist = self.iddValues['reference']
            for r in reflist:
                fh.write('        self.addReference("' + r + '")\n')

        if 'required-object' in self.iddValues :
            fh.write('        self.setRequired(True)\n')
        else:
            fh.write('        self.setRequired(False)\n')
        if 'min-fields' in self.iddValues :
            fh.write('        self.setMinfields(' + self.iddValues['min-fields'] + ')\n')
        else:
            fh.write('        self.setMinfields(0)\n')
        if 'group' in self.iddValues :
            fh.write('        self.setGroup("' + self.iddValues['group'] + '") \n')
        else:
            fh.write('        self.setGroup("")\n')
        if 'extensible' in self.iddValues:
            fh.write('        self.setExtensible(' + self.iddValues['extensible'] + ')\n')
        else:
            fh.write('        self.setExtensible(-1)\n')
        fh.write('        self.setClassnameIDD("' + self.getClassname() + '")\n')

        fh.write("\n\n\n")



class IddClassGen :
    def __init__(self) :
        self.fh = open('V4-0-0-Energy+.idd', 'r')
        self.type = ''
        self.unit = ''
        self.min = ''
        self.mingt = ''
        self.max = ''
        self.maxlt = ''
        self.objlist = ''
        self.default = ''
        self.reqfield = 0
        self.iddclasslist = []
        self.IDD_Version = ''
        self.parseFile()
        self.writeClassDef()
        

    def writeClassDef(self) :
        ofh = open('iddclass.py','w')


        ofh.write("# -*- coding: utf-8 -*-\n")
        ofh.write("from fieldclasses import *\n")
        ofh.write("from objectclass import *\n")
        ofh.write("import idfglobals")
        ofh.write("\n\n\n")
        iddgroupnamelist = dict()
        iddclassnamelist = []
    #   pdb.set_trace()
        for iddclass in self.iddclasslist :
            iddclass.createClass(ofh)
            groupname = iddclass.getGroupname()
            if groupname in iddgroupnamelist :
                iddgroupnamelist[groupname].append(iddclass.getClassname())
            else:
                iddclassnamelist = []
                iddgroupnamelist[groupname] = iddclassnamelist
                iddgroupnamelist[groupname].append(iddclass.getClassname())
        ofh.write("\n\n\n")
        iddclassnamelist = iddgroupnamelist.keys()
    #    pdb.set_trace()
        for gnl in iddclassnamelist :
            ofh.write('olist = []\n')
            for cn in iddgroupnamelist[gnl] :
                ofh.write('olist.append("' + cn + '")\n')
            ofh.write('idfglobals.objectdict["' + gnl + '"] = olist\n')
        ofh.write('\n\n')
        ofh.write('if __name__ == "__main__":\n')
        ofh.write('    n = idfglobals.objectdict.keys() \n')
        ofh.write('    for p in n:\n')
        ofh.write('        for am in idfglobals.objectdict[p] :\n')
        ofh.write('            print am\n\n')

        ofh.close()





    def assignVars(self) :
        #pdb.set_trace()
        iddfield = IddField(self.fieldname)
        iddfield.insertAttr('Variable', self.fieldvar)
        t = 0
        if self.type:
            self.type = self.type.lower()
            iddfield.insertAttr('type',self.type)
            t = 1
            self.type = ''
        if self.unit:
            iddfield.insertAttr('units', self.unit)
            self.unit = ''
        if self.min:
            iddfield.insertAttr('minimum', self.min)
            self.min = ''
        if self.max:
            iddfield.insertAttr('maximum', self.max)
            self.max = ''
        if self.mingt:
            iddfield.insertAttr('minimum>', self.mingt)
            self.mingt = ''
        if self.maxlt:
            iddfield.insertAttr('maximum<', self.maxlt)
            self.maxlt = ''

        if self.objlist:
        #      pdb.set_trace()
            iddfield.insertAttr('object_list', self.objlist)
            self.objlist = ''
        if self.reqfield:
            iddfield.insertAttr('required-field','required-field')
            self.reqfield = 0
        if self.autosizable:
            iddfield.insertAttr('autosizable',True)
            self.autosizable = False
        if not t:
            #  pdb.set_trace()
            if re.search('A',self.fieldvar):
                iddfield.insertAttr('type', 'alpha')
            else:
                iddfield.insertAttr('type', 'real')
        if len(self.choices) > 0 :
            iddfield.insertAttr('choices',self.choices)
            self.choices = []

        if len(self.notes) > 0:
            iddfield.insertAttr('notes',self.notes)
            self.notes = []
        if self.default:
            iddfield.insertAttr('default',self.default)
            self.default = ''
        self.idobj.insertField(iddfield)





    def parseObject(self,obj,gn):
        #pdb.set_trace()
        items = obj.splitlines()
        if re.match(r"^\\",items[0]):
            return
    
        self.choices = []
        self.memos = []
        self.notes = []
        self.references = []
        self.autosizable = False
        # status constants. 0 = start, 1 = found either A or N1, watching for details
        # 2 = found type, looking for keys, min, max defaults
        run = 0
        firstfield = 1
        for v in items:
            if run == 0 :  #first run
                cn = v.split(",")
                v = v.strip()
                v = v.strip(',')
                self.classname = cn[0]
                self.idobj = IddObject(cn[0])
                run = 1
                if cn[1] == '':
                    continue
                else:
                    v = cn[1]
        #     if re.search("CTF",v):
        #       pdb.set_trace()
            if re.search("\\\\",v) :
                #split off at comments
                ds = v.split("\\")
                c = ds[1].strip()
                e = ds[0].strip()
                if re.match(r"^[AN][0-9]*.*",e):
                    e = e.strip(';')
                    e = e.strip(',')
                    e = e.strip()

                fn = re.match(r"^[fF]ield\s(.*)",c)
                if fn:
                    if firstfield:
                        firstfield = 0
                        self.fns = fn
                        self.fieldname = self.fns.group(1)
                        self.fieldvar = e
                        continue
                    self.assignVars()
                    self.fieldvar = e
                    self.fns = fn
                    self.fieldname = self.fns.group(1)


                self.res = re.match(r"^[tT]ype\s+(.*)",c)
                if self.res:
                    self.type = self.res.group(1)
                    continue
                self.res = re.match(r"^[uU]nits\s(.*)",c)
                if self.res:
                    self.unit = self.res.group(1)
                    continue
                self.res = re.match(r"^[kK]ey\s(.*)",c)
                if self.res:
                    self.choices.append(self.res.group(1))
                    continue
                self.res = re.match(r"^[mM]inimum\s(.*)",c)
                if self.res:
                    self.min = self.res.group(1).translate(None,'>')
                    continue
                self.res = re.match(r"^[Mm]aximum\s(.*)",c)
                if self.res:
                    self.max = self.res.group(1)
                    continue
                self.res = re.match(r"^[mM]inimum>\s(.*)",c)
                if self.res:
                    self.mingt = self.res.group(1)

                    continue
                self.res = re.match(r"^[Mm]aximum<\s(.*)",c)
                if self.res:
                    self.maxlt = self.res.group(1)
                    continue
                self.res = re.match(r"^[Mm]emo\s(.*)",c)
                if self.res:
                    self.memos.append(self.res.group(1))
                self.res = re.match(r"^[nN]ote\s(.*)",c)
                if self.res:
                    self.notes.append(self.res.group(1))
                #pdb.set_trace()
                self.res = re.match(r"^[Dd]efault\s(.*)",c)
                if self.res:
                    self.default = self.res.group(1)
                    continue
                self.res = re.match(r"^[oO]bject\-list\s(.*)",c)
                if self.res:
                    self.objlist = self.res.group(1)
                    continue

                self.res = re.match(r"^[rR]equired-field(.*)",c)
                if self.res:
                    self.reqfield = 1
                    continue
                self.res = re.match(r"^[Ff]ormat\s(.*)",c)
                if self.res:
                    self.idobj.insertValue('format',self.res.group(1))
                    continue
                self.res = re.match(r"^[mM]in-fields\s(.*)",c)
                if self.res:
                    self.idobj.insertValue("min-fields",self.res.group(1))
                    continue
                #pdb.set_trace()
                self.res = re.match(r"^[Uu]nique-object.*",c)
                if self.res:
                    self.idobj.insertValue('unique-object','')
                    continue
                self.res = re.match(r"^autosizable.*",c)
                if self.res:
                    #pdb.set_trace()
                    self.autosizable = True
                    continue
                self.res = re.match(r"^autocalculatable.*",c)
                if self.res:
                    self.autosizable = True
                    continue
                self.res = re.match(r"^[Rr]eference\s(.*)",c)
                if self.res:
                    self.references.append(self.res.group(1))

                self.res = re.match(r"^extensible:([0-9])\s.*",c)
                if self.res:
        #          pdb.set_trace()
                    self.idobj.insertValue('extensible',self.res.group(1))

                self.res = re.match(r"^[Rr]equired-object.*",c)
                if self.res:
                    self.idobj.insertValue('required-object','')
                    continue

        #no / for comments in the line
            else :
                #pdb.set_trace()
                vlist = v.split(",")
                for var in vlist:
                    var = var.strip()
                    #pdb.set_trace()
                    self.res = re.match(r"^([AN][0-9]+).*",var)
            #          print var
                    if self.res :
                        self.fieldvar = self.res.group(1)
                        self.fieldname = self.res.group(1)
                        self.assignVars()


  
        # end of stuff
        if self.classname ==  'Version':
            self.default = self.IDD_Version
        self.assignVars()
        if len(self.memos) > 0:
            self.idobj.insertValue('memo',self.memos)
        if len(self.references) > 0:
            self.idobj.insertValue('reference',self.references)
        self.idobj.insertValue('group',gn)
        #self.idobj.Print()

        self.iddclasslist.append(self.idobj)
    

         
        




#      else:
        #no comments
#        if re.search(",",v) :
#          is = v.split(',')
          
          
    
#    print obj
#    quit()
    


    def parseFile(self) :
        #status flag 0 = empty state, looking for new object.
        # 1 = first line that contains a comma or ; after empty state
        #pdb.set_trace()
        self.status = 0
        self.longline = ''
        self.groupname = ''
        for line in self.fh:
            sline = string.strip(line)
#      if re.search("For Week  53",line):
      
      
            if sline == '' :
                continue


            if re.match(r"^!",line):
                v = re.match(r"^!IDD_Version\s([0-9]+\.[0-9]+\.[0-9]+)\.*",line)
                if v:
                    self.IDD_Version = v.group(1)
                    print self.IDD_Version
                    
                continue
            
            gf = re.match(r"^\\[Gg]roup\s(.*)",line)
            if gf:
                self.groupname = gf.group(1)
                self.groupname = string.strip(self.groupname)
                continue
        
      #
            if self.status == 0:
    #            print line
                #pdb.set_trace()
                if re.search("\\\\",line)  :
                    ls = line.split('\\')
                    if re.search(",",ls[0]):
                        self.status = 3
                        self.longline = self.longline + ls[0]+ '\n' + ls[1]
                    else:
                        self.longline = self.longline + line
                elif re.search(",",line):
                    self.status = 3
                if self.status == 3:
                    if not self.longline == '':
                        #  print self.longline
                        self.parseObject(self.longline,self.groupname)
                    self.longline = ''
                    self.status = 1
                    self.longline = self.longline + line


        

            elif re.search(",",line) or re.search("\\\\",line):
                self.longline = self.longline + line

            if re.search(";",line):
                # pdb.set_trace()
                #check if before the /
                ds = line.split("\\")
                if re.search(";",ds[0]) :
                    self.status = 0

        #last object
        self.parseObject(self.longline,self.groupname)
           
           

          
#          if not re.match(r"^[AN][0-9]+.*",line) :
#            print line
        
          




if __name__ == "__main__":
    c = IddClassGen()

 
      
      
      

