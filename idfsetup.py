$filename = ''

def SetupIDF(filename)
  if File.exists?(filename)
    puts filename + ' exists. Enter to keep, any other key to edit'
    STDOUT.flush
    if gets.chomp == ''
      return
    end
  end

  puts 'writing to ' + filename
  File.open(filename,'w') do |fh|
    fh.puts "Version, \n   3.0.0;  !- Version \n\nTimestep,\n  6;  !- Number of Timesteps per Hour\n\n"

    fh.puts "Building,"
    puts 'Building Details:'
    puts 'Building Name'
    STDOUT.flush
    fh.puts gets.chomp + ',   ! Name'
    puts
    fh.puts "0.0,  ! North Axis"
    ar = ['Country,','Suburbs,','City,','Ocean,','Urban,',]
    fh.puts ArrayChoice(ar,1) + '!  Terrain' 
    puts
    fh.puts '4.0,   !  Loads Convergence Tolerance Value'
    fh.puts '0.4,   !  Temperature Convergence Tolerance Value'
    puts 'Solar Distribution'
    ar = ['MinimalShadowing','FullExterior','FullInteriorAndExterior','FullExteriorWithReflections','FullInteriorAndExteriorWithReflections',]
    fh.puts ArrayChoice(ar,1) + ',   ! Solar Distribution'
    puts
    fh.puts '25;    ! Maximum Number of Warmup Days'

    puts


    
    fh.puts "SimulationControl,"

    puts 'SimulationControl'
    puts
    puts 'Do Zone Sizing Calculation? Enter for Yes'
    STDOUT.flush
    a = gets.chomp
    if a == ''
      fh.puts "Yes, !- Do Zone Sizing Calculation"
    else
      fh.puts "No,  !- Do Zone Sizing Calculation"
    end

    a = ''
    puts
    puts "Do System Sizing Calculation? Enter for Yes"
    STDOUT.flush
    a = gets.chomp
    if a == ''
      fh.puts "Yes,  !- Do System Sizing Calculation"
    else
      fh.puts "No,   !- Do System Sizing Calculation"
    end
    a = ''
    puts
    puts 'Do Plant Sizing Calculation? Enter for Yes'
    STDOUT.flush
    a = gets.chomp
    if a == ''
      fh.puts "Yes,  !- Do Plant Sizing Calculation"
    else
      fh.puts "No,   !- Do Plant Sizing Calculation"
    end
    a = ''
    puts
    puts 'Run Simulation for Sizing Periods? Enter for Yes'
    STDOUT.flush
    a = gets.chomp
    if a == ''
      fh.puts "Yes,  !- Run Simulation for Sizing Periods"
    else
      fh.puts "No,   !- Run Simulation for Sizing Periods"
    end
    a = ''
    puts
    puts 'Run Simulation for Weather File Run Periods? Enter for Yes'
    STDOUT.flush
    a = gets.chomp
    if a == ''
      fh.puts "Yes;   !- Run Simulation for Weather File Run Periods"
    else
      fh.puts  "No;    !- Run Simulation for Weather File Run Periods"
    end



    fh.puts "RunPeriod,\n  1,  !- Begin Month\n  1,  !- Begin Day of Month\n  12,  !- End Month\n  31,  !- End Day of Month\n
                  Sunday,  !- Day of Week for Start Day\n  No,  !- Use Weather File Holidays and Special Days\n
                  No,  !- Use Weather File Daylight Saving Period\n  No,  !- Apply Weekend Holiday Rule\n
                  Yes,  !- Use Weather File Rain Indicators\n  Yes,  !- Use Weather File Snow Indicators\n
                  1.0000;  !- Number of Times Runperiod to be Done"


    puts 'SurfaceConvectionAlgorithm:Inside'
    fh.puts  "\n\nSurfaceConvectionAlgorithm:Inside,"
    ar = ['Simple','Detailed','CeilingDiffuser',]
    fh.puts  ArrayChoice(ar,0)

    puts 'SurfaceConvectionAlgorithm:Outside'
    fh.puts   "\n\nSurfaceConvectionAlgorithm:Outside,"
    ar = ['Simple','Detailed','BLAST','TARP','DOE-2','MoWiTT',]
    fh.puts ArrayChoice(ar,0)

    puts 'HeatBalanceAlgorithm'
    fh.puts "\n\nHeatBalanceAlgorithm,"
    ar = ['ConductionTransferFunction','MoisturePenetrationDepthConductionTransferFunction','ConductionFiniteDifference','CombinedHeatAndMoistureFiniteElement',]
    fh.puts ArrayChoice(ar,0)
    fh.puts "200.0000;  !- Surface Temperature Upper Limit"

    fh.puts "\n\nSizing:Parameters,\n  1.2000,  !- Sizing Factor\n  6;  !- Time Steps in Averaging Window\n\n"

    fh.puts "ConvergenceLimits,\n  1,  !- Minimum System Timestep\n  20;  !- Maximum HVAC Iterations\n\n"

    fh.puts "ShadowCalculation,\n  30,  !- Calculation Frequency\n  15000;  !- Maximum Figures in Shadow Overlap Calculations\n\n"

    fh.puts "! US National Holidays\n"
    

    fh.puts "RunPeriodControl:SpecialDays,\nNew Years Day,           !- Name\nJanuary 1,               !- Start Date\n"
    fh.puts "1,                       !- Duration {days}\nHoliday;                 !- Special Day Type\n\n"
    fh.puts "RunPeriodControl:SpecialDays,\n    Veterans Day,            !- Name\nNovember 11,             !- Start Date\n"
    fh.puts "1,                       !- Duration {days}\nHoliday;                 !- Special Day Type\n\n"

fh.puts "RunPeriodControl:SpecialDays,\n
    Christmas,               !- Name\n
December 25,             !- Start Date\n
1,                       !- Duration {days}\n
Holiday;                 !- Special Day Type\n\n"

fh.puts"RunPeriodControl:SpecialDays,\n
    Independence Day,        !- Name\n
July 4,                  !- Start Date\n
1,                       !- Duration {days}\n
Holiday;                 !- Special Day Type\n\n"

fh.puts"RunPeriodControl:SpecialDays,\n
    MLK Day,                 !- Name\n
3rd Monday in January,   !- Start Date\n
1,                       !- Duration {days}\n
Holiday;                 !- Special Day Type\n\n"

fh.puts"RunPeriodControl:SpecialDays,\n
    Presidents Day,          !- Name\n
3rd Monday in February,  !- Start Date\n
1,                       !- Duration {days}\n
Holiday;                 !- Special Day Type\n\n"

fh.puts "RunPeriodControl:SpecialDays,\n
    Memorial Day,            !- Name\n
Last Monday in May,      !- Start Date\n
1,                       !- Duration {days}\n
Holiday;                 !- Special Day Type\n\n"

fh.puts "RunPeriodControl:SpecialDays,
    Labor Day,               !- Name
1st Monday in September, !- Start Date
1,                       !- Duration {days}
Holiday;                 !- Special Day Type\n\n"

fh.puts "RunPeriodControl:SpecialDays,
    Columbus Day,            !- Name
2nd Monday in October,   !- Start Date
1,                       !- Duration {days}
Holiday;                 !- Special Day Type\n\n"

fh.puts "RunPeriodControl:SpecialDays,
    Thanksgiving,            !- Name
4th Thursday in November,!- Start Date
1,                       !- Duration {days}
Holiday;                 !- Special Day Type\n\n"

fh.puts "! Daylight Saving Period in US\n\n"

fh.puts "RunPeriodControl:DaylightSavingTime,
    2nd Sunday in March,     !- Start Date
    1st Sunday in November;  !- End Date\n\n"



fh.puts "Site:Location,
    SPOKANE_WA_USA TMY2-24157,  !- Name
47.63000,                !- Latitude {deg}
-117.5300,               !- Longitude {deg}
-8.000000,               !- Time Zone {hr}
721.0000;                !- Elevation {m}\n\n"

fh.puts "Site:GroundTemperature:BuildingSurface,
    19.87,                   !- January Ground Temperature {C}
19.91,                   !- February Ground Temperature {C}
19.93,                   !- March Ground Temperature {C}
19.97,                   !- April Ground Temperature {C}
20.01,                   !- May Ground Temperature {C}
20.03,                   !- June Ground Temperature {C}
20.01,                   !- July Ground Temperature {C}
19.00,                   !- August Ground Temperature {C}
19.00,                   !- September Ground Temperature {C}
20.04,                   !- October Ground Temperature {C}
20.03,                   !- November Ground Temperature {C}
20.01;                   !- December Ground Temperature {C}\n\n"

fh.puts "! Daily Avg, -2.8, 0.6, 4.3, 7.2, 11.7, 16.3, 21.8, 19.3, 14.9, 8.0, 1.7, -1.0\n\n"

fh.puts "Site:WaterMainsTemperature,
    CORRELATION,             !- Calculation Method
,                        !- Temperature Schedule Name
8.50,                    !- Annual Average Outdoor Air Temperature {C}
24.60;                   !- Maximum Difference In Monthly Average Outdoor Air Temperatures {deltaC}\n\n"

fh.puts "! SPOKANE_WA_USA Annual Heating 99.6%, MaxDB=-15.8�C\n\n"

fh.puts "SizingPeriod:DesignDay,
    SPOKANE Ann Htg 99.6% Condns DB,  !- Name
-15.8,                   !- Maximum Dry-Bulb Temperature {C}
0.0,                     !- Daily Temperature Range {deltaC}
-15.8,                   !- Humidity Indicating Conditions at Maximum Dry-Bulb
92958.,                  !- Barometric Pressure {Pa}
3.1,                     !- Wind Speed {m/s}
30,                      !- Wind Direction {deg}
0.00,                    !- Sky Clearness
0,                       !- Rain Indicator
0,                       !- Snow Indicator
21,                      !- Day of Month
12,                      !- Month
WinterDesignDay,         !- Day Type
0,                       !- Daylight Saving Time Indicator
WetBulb;                 !- Humidity Indicating Type\n\n"

fh.puts "! SPOKANE_WA_USA Annual Cooling (DB=>MWB) .4%, MaxDB=32.8�C MWB=16.8�C\n\n"

fh.puts "SizingPeriod:DesignDay,
    SPOKANE Ann Clg .4% Condns DB=>MWB,  !- Name
32.8,                    !- Maximum Dry-Bulb Temperature {C}
14.3,                    !- Daily Temperature Range {deltaC}
16.8,                    !- Humidity Indicating Conditions at Maximum Dry-Bulb
92958.,                  !- Barometric Pressure {Pa}
3.1,                     !- Wind Speed {m/s}
230,                     !- Wind Direction {deg}
1.00,                    !- Sky Clearness
0,                       !- Rain Indicator
0,                       !- Snow Indicator
21,                      !- Day of Month
8,                       !- Month
SummerDesignDay,         !- Day Type
0,                       !- Daylight Saving Time Indicator
WetBulb;                 !- Humidity Indicating Type\n\n"



fh.puts "ScheduleTypeLimits,
Any Number;              !- Name\n\n"

fh.puts "ScheduleTypeLimits,
    Fraction,                !- Name
0.0:1.0,                 !- Range
CONTINUOUS;              !- Numeric Type\n\n"

fh.puts "ScheduleTypeLimits,
    Temperature,             !- Name
-60:200,                 !- Range
CONTINUOUS;              !- Numeric Type\n\n"

fh.puts "ScheduleTypeLimits,
    On/Off,                  !- Name
0:1,                     !- Range
DISCRETE;                !- Numeric Type\n\n"

fh.puts "ScheduleTypeLimits,
    Control Type,            !- Name
0:4,                     !- Range
DISCRETE;                !- Numeric Type\n\n"

fh.puts "ScheduleTypeLimits,
    Humidity,                !- Name
10:90,                   !- Range
CONTINUOUS;              !- Numeric Type\n\n"

fh.puts "ScheduleTypeLimits,
Number;                  !- Name\n\n"


fh.puts "! Schedule set    Schedule_Office_ASHRAE_90.1-1989_TypTstatSetback[]\n\n"
fh.puts "! Hours: Weekly: 92, Yearly: 4797\n\n"
fh.puts "! Schedule Office Lighting,  ASHRAE 90.1-1989, Section 13 w/addenda\n\n"

fh.puts "Schedule:Compact,
    BLDG_LIGHT_SCH,          !- Name
Fraction,                !- Schedule Type Limits Name
Through: 12/31,          !- Field 1
For: Weekdays,           !- Field 2
Until: 05:00,            !- Field 3
0.05,                    !- Field 4
Until: 07:00,            !- Field 5
0.1,                     !- Field 6
Until: 08:00,            !- Field 7
0.3,                     !- Field 8
Until: 17:00,            !- Field 9
0.9,                     !- Field 10
Until: 18:00,            !- Field 11
0.5,                     !- Field 12
Until: 20:00,            !- Field 13
0.3,                     !- Field 14
Until: 22:00,            !- Field 15
0.2,                     !- Field 16
Until: 23:00,            !- Field 17
0.1,                     !- Field 18
Until: 24:00,            !- Field 19
0.05,                    !- Field 20
For: SummerDesignDay,    !- Field 21
Until: 24:00,            !- Field 22
1.0,                     !- Field 23
For: Saturday,           !- Field 24
Until: 06:00,            !- Field 25
0.05,                    !- Field 26
Until: 08:00,            !- Field 27
0.1,                     !- Field 28
Until: 12:00,            !- Field 29
0.3,                     !- Field 30
Until: 17:00,            !- Field 31
0.15,                    !- Field 32
Until: 24:00,            !- Field 33
0.05,                    !- Field 34
For: WinterDesignDay,    !- Field 35
Until: 24:00,            !- Field 36
0.0,                     !- Field 37
For: Sunday Holidays AllOtherDays,  !- Field 38
Until: 24:00,            !- Field 39
0.05;                    !- Field 40\n\n"

fh.puts "! Schedule Office Receptacle,  ASHRAE 90.1-1989, Section 13\n\n"
fh.puts "! MODIFIED for increased off-hours plug loads (to account for more IT equipment)\n\n"
fh.puts "! Hours: Weekly: 86.15, Yearly: 4492\n\n"

fh.puts "Schedule:Compact,
    BLDG_EQUIP_SCH,          !- Name
Fraction,                !- Schedule Type Limits Name
Through: 12/31,          !- Field 1
For: Weekdays,           !- Field 2
Until: 08:00,            !- Field 3
0.40,                    !- Field 4
Until: 12:00,            !- Field 5
0.90,                    !- Field 6
Until: 13:00,            !- Field 7
0.80,                    !- Field 8
Until: 17:00,            !- Field 9
0.90,                    !- Field 10
Until: 18:00,            !- Field 11
0.50,                    !- Field 12
Until: 24:00,            !- Field 13
0.40,                    !- Field 14
For: SummerDesignDay,    !- Field 15
Until: 24:00,            !- Field 16
1.0,                     !- Field 17
For: Saturday,           !- Field 18
Until: 06:00,            !- Field 19
0.30,                    !- Field 20
Until: 08:00,            !- Field 21
0.4,                     !- Field 22
Until: 12:00,            !- Field 23
0.5,                     !- Field 24
Until: 17:00,            !- Field 25
0.35,                    !- Field 26
Until: 24:00,            !- Field 27
0.30,                    !- Field 28
For: WinterDesignDay,    !- Field 29
Until: 24:00,            !- Field 30
0.0,                     !- Field 31
For: Sunday Holidays AllOtherDays,  !- Field 32
Until: 24:00,            !- Field 33
0.30;                    !- Field 34\n\n"

fh.puts "! Schedule Office Occupancy,\n\n"

fh.puts "    Schedule:Compact,
    BLDG_OCC_SCH,            !- Name
Fraction,                !- Schedule Type Limits Name
Through: 12/31,          !- Field 1
For: Weekdays,           !- Field 2
Until: 06:00,            !- Field 3
0.0,                     !- Field 4
Until: 07:00,            !- Field 5
0.1,                     !- Field 6
Until: 08:00,            !- Field 7
0.2,                     !- Field 8
Until: 12:00,            !- Field 9
0.95,                    !- Field 10
Until: 13:00,            !- Field 11
0.5,                     !- Field 12
Until: 17:00,            !- Field 13
0.95,                    !- Field 14
Until: 18:00,            !- Field 15
0.3,                     !- Field 16
Until: 20:00,            !- Field 17
0.1,                     !- Field 18
Until: 24:00,            !- Field 19
0.05,                    !- Field 20
For: SummerDesignDay,    !- Field 21
Until: 06:00,            !- Field 22
0.0,                     !- Field 23
Until: 22:00,            !- Field 24
1.0,                     !- Field 25
Until: 24:00,            !- Field 26
0.05,                    !- Field 27
For: Saturday,           !- Field 28
Until: 06:00,            !- Field 29
0.0,                     !- Field 30
Until: 08:00,            !- Field 31
0.1,                     !- Field 32
Until: 12:00,            !- Field 33
0.3,                     !- Field 34
Until: 17:00,            !- Field 35
0.1,                     !- Field 36
Until: 19:00,            !- Field 37
0.0,                     !- Field 38
Until: 24:00,            !- Field 39
0.0,                     !- Field 40
For: WinterDesignDay,    !- Field 41
Until: 24:00,            !- Field 42
0.0,                     !- Field 43
For: Sunday Holidays AllOtherDays,  !- Field 44
Until: 06:00,            !- Field 45
0.0,                     !- Field 46
Until: 18:00,            !- Field 47
0.0,                     !- Field 48
Until: 24:00,            !- Field 49
0.0;                     !- Field 50\n\n"

fh.puts "! Schedule Elevator\n\n"

fh.puts "Schedule:Compact,
    BLDG_ELEVATORS,          !- Name
Fraction,                !- Schedule Type Limits Name
Through: 12/31,          !- Field 1
For: Weekdays SummerDesignDay,  !- Field 2
Until: 07:00,            !- Field 3
0.0,                     !- Field 4
Until: 08:00,            !- Field 5
0.35,                    !- Field 6
Until: 09:00,            !- Field 7
0.69,                    !- Field 8
Until: 10:00,            !- Field 9
0.43,                    !- Field 10
Until: 11:00,            !- Field 11
0.37,                    !- Field 12
Until: 12:00,            !- Field 13
0.43,                    !- Field 14
Until: 13:00,            !- Field 15
0.58,                    !- Field 16
Until: 14:00,            !- Field 17
0.48,                    !- Field 18
Until: 15:00,            !- Field 19
0.37,                    !- Field 20
Until: 16:00,            !- Field 21
0.37,                    !- Field 22
Until: 17:00,            !- Field 23
0.46,                    !- Field 24
Until: 18:00,            !- Field 25
0.62,                    !- Field 26
Until: 19:00,            !- Field 27
0.12,                    !- Field 28
Until: 20:00,            !- Field 29
0.04,                    !- Field 30
Until: 21:00,            !- Field 31
0.04,                    !- Field 32
Until: 24:00,            !- Field 33
0.00,                    !- Field 34
For: Saturday WinterDesignDay,  !- Field 35
Until: 07:00,            !- Field 36
0.0,                     !- Field 37
Until: 08:00,            !- Field 38
0.16,                    !- Field 39
Until: 09:00,            !- Field 40
0.14,                    !- Field 41
Until: 10:00,            !- Field 42
0.21,                    !- Field 43
Until: 11:00,            !- Field 44
0.18,                    !- Field 45
Until: 12:00,            !- Field 46
0.25,                    !- Field 47
Until: 13:00,            !- Field 48
0.21,                    !- Field 49
Until: 14:00,            !- Field 50
0.13,                    !- Field 51
Until: 15:00,            !- Field 52
0.08,                    !- Field 53
Until: 16:00,            !- Field 54
0.04,                    !- Field 55
Until: 17:00,            !- Field 56
0.05,                    !- Field 57
Until: 18:00,            !- Field 58
0.06,                    !- Field 59
Until: 24:00,            !- Field 60
0.00,                    !- Field 61
For: Sunday Holidays AllOtherDays,  !- Field 62
Until: 24:00,            !- Field 63
0.0;                     !- Field 64\n\n"

fh.puts "Schedule:Compact,
    INFIL_SCH,               !- Name
fraction,                !- Schedule Type Limits Name
Through: 12/31,          !- Field 1
For: Weekdays SummerDesignDay,  !- Field 2
Until: 06:00,            !- Field 3
1.0,                     !- Field 4
Until: 22:00,            !- Field 5
0.0,                     !- Field 6
Until: 24:00,            !- Field 7
1.0,                     !- Field 8
For: Saturday WinterDesignDay,  !- Field 9
Until: 06:00,            !- Field 10
1.0,                     !- Field 11
Until: 18:00,            !- Field 12
0.0,                     !- Field 13
Until: 24:00,            !- Field 14
1.0,                     !- Field 15
For: Sunday Holidays AllOtherDays,  !- Field 16
Until: 24:00,            !- Field 17
1.0;                     !- Field 18\n\n"

fh.puts "Schedule:Compact,
    INFIL_HALF_ON_SCH,       !- Name
fraction,                !- Schedule Type Limits Name
Through: 12/31,          !- Field 1
For: Weekdays SummerDesignDay,  !- Field 2
Until: 06:00,            !- Field 3
1.0,                     !- Field 4
Until: 22:00,            !- Field 5
0.5,                     !- Field 6
Until: 24:00,            !- Field 7
1.0,                     !- Field 8
For: Saturday WinterDesignDay,  !- Field 9
Until: 06:00,            !- Field 10
1.0,                     !- Field 11
Until: 18:00,            !- Field 12
0.5,                     !- Field 13
Until: 24:00,            !- Field 14
1.0,                     !- Field 15
For: Sunday Holidays AllOtherDays,  !- Field 16
Until: 24:00,            !- Field 17
1.0;                     !- Field 18\n\n"

fh.puts "Schedule:Compact,
    INFIL_QUARTER_ON_SCH,    !- Name
fraction,                !- Schedule Type Limits Name
Through: 12/31,          !- Field 1
For: Weekdays SummerDesignDay,  !- Field 2
Until: 06:00,            !- Field 3
1.0,                     !- Field 4
Until: 22:00,            !- Field 5
0.25,                    !- Field 6
Until: 24:00,            !- Field 7
1.0,                     !- Field 8
For: Saturday WinterDesignDay,  !- Field 9
Until: 06:00,            !- Field 10
1.0,                     !- Field 11
Until: 18:00,            !- Field 12
0.25,                    !- Field 13
Until: 24:00,            !- Field 14
1.0,                     !- Field 15
For: Sunday Holidays AllOtherDays,  !- Field 16
Until: 24:00,            !- Field 17
1.0;                     !- Field 18\n\n"

fh.puts "! Schedule Office Service Water Heating, ASHRAE 90.1-1989, Section 13\n\n"

fh.puts "Schedule:Compact,
    BLDG_SWH_SCH,            !- Name
Fraction,                !- Schedule Type Limits Name
Through: 12/31,          !- Field 1
For: Weekdays SummerDesignDay,  !- Field 2
Until: 05:00,            !- Field 3
0.05,                    !- Field 4
Until: 06:00,            !- Field 5
0.08,                    !- Field 6
Until: 07:00,            !- Field 7
0.07,                    !- Field 8
Until: 08:00,            !- Field 9
0.19,                    !- Field 10
Until: 09:00,            !- Field 11
0.35,                    !- Field 12
Until: 10:00,            !- Field 13
0.38,                    !- Field 14
Until: 11:00,            !- Field 15
0.39,                    !- Field 16
Until: 12:00,            !- Field 17
0.47,                    !- Field 18
Until: 13:00,            !- Field 19
0.57,                    !- Field 20
Until: 14:00,            !- Field 21
0.54,                    !- Field 22
Until: 15:00,            !- Field 23
0.34,                    !- Field 24
Until: 16:00,            !- Field 25
0.33,                    !- Field 26
Until: 17:00,            !- Field 27
0.44,                    !- Field 28
Until: 18:00,            !- Field 29
0.26,                    !- Field 30
Until: 19:00,            !- Field 31
0.21,                    !- Field 32
Until: 20:00,            !- Field 33
0.15,                    !- Field 34
Until: 21:00,            !- Field 35
0.17,                    !- Field 36
Until: 22:00,            !- Field 37
0.08,                    !- Field 38
Until: 24:00,            !- Field 39
0.05,                    !- Field 40
For: Saturday WinterDesignDay,  !- Field 41
Until: 05:00,            !- Field 42
0.05,                    !- Field 43
Until: 06:00,            !- Field 44
0.08,                    !- Field 45
Until: 07:00,            !- Field 46
0.07,                    !- Field 47
Until: 08:00,            !- Field 48
0.11,                    !- Field 49
Until: 09:00,            !- Field 50
0.15,                    !- Field 51
Until: 10:00,            !- Field 52
0.21,                    !- Field 53
Until: 11:00,            !- Field 54
0.19,                    !- Field 55
Until: 12:00,            !- Field 56
0.23,                    !- Field 57
Until: 13:00,            !- Field 58
0.20,                    !- Field 59
Until: 14:00,            !- Field 60
0.19,                    !- Field 61
Until: 15:00,            !- Field 62
0.15,                    !- Field 63
Until: 16:00,            !- Field 64
0.13,                    !- Field 65
Until: 17:00,            !- Field 66
0.14,                    !- Field 67
Until: 21:00,            !- Field 68
0.07,                    !- Field 69
Until: 22:00,            !- Field 70
0.09,                    !- Field 71
Until: 24:00,            !- Field 72
0.05,                    !- Field 73
For: Sunday Holidays AllOtherDays,  !- Field 74
Until: 05:00,            !- Field 75
0.04,                    !- Field 76
Until: 06:00,            !- Field 77
0.07,                    !- Field 78
Until: 11:00,            !- Field 79
0.04,                    !- Field 80
Until: 13:00,            !- Field 81
0.06,                    !- Field 82
Until: 14:00,            !- Field 83
0.09,                    !- Field 84
Until: 15:00,            !- Field 85
0.06,                    !- Field 86
Until: 21:00,            !- Field 87
0.04,                    !- Field 88
Until: 22:00,            !- Field 89
0.07,                    !- Field 90
Until: 24:00,            !- Field 91
0.04;                    !- Field 92\n\n"

fh.puts "Schedule:Compact,
    Hours_of_operation,      !- Name
on/off,                  !- Schedule Type Limits Name
Through: 12/31,          !- Field 1
For: Weekdays SummerDesignDay,  !- Field 2
Until: 06:00,            !- Field 3
0.0,                     !- Field 4
Until: 22:00,            !- Field 5
1.0,                     !- Field 6
Until: 24:00,            !- Field 7
0.0,                     !- Field 8
For: Saturday WinterDesignDay,  !- Field 9
Until: 06:00,            !- Field 10
0.0,                     !- Field 11
Until: 18:00,            !- Field 12
1.0,                     !- Field 13
Until: 24:00,            !- Field 14
0.0,                     !- Field 15
For: Sunday Holidays AllOtherDays,  !- Field 16
Until: 24:00,            !- Field 17
0.0;                     !- Field 18\n\n"

fh.puts "Schedule:Compact,
    ALWAYS_ON,               !- Name
Fraction,                !- Schedule Type Limits Name
Through: 12/31,          !- Field 1
For: AllDays,            !- Field 2
Until: 24:00,            !- Field 3
1.0;                     !- Field 4\n\n"

fh.puts "Schedule:Compact,
    ALWAYS_OFF,              !- Name
Fraction,                !- Schedule Type Limits Name
Through: 12/31,          !- Field 1
For: AllDays,            !- Field 2
Until: 24:00,            !- Field 3
0.0;                     !- Field 4\n\n"

fh.puts "! Schedule Office HVAC Systems, ASHRAE 90.1-1989, Section 13\n\n"
fh.puts "!  Equivalent Full-Load Hours: Weekdays 16, Saturday 12, Sunday/Holidays 0\n\n"

fh.puts "Schedule:Compact,
    HVACOperationSchd,       !- Name
on/off,                  !- Schedule Type Limits Name
Through: 12/31,          !- Field 1
For: Weekdays SummerDesignDay,  !- Field 2
Until: 06:00,            !- Field 3
0.0,                     !- Field 4
Until: 22:00,            !- Field 5
1.0,                     !- Field 6
Until: 24:00,            !- Field 7
0.0,                     !- Field 8
For: Saturday WinterDesignDay,  !- Field 9
Until: 06:00,            !- Field 10
0.0,                     !- Field 11
Until: 18:00,            !- Field 12
1.0,                     !- Field 13
Until: 24:00,            !- Field 14
0.0,                     !- Field 15
For: Sunday Holidays AllOtherDays,  !- Field 16
Until: 24:00,            !- Field 17
0.0;                     !- Field 18\n\n"

fh.puts "Schedule:Compact,
    PlantOnSched,            !- Name
On/Off,                  !- Schedule Type Limits Name
Through: 12/31,          !- Field 1
For: AllDays,            !- Field 2
Until: 24:00,            !- Field 3
1.0;                     !- Field 4\n\n"

fh.puts "Schedule:Compact,
    FAN_SCH,                 !- Name
Fraction,                !- Schedule Type Limits Name
Through: 12/31,          !- Field 1
For: AllDays,            !- Field 2
Until: 24:00,            !- Field 3
1.0;                     !- Field 4\n\n"

fh.puts "Schedule:Compact,
    ReheatCoilAvailSched,    !- Name
Fraction,                !- Schedule Type Limits Name
Through: 12/31,          !- Field 1
For: AllDays,            !- Field 2
Until: 24:00,            !- Field 3
1.0;                     !- Field 4\n\n"

fh.puts "Schedule:Compact,
    CoolingCoilAvailSched,   !- Name
Fraction,                !- Schedule Type Limits Name
Through: 12/31,          !- Field 1
For: AllDays,            !- Field 2
Until: 24:00,            !- Field 3
1.0;                     !- Field 4\n\n"

fh.puts "Schedule:Compact,
    HTGSETP_SCH,             !- Name
Temperature,             !- Schedule Type Limits Name
Through: 12/31,          !- Field 1
For: Weekdays WinterDesignDay,  !- Field 2
Until: 05:00,            !- Field 3
15.6,                    !- Field 4
Until: 19:00,            !- Field 5
21.0,                    !- Field 6
Until: 24:00,            !- Field 7
13.,                     !- Field 8
For SummerDesignDay,     !- Field 9
Until: 24:00,            !- Field 10
15.6,                    !- Field 11
For: Saturday,           !- Field 12
Until: 06:00,            !- Field 13
15.6,                    !- Field 14
Until: 17:00,            !- Field 15
21.0,                    !- Field 16
Until: 24:00,            !- Field 17
15.6,                    !- Field 18
For: Sunday Holidays AllOtherDays,  !- Field 19
Until: 24:00,            !- Field 20
15.6;                    !- Field 21\n\n"

fh.puts "Schedule:Compact,
    CLGSETP_SCH,             !- Name
Temperature,             !- Schedule Type Limits Name
Through: 12/31,          !- Field 1
For: Weekdays SummerDesignDay,  !- Field 2
Until: 06:00,            !- Field 3
30.0,                    !- Field 4
Until: 22:00,            !- Field 5
24.0,                    !- Field 6
Until: 24:00,            !- Field 7
30.0,                    !- Field 8
For: Saturday,           !- Field 9
Until: 06:00,            !- Field 10
30.0,                    !- Field 11
Until: 18:00,            !- Field 12
24.0,                    !- Field 13
Until: 24:00,            !- Field 14
30.0,                    !- Field 15
For WinterDesignDay,     !- Field 16
Until: 24:00,            !- Field 17
30.0,                    !- Field 18
For: Sunday Holidays AllOtherDays,  !- Field 19
Until: 24:00,            !- Field 20
30.0;                    !- Field 21\n\n"

fh.puts "Schedule:Compact,
    Humidity Setpoint Schedule,  !- Name
Humidity,                !- Schedule Type Limits Name
Through: 12/31,          !- Field 1
For: Weekdays SummerDesignDay,  !- Field 2
Until: 24:00,            !- Field 3
50,                      !- Field 4
For: Saturday WinterDesignDay,  !- Field 5
Until: 24:00,            !- Field 6
50,                      !- Field 7
For: Sunday Holidays AllOtherDays,  !- Field 8
Until: 24:00,            !- Field 9
50;                      !- Field 10\n\n"

fh.puts "Schedule:Compact,
    MinOA_MotorizedDamper_Sched,  !- Name
fraction,                !- Schedule Type Limits Name
Through: 12/31,          !- Field 1
For: Weekdays SummerDesignDay,  !- Field 2
Until: 07:00,            !- Field 3
0.0,                     !- Field 4
Until: 22:00,            !- Field 5
1.0,                     !- Field 6
Until: 24:00,            !- Field 7
0.0,                     !- Field 8
For: Saturday WinterDesignDay,  !- Field 9
Until: 07:00,            !- Field 10
0.0,                     !- Field 11
Until: 18:00,            !- Field 12
1.0,                     !- Field 13
Until: 24:00,            !- Field 14
0.0,                     !- Field 15
For: Sunday Holidays AllOtherDays,  !- Field 16
Until: 24:00,            !- Field 17
0.0;                     !- Field 18\n\n"

fh.puts "Schedule:Compact,
    MinOA_Sched,             !- Name
fraction,                !- Schedule Type Limits Name
Through: 12/31,          !- Field 1
For: AllDays,            !- Field 2
Until: 24:00,            !- Field 3
1.0;                     !- Field 4\n\n"

fh.puts "Schedule:Compact,
    Dual Zone Control Type Sched,  !- Name
Control Type,            !- Schedule Type Limits Name
Through: 12/31,          !- Field 1
For: AllDays,            !- Field 2
Until: 24:00,            !- Field 3
4;                       !- Field 4\n\n"

fh.puts "Schedule:Compact,
    Seasonal-Reset-Supply-Air-Temp-Sch,  !- Name
Temperature,             !- Schedule Type Limits Name
Through: 3/31,           !- Field 1
For: AllDays,            !- Field 2
Until: 24:00,            !- Field 3
13.0,                    !- Field 4
Through: 9/30,           !- Field 5
For: AllDays,            !- Field 6
Until: 24:00,            !- Field 7
13.0,                    !- Field 8
Through: 12/31,          !- Field 9
For: AllDays,            !- Field 10
Until: 24:00,            !- Field 11
13.0;                    !- Field 12\n\n"

fh.puts "Schedule:Compact,
    CW-Loop-Temp-Schedule,   !- Name
Temperature,             !- Schedule Type Limits Name
Through: 12/31,          !- Field 1
For: AllDays,            !- Field 2
Until: 24:00,            !- Field 3
6.7;                     !- Field 4\n\n"

fh.puts "Schedule:Compact,
    HW-Loop-Temp-Schedule,   !- Name
Temperature,             !- Schedule Type Limits Name
Through: 12/31,          !- Field 1
For: AllDays,            !- Field 2
Until: 24:00,            !- Field 3
60.;                     !- Field 4\n\n"

fh.puts "Schedule:Compact,
    Heating-Supply-Air-Temp-Sch,  !- Name
Temperature,             !- Schedule Type Limits Name
Through: 12/31,          !- Field 1
For: AllDays,            !- Field 2
Until: 24:00,            !- Field 3
16.0;                    !- Field 4\n\n"

fh.puts "Schedule:Compact,
    ACTIVITY_SCH,            !- Name
Any Number,              !- Schedule Type Limits Name
Through: 12/31,          !- Field 1
For: AllDays,            !- Field 2
Until: 24:00,            !- Field 3
120.;                    !- Field 4\n\n"

fh.puts "Schedule:Compact,
    WORK_EFF_SCH,            !- Name
Fraction,                !- Schedule Type Limits Name
Through: 12/31,          !- Field 1
For: AllDays,            !- Field 2
Until: 24:00,            !- Field 3
0.0;                     !- Field 4\n\n"

fh.puts "Schedule:Compact,
    AIR_VELO_SCH,            !- Name
Any Number,              !- Schedule Type Limits Name
Through: 12/31,          !- Field 1
For: AllDays,            !- Field 2
Until: 24:00,            !- Field 3
0.2;                     !- Field 4\n\n"

fh.puts "Schedule:Compact,
    CLOTHING_SCH,            !- Name
Any Number,              !- Schedule Type Limits Name
Through: 04/30,          !- Field 1
For: AllDays,            !- Field 2
Until: 24:00,            !- Field 3
1.0,                     !- Field 4
Through: 09/30,          !- Field 5
For: AllDays,            !- Field 6
Until: 24:00,            !- Field 7
0.5,                     !- Field 8
Through: 12/31,          !- Field 9
For: AllDays,            !- Field 10
Until: 24:00,            !- Field 11
1.0;                     !- Field 12\n\n"

fh.puts "Schedule:Compact,
    SHADING_SCH,             !- Name
Any Number,              !- Schedule Type Limits Name
Through: 12/31,          !- Field 1
For: AllDays,            !- Field 2
Until: 24:00,            !- Field 3
0.0;                     !- Field 4\n\n"



  end
end