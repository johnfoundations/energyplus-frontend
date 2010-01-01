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

from defaultconstruction import *

#surface edit routines.

#routines do not delete iddclass

def surfaceEditFloorToSlab(iclass):
    if iclass.getClassnameIDD() == 'Floor:Detailed':
        iclass.fieldlist[3].setValue('Ground')
        retiddclass = iclass.floor_detailed()
        for f,c in enumerate(iclass.fieldlist):
            retiddclass.field.list[c].setValue(f.getValue())
            
        return retiddclass
        
    if (iclass.getClassnameIDD() == 'Floor:Interzone') or (iclass.getClassnameIDD() == 'Floor:Adiabatic'):
        retiddclass = iddclass.floor_groundcontact()
        constructionclass = iclass.construction_ffactorgroundfloor()
        constructionclass.fieldlist[0].setValue(iddclass.getName() + "_ffactorgroundfloor")
        l = iclass.getFieldDataByName('Length')
        w = iclass.getFieldDataByName('Width')
        
        #construction:ffactorgroundfloor

        #self.InsertField(FieldText(self,"Name","","",""))
        #self.InsertField(FieldReal(self,"F-Factor",0,"","W/m-K","","",0.0,""))
        #self.InsertField(FieldReal(self,"Area",0,("Enter area of the floor","Units: m2",),"m2","","",0.0,""))
        #self.InsertField(FieldReal(self,"PerimeterExposed",0,("Enter exposed perimeter of the floor","Units: m",),"m",0.0,"","",""))

        
        try:
            lf = float(l)
            wf = float(w)
            area = lf*wf
            perimeter = (lf+wf)*2
            constructionclass.fieldlist[2].setValue(area)
            constructionclass.fieldlist[3].setValue(perimeter)
        except:
            print "length and width conversion failed"
            
        #copy data #floor:groundcontact
        #self.InsertField(FieldText(self,"Name","","",""))
        #self.InsertField(FieldObjectlist(self,"Construction Name","",("To be matched with a construction in this input file","If the construction is type *Construction:FfactorGroundFloor*,","then the GroundFCfactorMethod will be used.","",),"","ConstructionNames"))
        #self.InsertField(FieldObjectlist(self,"Zone Name","",("Zone the surface is a part of","",),"","ZoneNames"))
        #self.InsertField(FieldReal(self,"Azimuth Angle",0,"","",0,360,"",""))
        #self.InsertField(FieldReal(self,"Tilt Angle","180",("Floors are usually tilted 180 degrees","",),"",0,180,"",""))
        #self.InsertField(FieldReal(self,"Starting X Coordinate",0,("if not flat, should be lower left corner (from outside)","Units: m",),"m","","","",""))
        #self.InsertField(FieldReal(self,"Starting Y Coordinate",0,"","m","","","",""))
        #self.InsertField(FieldReal(self,"Starting Z Coordinate",0,"","m","","","",""))
        #self.InsertField(FieldReal(self,"Length",0,("Along X Axis","Units: m",),"m","","","",""))
        #self.InsertField(FieldReal(self,"Width",0,("Along Y Axis","Units: m",),"m","","","",""))

        retiddclass.fieldlist[1].setValue(constructionclass.getName())
        retiddclass.fieldlist[2].setValue(iclass.getFieldDataByName('Zone Name'))
        retiddclass.fieldlist[3].setValue(iclass.getFieldDataByName('Azimuth Angle')
        retiddclass.fieldlist[4].setValue(iclass.getFieldDataByName('Tilt Angle')
        retiddclass.fieldlist[5].setValue(iclass.getFieldDataByName('Starting X Coordinate')
        retiddclass.fieldlist[6].setValue(iclass.getFieldDataByName('Starting Y Coordinate')
        retiddclass.fieldlist[7].setValue(iclass.getFieldDataByName('Starting Z Coordinate')
        retiddclass.fieldlist[8].setValue(iclass.getFieldDataByName('Length')
        retiddclass.fieldlist[9].setValue(iclass.getFieldDataByName('Width')
        return retiddclass
        


        
    
        
    
    
    
def surfaceEditExteriorToInteriorWall(iclass,boundaryclass):

    intclass = iddclass.wall_interzone()
    intclass.fieldlist[0].setValue(iclass.getName())
    intclass.fieldlist[1].setValue("")  #interior wall construction
    intclass.fieldlist[2].setValue(iclass.getFieldDataByName('Zone Name'))
    intclass.fieldlist[3].setValue('')  #boundary class
    intclass.fieldlist[4].setValue(iclass.getFieldDataByName('Azimuth Angle')
    intclass.fieldlist[5].setValue(iclass.getFieldDataByName('Tilt Angle')
    intclass.fieldlist[6].setValue(iclass.getFieldDataByName('Starting X Coordinate')
    intclass.fieldlist[7].setValue(iclass.getFieldDataByName('Starting Y Coordinate')
    intclass.fieldlist[8].setValue(iclass.getFieldDataByName('Starting Z Coordinate')
    intclass.fieldlist[9].setValue(iclass.getFieldDataByName('Length')
    intclass.fieldlist[10].setValue(iclass.getFieldDataByName('Width')
    return intclass
        
    ##interior
          #self.InsertField(FieldText(self,"Name","","",""))
        #self.InsertField(FieldObjectlist(self,"Construction Name","",("To be matched with a construction in this input file","",),"","ConstructionNames"))
        #self.InsertField(FieldObjectlist(self,"Zone Name","",("Zone for the inside of the surface","",),"","ZoneNames"))
        #self.InsertField(FieldObjectlist(self,"Outside Boundary Condition Object","",("Specify a surface name in an adjacent zone for known interior walls.","Specify a zone name of an adjacent zone to automatically generate","the interior wall in the adjacent zone.","",),"","OutFaceEnvNames"))
        #self.InsertField(FieldReal(self,"Azimuth Angle",0,("Facing direction of outside of wall (S=180,N=0,E=90,W=270)","Units: deg",),"deg",0,360,"",""))
        #self.InsertField(FieldReal(self,"Tilt Angle","90",("Walls are usually tilted 90 degrees","Units: deg",),"deg",0,180,"",""))
        #self.InsertField(FieldReal(self,"Starting X Coordinate",0,("Starting (x,y,z) coordinate is the Lower Left Corner of the Wall","Units: m",),"m","","","",""))
        #self.InsertField(FieldReal(self,"Starting Y Coordinate",0,"","m","","","",""))
        #self.InsertField(FieldReal(self,"Starting Z Coordinate",0,"","m","","","",""))
        #self.InsertField(FieldReal(self,"Length",0,"","m","","","",""))
        #self.InsertField(FieldReal(self,"Height",0,"","m","","","",""))


def surfaceEditInteriorToExteriorWall(iddclass):
    extclass = iddclass.wall_exterior()
    extclass.fieldlist[0].setValue(iclass.getName())
    extclass.fieldlist[1].setValue('')  #construction
    extclass.fieldlist[2].setValue(iclass.getFieldDataByName('Zone Name'))
    extclass.fieldlist[3].setValue(iclass.getFieldDataByName('Azimuth Angle')
    extclass.fieldlist[4].setValue(iclass.getFieldDataByName('Tilt Angle')
    extclass.fieldlist[5].setValue(iclass.getFieldDataByName('Starting X Coordinate')
    extclass.fieldlist[6].setValue(iclass.getFieldDataByName('Starting Y Coordinate')
    extclass.fieldlist[7].setValue(iclass.getFieldDataByName('Starting Z Coordinate')
    extclass.fieldlist[8].setValue(iclass.getFieldDataByName('Length')
    extclass.fieldlist[9].setValue(iclass.getFieldDataByName('Width')
    return extclass
     
        #exterior
     #self.InsertField(FieldText(self,"Name","","",""))
        #self.InsertField(FieldObjectlist(self,"Construction Name","",("To be matched with a construction in this input file","",),"","ConstructionNames"))
        #self.InsertField(FieldObjectlist(self,"Zone Name","",("Zone the surface is a part of","",),"","ZoneNames"))
        #self.InsertField(FieldReal(self,"Azimuth Angle",0,("Facing direction of outside of wall (S=180,N=0,E=90,W=270)","Units: deg",),"deg",0,360,"",""))
        #self.InsertField(FieldReal(self,"Tilt Angle","90",("Walls are usually tilted 90 degrees","Units: deg",),"deg",0,180,"",""))
        #self.InsertField(FieldReal(self,"Starting X Coordinate",0,("Starting (x,y,z) coordinate is the Lower Left Corner of the Wall","Units: m",),"m","","","",""))
        #self.InsertField(FieldReal(self,"Starting Y Coordinate",0,"","m","","","",""))
        #self.InsertField(FieldReal(self,"Starting Z Coordinate",0,"","m","","","",""))
        #self.InsertField(FieldReal(self,"Length",0,"","m","","","",""))
        #self.InsertField(FieldReal(self,"Height",0,"","m","","","",""))

def surfaceEditWallSizeChange(iclass,origin,length,height):
    iclass.setFieldDataByName('Starting X Coordinate',origin[0])
    iclass.setFieldDataByName('Starting Y Coordinate',origin[1])
    iclass.setFieldDataByName('Starting Z Coordinate',origin[2])
    iclass.setFieldDataByName('Length',length)
    iclass.setFieldDataByName('Height',height)
    
    
def surfaceEditGetFaceAngle(v):
    #returns angle to ground in rads, and angle from vector 1,0,0 on flat plane in rads
    #transform [1] and [2] to [0]
    if len(v) < 3:
        return
    print self.idfclass.getName() ,self.idfclass.getClassnameIDD()
#        QtCore.pyqtRemoveInputHook() 
#        import pdb 
#        pdb.set_trace() 
        
    v1 = self.math.transform(v[0],v[1])
    v2 = self.math.transform(v[0],v[2])
    c = numpy.cross(v2,v1)
    #get angle to ground
    #unit
    c = self.math.mult(c,1/self.math.dist(c))
    c1 = c[:]
    c1[2] = 0.0
    d = numpy.dot(c,c1)
    if d > 1:
        d = 1
    ground = math.acos(d)
    print self.idfclass.getFieldDataByName('Tilt Angle'), self.idfclass.getFieldDataByName('View Factor to Ground')
    print 'ground',ground
    #azimuth, or direction on compass
    if ground == 1.57079632679:
        azimuth = ground
    else:
        na = [1.0,0.0,0.0]
        d = numpy.dot(na,c1)
        azimuth = math.acos(d)

    print 'azimuth',azimuth,self.idfclass.getFieldDataByName('Azimuth Angle')
    
    return ground,azimuth
        
def surfaceEditCreateWall(v1,v2,height,exterior,name,zonename):
    #v1 is bottom left corner. v2 is bottom right
    #exterior is boolean
    #assumes v1 and v2 are relative to whatever is in globalgeometryrules
    #only for vertical surfaces
    if exterior:
        iclass = iddclass.wall_exterior()
    else:
        iclass = iddclass.wall_interzone()
     
    verticelist = [] 
    verticelist.append(v1)
    verticelist.append(verticemath.add(v1,[0,0,height])
    verticelist.append(verticemath.add(v2,[0,0,height])
    verticelist.append(v2)
    
    res = surfaceEditGetFaceAngle(verticelist)
    
     
    iclass.setFieldDataByName('Name',name) 
    iclass.setFieldDataByName('Zone Name',zonename)
    iclass.setFieldDataByName('Starting X Coordinate',v1[0])
    iclass.setFieldDataByName('Starting Y Coordinate',v1[1])
    iclass.setFieldDataByName('Starting Z Coordinate',v1[2])
    iclass.setFieldDataByName('Length',verticemath.dist(v1,v2)
    iclass.setFieldDataByName('Height',height)
    iclass.setFieldDataByName("Azimuth Angle",res[1])
    iclass.setFieldDataByName('Tilt Angle',res[0])
    
    return iclass
     
def surfaceEditCreateFFactorGroundFloorClass(vlist,slist,floorname):
    constructionclass = iclass.construction_ffactorgroundfloor()
    constructionclass.fieldlist[0].setValue(floorname + "_ffactorgroundfloor")
    area = verticemath.polygonArea(vlist)
    #calculate perimeter
    perimeter = 0
    for i = range(0,len(slist-1):
        if slist[i] = 1:
            #outside
            perimeter += verticemath.dist(vlist[i],vlist[i+1])
    
    constructionclass.fieldlist[2].setValue(area)
    constructionclass.fieldlist[3].setValue(perimeter)
    return constructionclass
     
     
def surfaceEditCreateFloor(vlist,slist,slab,name,zonename):
    #vlist is same as zone vertice list
    #slist is boolean outside 1 inside 0
    #slab is boolean
    constructionclass = None
    if len(vlist) == 4:
        #simple surface
        if slab:
            #rectangular floor
            iclass = iddclass.floor_groundcontact()
            constructionclass = surfaceEditCreateFFactorGroundFloorClass(vlist,slist,name)
            iclass.setFieldDataByName('Construction Name',constructionclass.getName())
        else:
            iclass = iddclass.floor_interzone()
            iclass.setFieldDataByName('Construction Name',globaldefault.getDefault(iclass.getClassnameIDD())
            
        iclass.fieldlist[0].setValue(name)
        iclass.fieldlist[2].setValue(zonename)
        iclass.fieldlist[4].setValue(0)
        iclass.fieldlist[5].setValue(180)
        iclass.fieldlist[6].setValue(vlist[0][0])
        iclass.fieldlist[7].setValue(vlist[0][1])
        iclass.fieldlist[8].setValue(vlist[0][2])
        iclass.fieldlist[9].setValue(verticemath.dist(vlist[0],vlist[3])
        iclass.fieldlist[10].setValue(verticemath.dist(vlist[0],vlist[1])
        
        
            
            
        #class floor_interzone(ObjectAbstract):
        #self.InsertField(FieldText(self,"Name","","",""))
        #self.InsertField(FieldObjectlist(self,"Construction Name","",("To be matched with a construction in this input file","",),"","ConstructionNames"))
        #self.InsertField(FieldObjectlist(self,"Zone Name","",("Zone for the inside of the surface","",),"","ZoneNames"))
        #self.InsertField(FieldObjectlist(self,"Outside Boundary Condition Object","",("Specify a surface name in an adjacent zone for known interior ceilings.","Specify a zone name of an adjacent zone to automatically generate","the interior ceiling in the adjacent zone.","",),"","OutFaceEnvNames"))
        #self.InsertField(FieldReal(self,"Azimuth Angle",0,"","deg",0,360,"",""))
        #self.InsertField(FieldReal(self,"Tilt Angle","180",("Floors are usually tilted 180 degrees","Units: deg",),"deg",0,180,"",""))
        #self.InsertField(FieldReal(self,"Starting X Coordinate",0,("If not Flat, should be Lower Left Corner (from outside)","Units: m",),"m","","","",""))
        #self.InsertField(FieldReal(self,"Starting Y Coordinate",0,"","m","","","",""))
        #self.InsertField(FieldReal(self,"Starting Z Coordinate",0,"","m","","","",""))
        #self.InsertField(FieldReal(self,"Length",0,("Along X Axis","Units: m",),"m","","","",""))
        #self.InsertField(FieldReal(self,"Width",0,("Along Y Axis","Units: m",),"m","","","",""))

        #class floor_groundcontact(ObjectAbstract):
        #self.InsertField(FieldText(self,"Name","","",""))
        #self.InsertField(FieldObjectlist(self,"Construction Name","",("To be matched with a construction in this input file","If the construction is type *Construction:FfactorGroundFloor*,","then the GroundFCfactorMethod will be used.","",),"","ConstructionNames"))
        #self.InsertField(FieldObjectlist(self,"Zone Name","",("Zone the surface is a part of","",),"","ZoneNames"))
        #self.InsertField(FieldReal(self,"Azimuth Angle",0,"","",0,360,"",""))
        #self.InsertField(FieldReal(self,"Tilt Angle","180",("Floors are usually tilted 180 degrees","",),"",0,180,"",""))
        #self.InsertField(FieldReal(self,"Starting X Coordinate",0,("if not flat, should be lower left corner (from outside)","Units: m",),"m","","","",""))
        #self.InsertField(FieldReal(self,"Starting Y Coordinate",0,"","m","","","",""))
        #self.InsertField(FieldReal(self,"Starting Z Coordinate",0,"","m","","","",""))
        #self.InsertField(FieldReal(self,"Length",0,("Along X Axis","Units: m",),"m","","","",""))
        #self.InsertField(FieldReal(self,"Width",0,("Along Y Axis","Units: m",),"m","","","",""))
    
        
    else:
        #floor detailed
        iclass = iddclass.buildingsurface_detailed
        dl = []
        dl.append(name)
        dl.append('Floor')
        if slab:
            constructionclass = surfaceEditCreateFFactorGroundFloorClass(vlist,slist,name)
            dl.append(constructionclass.getName())  #slab construction name
            dl.append(zonename)
            dl.append('GroundFCfactorMethod')
        else:
            dl.append(globaldefault.getDefault(iclass.getClassnameIDD(),'Floor')) #default floor
            dl.append(zonename)
            dl.append('Zone')
        dl.append('')  #outside boundary, zone
        dl.append('NoSun')
        dl.append('NoWind')
        dl.append('autocalculate')
        dl.append('autocalculate')
        for v in vlist:
            dl.append(v[0])
            dl.append(v[1])
            dl.append(v[2])
            
        iclass.setData(dl)
        
    return iclass,constructionclass
        
        
        #self.InsertField(FieldText(self,"Name","","",""))
        #self.InsertField(FieldChoice(self,"Surface Type","","","",["Floor","Wall","Ceiling","Roof",]))
        #self.InsertField(FieldObjectlist(self,"Construction Name","",("To be matched with a construction in this input file","",),"","ConstructionNames"))
        #self.InsertField(FieldObjectlist(self,"Zone Name","",("Zone the surface is a part of","",),"","ZoneNames"))
        #self.InsertField(FieldChoice(self,"Outside Boundary Condition","","","",["Adiabatic","Surface","Zone","Outdoors","Ground","GroundFCfactorMethod","OtherSideCoefficients","OtherSideConditionsModel",]))
        #self.InsertField(FieldObjectlist(self,"Outside Boundary Condition Object","",("Non-blank only if the field Outside Boundary Condition is Surface,","Zone, OtherSideCoefficients or OtherSideConditionsModel","If Surface, specify name of corresponding surface in adjacent zone or","specify current surface name for internal partition separating like zones","If Zone, specify the name of the corresponding zone and","the program will generate the corresponding interzone surface","If OtherSideCoefficients, specify name of SurfaceProperty:OtherSideCoefficients","If OtherSideConditionsModel, specify name of SurfaceProperty:OtherSideConditionsModel","",),"","OutFaceEnvNames"))
        #self.InsertField(FieldChoice(self,"Sun Exposure","SunExposed","","",["SunExposed","NoSun",]))
        #self.InsertField(FieldChoice(self,"Wind Exposure","WindExposed","","",["WindExposed","NoWind",]))
        #self.InsertField(FieldRealAutocalculate(self,"View Factor to Ground","autocalculate",("From the exterior of the surface","Unused if one uses the *reflections* options in Solar Distribution in Building input","unless a DaylightingDevice:Shelf or DaylightingDevice:Tubular object has been specified.","autocalculate will automatically calculate this value from the tilt of the surface","",),"",0.0,1.0,"",""))
        #self.InsertField(FieldRealAutocalculate(self,"Number of Vertices","autocalculate",("shown with 120 vertex coordinates -- extensible object"," *extensible* -- duplicate last set of x,y,z coordinates, renumbering please","(and changing z terminator to a comma *,* for all but last one which needs a semi-colon *;*)","vertices are given in GlobalGeometryRules coordinates -- if relative, all surface coordinates","are *relative* to the Zone Origin.  If world, then building and zone origins are used","for some internal calculations, but all coordinates are given in an *absolute* system.","",),"",3,"","",""))
        #self.InsertField(FieldReal(self,"Vertex 1 X-coordinate",0,"","m","","","",""))
        #self.InsertField(FieldReal(self,"Vertex 1 Y-coordinate",0,"","m","","","",""))
        #self.InsertField(FieldReal(self,"Vertex 1 Z-coordinate",0,"","m","","","",""))


            