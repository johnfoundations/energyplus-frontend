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

import os
import re

def getRDDVariables(filename,rdd):
    #get path to rdd file
    basename = os.path.split(str(filename))[1]
    directory = os.path.split(str(filename))[0]
#    print basename, directory
    name = os.path.splitext(basename)
#    print name
    if rdd:
        rddfile = directory + '/Output/' + name[0] + '.rdd' 
    else:
        rddfile = directory + '/Output/' + name[0] + '.mdd' 
#    print rddfile
    if os.path.exists(rddfile):
        #examine file
        #if first character a !, then it is in idd format.
        #otherwise text.
#Program Version,EnergyPlus, Linux, VERSION 4.0.0.024,IDD_Version 4.0.0.024
#Var Type (reported time step),Var Report Type,Variable Name [Units]
#Zone,Average,Outdoor Dry Bulb [C]
#Zone,Average,Outdoor Dew Point [C]
#Zone,Average,Outdoor Wet Bulb [C]

    
#! Program Version,EnergyPlus, Linux, VERSION 4.0.0.024,IDD_Version 4.0.0.024
#! Output:Variable Objects (applicable to this run)
#Output:Variable,*,Outdoor Dry Bulb,hourly; !- Zone Average [C]
#Output:Variable,*,Outdoor Dew Point,hourly; !- Zone Average [C]
        try:
            fh = open(rddfile, 'r')
        except:
            return
            
        idf = False
            
        res = []    
            
        for line in fh:
            #check first line
            if re.match(r"^!.+",line):
                idf = True
                continue
            
            if re.match(r"^Program Version.*",line):
                continue
            
            if re.match(r"^Var Type (.*)",line):
                continue
            
            if idf:
                v = re.match(r"^(.*),(.*),(.*),(.+); !- (.+) (.+) \[(.*)\]$",line)
                #('Output:Variable', '*', 'Tot SimAirLoopComponents Calls', 'hourly', 'HVAC', 'Sum', '[]')
                res.append([v.group(3),v.group(5),v.group(6),v.group(7),v.group(2),v.group(4)])
                
            else:
                v = re.match(r"^(.+),(.+),(.+) \[(.*)\]$",line)
                #('HVAC', 'Sum', 'Tot SimAirLoopComponents Calls','[]')
                res.append([v.group(3),v.group(1),v.group(2),v.group(4),'*',''] )
                
                
        return res
                
            
                
    
    
if __name__ == "__main__":
    print getRDDVariables('/home/derek/energyplus-frontend/energyplus-frontend/wildlifegenetics/wlgidealair3.rdd')[3]
    print getRDDVariables('/home/derek/energyplus-frontend/energyplus-frontend/wildlifegenetics/wlgidealair4.rdd')[3]
    
