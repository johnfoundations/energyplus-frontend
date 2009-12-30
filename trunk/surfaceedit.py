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
     
def surfaceEditCreateFloor(vlist,slab,name,zonename):
    #vlist is same as zone vertice list
    #slab is boolean
    if slab:
        if len(vlist) == 4:
            #rectangular floor
            iclass = iddclass.floor_groundcontact()
            constructionclass = iclass.construction_ffactorgroundfloor()
            constructionclass.fieldlist[0].setValue(name() + "_ffactorgroundfloor")
            l = verticemath.dist(vlist[0],vlist[1])
            w = verticemath.dist(vlist[0],vlist[3])
            area = l*w
            perimeter = (l+w)*2
            constructionclass.fieldlist[2].setValue(area)
            constructionclass.fieldlist[3].setValue(perimeter)
            iclass.setFieldDataByName('Construction Name',constructionclass.getName())
            
        else:
            #floor detailed
            iclass = iddclass.surface_detailed