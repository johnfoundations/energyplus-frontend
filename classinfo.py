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

allconstructionclasses = "BuildingSurface:Detailed","Wall:Detailed","RoofCeiling:Detailed","Floor:Detailed",\
                         "FenestrationSurface:Detailed",\
                         "Shading:Zone:Detailed","Shading:Site:Detailed","Shading:Building:Detailed",\
                         "Zone","Building",\
                         "GlazedDoor:Interzone","GlazedDoor","Door","Door:Interzone","Window:Interzone","Window",\
                         "Wall:Exterior","Wall:Adiabatic","Wall:Underground","Wall:Interzone",\
                         "Shading:Site","Shading:Building",\
                         "Ceiling:Adiabatic","Ceiling:Interzone","Floor:GroundContact","Floor:Adiabatic","Floor:Interzone",\
                         "Roof","Zone"
                
doorclasses = "GlazedDoor:Interzone","GlazedDoor","Door","Door:Interzone"        

windowclasses = "Window:Interzone","Window"

wallclasses = "Wall:Detailed","Wall:Exterior","Wall:Adiabatic","Wall:Underground","Wall:Interzone"

roofceilingclasses = "Ceiling:Adiabatic","Ceiling:Interzone", "Roof","RoofCeiling:Detailed"

floorclasses = "Floor:Detailed","Floor:GroundContact","Floor:Adiabatic","Floor:Interzone"

mixedclasses = "BuildingSurface:Detailed","FenestrationSurface:Detailed"
                
                
                
                         
verticeclasses = "BuildingSurface:Detailed","Wall:Detailed","RoofCeiling:Detailed","Floor:Detailed","FenestrationSurface:Detailed"
                 
#verticesurfaceelementclasses = 
        #all have vertices

verticeshadingclasses = "Shading:Zone:Detailed","Shading:Site:Detailed","Shading:Building:Detailed"


zoneclasses = ("Zone","Building")

surfaceelementclasses = "GlazedDoor:Interzone","GlazedDoor","Door","Door:Interzone","Window:Interzone","Window"
        #multiplier,xy,length,height

azimuthwallclasses = "Wall:Exterior","Wall:Adiabatic","Wall:Underground","Wall:Interzone"
        #azimuth,tilt,xyz,length,width
        
azimuthshadingclasses = "Shading:Site","Shading:Building"

azimuthflatclasses = "Ceiling:Adiabatic","Ceiling:Interzone","Floor:GroundContact","Floor:Adiabatic","Floor:Interzone",\
                     "Roof"



def constructionType(iddclass):
    #returns 'wall','window',etc.
    #first check if a construction element
    if not iddclass.getClassnameIDD() in allconstructionclasses:
        return ''
        
    if iddclass.getClassnameIDD() in doorclasses:
        return 'Door'
        
    if iddclass.getClassnameIDD() in windowclasses:
        return 'Window'
    
    if iddclass.getClassnameIDD() in wallclasses:
        return 'Wall'
    
    if iddclass.getClassnameIDD() in roofceilingclasses:
        return 'RoofCeiling'
    
    if iddclass.getClassnameIDD() in floorclasses:
        return 'Floor'
    
    if iddclass.getClassnameIDD() in mixedclasses:
        return iddclass.getFieldDataByName('Surface Type')
        
    if iddclass.getClassnameIDD() == "Zone":
        return 'Zone'

    return ''
            
    
