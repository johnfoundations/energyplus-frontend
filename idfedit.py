require "idfclass.rb"
require "idfdefines.rb"
require "arraychoice.rb"
require "idfsetup.rb"
require 'find'

$zones = []
$surfaces = []
$fenestration= []

$buildingnorthaxis = 0
$northsetup = false



  
def ZoneCreate
  if !$northsetup
    SetupNorth()
  end
  
  key = 1
  while key == 1
    if !$zones.empty?
      puts "Already existing zones"
      puts
      $zones.each do |zz|
        puts zz.Name
      end
      puts
    end
    puts "Creating a zone"
    puts "Zone Name: something like zone_abcd_basement"
    STDOUT.flush
    z = Zone.new(gets.chomp)
    puts "Zone North Axis, relative to Building North Axis. Default 0"
    
    STDOUT.flush
    na = gets.chomp
    if na == ''
      z.NorthAxis(0)
    else
      z.NorthAxis(na)
    end
    puts 'x,y,z zone origin'
    puts 'x='
    STDOUT.flush
    z.X gets.chomp
    puts 'y='
    STDOUT.flush
    z.Y gets.chomp
    puts 'z='
    STDOUT.flush
    z.Z gets.chomp
    

    puts "Zone Multiplier: multiplies calculated load by specified amount. Hit enter for default of 1, or enter value"
    STDOUT.flush
    zm = gets.chomp
    if zm == ''
      z.Multiplier(1)
    else
      z.Multiplier(zm)
    end

    puts 'Ceiling height: Hit enter for default, which is autocalculate, or enter value'
    STDOUT.flush
    ch = gets.chomp
    if ch ==''
      z.CeilingHeight('autocalculate')
    else
      z.CeilingHeight(ch)
    end

    puts 'Volume: hit enter for default which is autocalculate, or enter value'
    STDOUT.flush
    vo = gets.chomp
    if vo ==''
      z.Volume('autocalculate')
    else
      z.Volume(vo)
    end
    z.Print()
    puts 'Is this definition ok? enter y'
    STDOUT.flush
    key = gets.chomp
    if key == 'y'
      $zones << z
    else
      key = 1
    end
  end
  File.open($pj+'/zone.idf','w+') do |fh|
    z.PrintToFile(fh)
  end
end  #ZoneCreate


def SurfaceCreate
  if !$northsetup
    SetupNorth()
  end
  
  puts
  key = 1
  while key == 1
    if !$surfaces.empty?
      puts "Already existing surfaces"
      puts
      $surfaces.each do |ss|
        puts ss.Name
      end
      puts
    end
    puts "Creating a new surface"
    puts "Enter the surface name: something like Surface_ab_basement"
    STDOUT.flush
    s = BuildingSurface_Detailed.new(gets.chomp)
    s.RotationFromNorth($buildingnorthaxis.to_i)
    puts
    puts 'Surface Type:'
    puts
    stype = ArrayChoice(s.SurfaceTypes(),1)
    s.SurfaceType(stype)
    puts
    puts 'Construction Name: Choices are available from the dataset folder in the EnergyPlus installation'
    if stype == 'Wall'
      s.Construction(ArrayChoice(WallConstruction(),0))
    end
    if stype == 'Floor'
      s.Construction(ArrayChoice(FloorConstruction(),0))
    end
    if stype == 'Roof'
      s.Construction(ArrayChoice(RoofConstruction(),0))
    end
    if stype == 'Ceiling'
      s.Construction(ArrayChoice(CeilingConstruction(),0))
    end
    
    puts
    puts 'Zone name to which the surface belongs. The already defined Zones are '
    znames = []
    $zones.each do |zz|
      znames << zz.Name()
    end
    s.ZoneName(ArrayChoice(znames,0))
    puts
    puts 'Outside Boundary Condition:'
    s.OutsideBoundaryCondition(ArrayChoice(s.OutsideBoundaryConditions(),2))
    puts
    puts 'Sun Exposure: One of the following '
    s.SunExposure(ArrayChoice(s.SunExposures(),0))
    puts
    puts 'Wind exposure: One of the following '
    s.WindExposure(ArrayChoice(s.WindExposures(),0))
    puts
    puts 'View Factor: A number from 0.0 - horizontal facing away from the ground, to 1.0 horizontal facing the ground. A vertical wall is 0.5'
    puts 'Hit enter to accept the default of 0.5, or enter new value'
    STDOUT.flush
    vf = gets.chomp
    if vf == ''
      s.ViewFactor(0.5)
    else
      s.ViewFactor(vf)
    end
    puts

    puts 'Number of Vertices: This is the number of sides that the surface has. Default is 4, hit enter to accept, or enter a new number'
    STDOUT.flush
    nv = gets.chomp
    if nv == ''
      s.VerticeCount(4)
    else
      s.VerticeCount(nv)
    end

    puts
    puts 'Enter the x,y,z coordinates for the top right corner'
    puts 'x='
    STDOUT.flush
    x = gets.chomp
    puts 'y='
    STDOUT.flush
    y = gets.chomp
    puts 'z='
    z = gets.chomp
    tr = Vertice.new(x,y,z)
    
    puts
    puts 'Enter the x,y,z coordinates for the bottom left corner'
    puts 'x='
    STDOUT.flush
    x = gets.chomp
    puts 'y='
    STDOUT.flush
    y = gets.chomp
    puts 'z='
    z = gets.chomp
    bl = Vertice.new(x,y,z)

    s.VerticeDefine(bl,tr)
    puts
    s.Print(false)
    s.Print(true)
    puts
    puts 'Is this definition ok? enter y'
    STDOUT.flush
    key = gets.chomp
    if key == 'y'
      $surfaces << s
    else
      key = 1
    end
  end
  File.open($pj+'/surface.idf','w+') do |fh|
    s.PrintToFile(fh)
  end

end  #surfaces

def WindowDoorCreate

  key = 1
  while key == 1
    
    puts
    if !$fenestration.empty?
      $fenestration.each do |f|
        puts 'Already existing Windows and Doors'
        puts
        puts f.Name()
      end
    end

    puts 'Creating a new Window or Door'
    puts 'Enter a name, such as window_ab_1'
    STDOUT.flush
    w = Window.new(gets.chomp)

    puts 'Surface Type:'
    puts
    stype = ArrayChoice(w.SurfaceTypes(),1)
    w.SurfaceType(stype)
    puts
    puts 'Construction Name: Choices are available from the dataset folder in the EnergyPlus installation'
    if stype == 'Window'
      w.Construction(ArrayChoice(WindowConstruction(),0))
    end
    if stype == 'Door'
      w.Construction(ArrayChoice(DoorConstruction(),0))
    end
    if stype == 'GlassDoor'
      w.Construction(ArrayChoice(WindowConstruction(),0))
    end
    if stype == 'TubularDaylightDome'
      w.Construction(ArrayChoice(TubularDomeConstruction(),0))
    end
    if stype == 'TubularDaylightDiffuser'
      w.Construction(ArrayChoice(TubularDiffuserConstruction(),0))
    end

    puts
    puts 'Surface that this belongs to'
    surf = ArrayChoice($surfaces,0)
    w.BuildingSurfaceName(surf.Name())
    puts
    w.OutsideFaceEnvObject(' ')

    puts 'View Factor: A number from 0.0 - horizontal facing away from the ground, to 1.0 horizontal facing the ground. A vertical wall is 0.5'
    puts 'Hit enter to accept the default of 0.5, or enter new value'
    STDOUT.flush
    vf = gets.chomp
    if vf == ''
      w.ViewFactor(0.5)
    else
      w.ViewFactor(vf)
    end
    puts
    puts 'Shading Control: Hit enter for blank'
    w.ShadingControl(' ')
    STDOUT.flush
    gets.chomp
    puts
    w.FrameAndDivider(' ')
    puts 'How many equivalent windows or doors are there on this surface. Enter for default of 1'
    STDOUT.flush
    mc = gets.chomp
    if mc == ''
      w.Multiplier(1)
    else
      w.Multiplier(mc)
    end

    puts 'Number of Vertices: This is the number of sides that the window or door has. Default is 4, hit enter to accept, or enter a new number'
    STDOUT.flush
    nv = gets.chomp
    if nv == ''
      w.VerticeCount(4)
    else
      w.VerticeCount(nv)
    end

    puts
    puts 'Enter how far from the left edge of the wall to the left edge of the window or door'
    STDOUT.flush
    c = gets.chomp
    puts
    puts 'Enter the width of the door or window'
    STDOUT.flush
    w = gets.chomp
    puts 'Enter the height of the door or window'
    STDOUT.flush
    h = gets.chomp
    if stype == 'Door' || stype == 'GlassDoor'
      zz = surf.BottomLeftVertice.Z
    end
    if stype == 'Window'
      zz = (surf.TopLeftVertice.Z - surf.BottomLeftVertice.Z - h) / 2
    end

    bl = surf.BottomRightVertice.Transform(surf.BottomLeftVertice.X,surf.BottomLeftVertice.Y,zz,c)
    tl = surf.BottomRightVertice.Transform(surf.BottomLeftVertice.X,surf.BottomLeftVertice.Y,zz+h,c)

    br = surf.BottomRightVertice.Transform(surf.BottomLeftVertice.X,surf.BottomLeftVertice.Y,zz,c+w)
    tr = surf.BottomRightVertice.Transform(surf.BottomLeftVertice.X,surf.BottomLeftVertice.Y,zz+h,c+w)

    w.VerticeDefine(bl,br,tl,tr)
    puts
    w.Print(false)
    w.Print(true)
    puts
    puts 'Is this definition ok? enter y'
    STDOUT.flush
    key = gets.chomp
    if key == 'y'
      $fenestration << w
    else
      key = 1
    end
  end
  File.open($pj+'/fenestration.idf','w+') do |fh|
    w.PrintToFile(fh)
  end
end


  
  


  

  
def SetupNorth
  puts "To layout building orientation, choose a corner with a wall pointing away from it towards the North"
  puts "Call this corner a, and it's vertice is 0,0,0 and all other elements are in relation to it"
  puts "The next intersection or corner towards the north, call it b, and continue around the building with c,d,e etc."
  puts "The ab wall points North or nearly so. Enter angle offset from north."
  puts "Due north would be 0 degrees, towards the east -X degrees, west X degrees."
  STDOUT.flush
  $buildingnorthaxis = gets.chomp
  $northsetup = true
end
  

def PopulateArray(array,file,watchstr)
  if File.exists?(file)
    File.open(file, 'r') do |f1|
      while line = f1.gets
        reg = /#{watchstr}/
        m = reg.match(line)
        if m
          line = f1.gets
          lar = line.split('!')
          line = lar[0]
          line = line.strip
          line = line.chop
#               puts line
          array << line
        end
      end
    end
  end
end



puts "IDF Creator"

puts
puts 'Select project to edit, or hit Enter to create new one'
$ar = []
Find.find('./') do |f|
  if File.directory?(f)
    f = f.delete './'
    $ar << f
  end
end

$ar.insert(0,'Create New')
$pj = ArrayChoice($ar,0)

if $pj == 'Create New'
  puts 'Enter Name: Will create folder for data files'
  STDOUT.flush
  $pj = gets.chomp
  if !File.exist?($pj)
    Dir.mkdir($pj)
  end
end
SetupIDF($pj+'/'+$pj+'.idf')

#read zones,surfaces and windows from file
PopulateArray($zones,$pj+'/zone.idf','Zone,')
PopulateArray($surfaces,$pj+'/surface.idf','BuildingSurface:Detailed,')
PopulateArray($fenestration,$pj+'/fenestration.idf','FenestrationSurface:Detailed')

while $key != "q"
#  puts "Type L to select wall construction types"
   puts "Type W to insert a Window or Door"
#  puts "Type R to build a roof construction"
  puts "Type Z to create a Zone"
  puts "Type S to create a surface"
#  puts "Type N to set up building orientation"
  puts "Type q to quit"
  STDOUT.flush
  $key = gets.chomp
  if $key == "Z"
    ZoneCreate()
  end
  if $key == "S"
    if !$zones.empty?
      SurfaceCreate()
    else
      puts
      puts 'Create a Zone first ---'
      puts
    end
  end
  if $key == 'W'
    if !$surfaces.empty?
      WindowDoorCreate()
    else
      puts 'Create a wall Surface first ---'
    end
  end

end