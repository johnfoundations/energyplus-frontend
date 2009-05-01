$ConstructionType = []
$WindowType = []
$FloorType = []
$WallType = []

def GetConstructionTypes
  ENV.each {|k,v| if k == 'PATH' then $p = v end}
  ar = $p.split(':')

  ar.each do |element|
    ear = element.scan('EnergyPlus')
    if !ear.empty?
      $epdir = element
    end
  end

  $epdir = $epdir.chomp('bin')

  #puts $epdir
  $epdir = $epdir + 'datasets'

  #puts $epdir


  File.open($epdir +'/CompositeWallConstructions.idf', 'r') do |f1|
    while line = f1.gets
      reg = /Construction,/
      m = reg.match(line)
      if m
        line = f1.gets
        lar = line.split('!')
        line = lar[0]
        line = line.strip
        line = line.chop
  #     puts line
        $ConstructionType << line
      end
    end
  end


  File.open($epdir +'/ASHRAE_2005_HOF_Materials.idf', 'r') do |f1|
    while line = f1.gets
      reg = /Construction,/
      m = reg.match(line)
      if m
        line = f1.gets
        lar = line.split('!')
        line = lar[0]
        line = line.strip
        line = line.chop
  #      puts line
        $ConstructionType << line
      end
    end
  end

  File.open($epdir +'/WindowConstructs.idf', 'r') do |f1|
    while line = f1.gets
      reg = /Construction,/
      m = reg.match(line)
      if m
        line = f1.gets
        lar = line.split('!')
        line = lar[0]
        line = line.strip
        line = line.chop
        #puts line
        $WindowType << line
      end
    end
  end
end


def SelectWallType
  if $ConstructionType.empty?
    GetConstructionTypes()
  end
  puts 'Select wall construction types for use in your layout'
  puts 'Enter the line numbers you want, for example 13,3,15 and hit enter'
  count = -1
  $ConstructionType.each do |litem|
    count = count + 1
    puts count.to_s + '   ' + litem
  end
  STDOUT.flush
  sel = gets.chomp
  selarray = sel.split(',')
  selarray.each do |n|
    ctarray << n
  end

  return ctarray
end

def BuildWallType

end


def WallConstruction
  wallarray = []
  File.open('ConstructionMaterials.idf', 'r') do |f1|
    while line = f1.gets
      reg = /Construction,/
      m = reg.match(line)
      if m
        line = f1.gets
        lar =  line.split('!')
        line = lar[0]
        line = line.strip        
        line = line.chop
        rx = /Wall/i
        if rx.match(line)
          puts   line
          wallarray << line
        end
      end
    end
  end
  return wallarray
end


def FloorConstruction
  floorarray = []
  File.open('ConstructionMaterials.idf', 'r') do |f1|
    while line = f1.gets
      reg = /Construction,/
      m = reg.match(line)
      if m
        line = f1.gets
        lar =  line.split('!')
        line = lar[0]
        line = line.strip
        line = line.chop
        rx = /floor|slab/i
        if rx.match(line)
          puts   line
          floorarray << line
        end
      end
    end
  end
  return floorarray
end

def WindowConstruction
  windowarray = []
  File.open('ConstructionMaterials.idf', 'r') do |f1|
    while line = f1.gets
      reg = /Construction,/
      m = reg.match(line)
      if m
        line = f1.gets
        lar =  line.split('!')
        line = lar[0]
        line = line.strip
        line = line.chop
        rx = /window/i
        if rx.match(line)
          puts   line
          windowarray << line
        end
      end
    end
  end
  return windowarray
end

def RoofConstruction
  roofarray = []
  File.open('base.idf', 'r') do |f1|
    while line = f1.gets
      reg = /Construction,/
      m = reg.match(line)
      if m
        line = f1.gets
        lar =  line.split('!')
        line = lar[0]
        line = line.strip
        line = line.chop
        rx = /roof/i
        if rx.match(line)
          puts   line
          roofarray << line
        end
      end
    end
  end
  return roofarray
end

def CeilingConstruction
  ceilingarray = []
  File.open('ConstructionMaterials.idf', 'r') do |f1|
    while line = f1.gets
      reg = /Construction,/
      m = reg.match(line)
      if m
        line = f1.gets
        lar =  line.split('!')
        line = lar[0]
        line = line.strip
        line = line.chop
        rx = /ceiling/i
        if rx.match(line)
          puts   line
          ceilingarray << line
        end
      end
    end
  end
  return ceilingarray
end

def PeopleSchedules
  ar = []
end


#WallConstruction()
#FloorConstruction()
#WindowConstruction()