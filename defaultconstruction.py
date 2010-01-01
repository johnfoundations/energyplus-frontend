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

import classinfo
import idfabstractmodel

#stores default selections for things like construction, or materials.


#defaults stored in dict indexed by idf class name. data is array of pairs. [[count],[dict fieldname:value]]
class defaultContruction():
    def __init__(self,model = None):
        self.defaultlist = dict()
        if model:
            self.readDefaults(model)
            
            
    def setModel(self,model):
        self.readDefaults(model)
            
            
    def readDefaults(self,model):
        dlist = dict()
        for i in model.idfsource.idflist:
            if i.getClassnameIDD() in classinfo.constructionelements:
                n = i.getClassnameIDD()
                if n in dlist:
                    found = False
                    for dl in dlist[n]:
                        if dl[1]== i.getFieldDataByName('Construction Name'):
                            dl[0] += 1
                            found == True
                            
                    if not found:
                        dlist[n].append([[1],[i.getFieldDataByName('Construction Name')]])
                        
                else:  #not found in dict
                    dlist[n] = [[[1],[i.getFieldDataByName('Construction Name')]]]

            if i.getClassnameIDD() in classinfo.mixedclasses:
                n = i.getClassnameIDD() + ':' + i.getFieldDataByName('Surface Type')
                if n in dlist:
                    found = False
                    for dl in dlist[n]:
                        if dl[1]== i.getFieldDataByName('Construction Name'):
                            dl[0] += 1
                            found == True
                            
                    if not found:
                        dlist[n].append([[1],[i.getFieldDataByName('Construction Name')]])
                        
                else:  #not found in dict
                    dlist[n] = [[[1],[i.getFieldDataByName('Construction Name')]]]






            if i.getClassnameIDD() == 'Construction:CfactorUndergroundWall':
                n = i.getClassnameIDD()
                if n in dlist:
                    found = False
                    for dl in dlist[n]:
                        if dl[1]== i.getFieldDataByName('C-Factor'):
                            dl[0] += 1
                            found == True
                            
                    if not found:
                        dlist[n].append([[1],[i.getFieldDataByName('C-Factor')]])
                        
                else:  #not found in dict
                    dlist[n] = [[[1],[i.getFieldDataByName('C-Factor')]]]

                
            if i.getClassnameIDD() == 'Construction:FFactorGroundFloor':
                n = i.getClassnameIDD()
                if n in dlist:
                    found = False
                    for dl in dlist[n]:
                        if dl[1]== i.getFieldDataByName('F-Factor'):
                            dl[0] += 1
                            found == True
                            
                    if not found:
                        dlist[n].append([[1],[i.getFieldDataByName('F-Factor')]])
                        
                else:  #not found in dict
                    dlist[n] = [[[1],[i.getFieldDataByName('F-Factor')]]]

        for k in dlist.keys():
            v = 0
            highest = 0
            print k
            for i,l in enumerate(dlist[k]):
                if l[0] > v:
                    v = l[0]
                    highest = i
                    
            self.defaultlist[k] = dlist[k][highest][1]
                
    def getDefault(self,classname,modifier = None):
        if modifier:
            cname = classname + ':' + modifier
        else:
            cname = classname
            
        return self.defaultlist[cname]


globaldefault = defaultConstruction()













if __name__ == "__main__":
    import sys
    import idfdata
    from PyQt4 import QtGui

    try:
        fname = sys.argv[1]
    except:
        fname = '5ZoneTDV.idf'

    f = idfdata.idfData()
    f.openIdf(fname)

    model = idfabstractmodel.idfAbstractModel(f)
    default = defaultContruction(model)
    print default.defaultlist
    