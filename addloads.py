# -*- coding: utf-8 -*-
# additional loads; people, electrical, lights etc.

class People :
  def __init__ (name) :
    classname = 'People'
    name = name
  

  def Name :
    return name


  def ZoneName (z) :
    zonename = z
  

  def NumberOfPeopleSchedule (s) :
    numberofpeopleschedule = s

  
  def NumberOfPeopleCalculation (c) :
    numberofpeoplecalculation = c
  
  def NumberOfPeopleCalculations :
    return ['People','People/Area','Area/Person']
    

  def NumberOfPeople(n) :
    numberofpeople = n


  def PeoplePerSqMeter(n) :
    peoplepersqmeter = n


  def SqMeterPerPerson (n) :
    sqmeterperperson = n


  def FractionRadiant (f) :
    fractionradiant = f

  
  def SensibleHeatFraction(s) :
    sensibleheatfraction = s


  def ActivityLevelSchedule (s) :
    activitylevelschedule = s


  def AshraeComfortWarnings(b) :
    ashraecomfortwarnings = b


#   def MeanRadiantTempCalcType(s)
#     meanradianttempcalctype = s
#
# 
#   def MeanRadiantTempCalcTypes
#     return ['ZoneAveraged','SurfaceWeighted','AngleFactor',]
#
# 
#   def SurfaceNameFactorListName (s)
#     surfacenamefactorlistname = s
#
# 
#   def WorkEfficiencyScheduleName (s)
#     workefficiencyschedule = s
#
# 
#   def ClothingInsulationScheduleName (s)
#     clothinginsulationschedule = s
#
# 
#   def AirVelocityScheduleName (s)
#     airvelocityschedule =s
#

  def Print() :
    print
    print classname + ','
    print zonename
    print numberofpeopleshedule
    if numberofpeoplecalculation == 'People'
      print 'People,            !Number of People calculation method'
      print numberofpeople +  ' ,   ! Number of People'

    if numberofpeoplecalculation == 'People/Area'
      print 'People/Area,       !Number of People calculation method'
      print peoplepersqmeter +  ',   ! Number of People per sq meter'

    if numberofpeoplecalculation == 'Area/Person'
      print 'Area/Person,       !Number of People calculation method'
      print sqmeterperperson +  ',   ! Sq meter per person'

    print fractionradiant +     ',Fraction Radiant'
    print sensibleheatfraction   ',Sensible Heat Fraction blank for auto'
    print activitylevelschedule  '; Activity level schedule'


  
    
  



  
  if __name__ == "__main__":  