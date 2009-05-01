# for editing additional loads

def CreatePeople(zone)
  #called with zone already selected
  puts 'Creating People loads for zone ' +zone

  puts 'Enter name. Something like people_zonename'
  STDOUT.flush
  p = People.new(gets.chomp)
  puts
  p.ZoneName(zone)
  puts 'Number of People Schedule name'
  
  