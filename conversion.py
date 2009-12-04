# -*- coding: utf-8 -*-
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

#!     m                      =>   ft                  3.281
#!     W                      =>   Btu/h               3.412
#!     m3/s                   =>   ft3/min             2118.6438
#!     C                      =>   F                   1.8 (plus 32)
#!     kg/J                   =>   lb/Btu              2325.83774250441
#!     Pa                     =>   psi                 0.0001450377
#!     W/m-K                  =>   Btu-in/h-ft2-F      6.93481276005548
#!     W/K                    =>   Btu/h-F             1.8987
#!     deltaC                 =>   deltaF              1.8
#!     m2                     =>   ft2                 10.764961
#!     K                      =>   R                   1.8
#!     1/K                    =>   1/R                 0.555555556
#!     (kg/s)/W               =>   (lbm/sec)/(Btu/hr)  0.646078115385742
#!     J/kg                   =>   Btu/lb              0.00042986 (plus 7.686)
#!     kg-H2O/kg-air          =>   lb-H2O/lb-air       1
#!     kJ/kg                  =>   Btu/lb              0.429925
#!     lux                    =>   foot-candles        0.092902267
#!     kg/m3                  =>   lb/ft3              0.062428
#!     kg/s                   =>   lb/s                2.2046
#!     kg/s-m                 =>   lb/s-ft             0.67194
#!     m3                     =>   ft3                 35.319837041
#!     m3                     =>   gal                 264.172
#!     W/m2-K                 =>   Btu/h-ft2-F         0.176110194261872
#!     1/m                    =>   1/ft                0.304785126485827
#!     J/kg-K                 =>   Btu/lb-F            0.000239005736137667
#!     J/m3-K                 =>   Btu/ft3-F           1.49237004739337E-05
#!     m/s                    =>   ft/min              196.86
#!     m/s                    =>   miles/hr            2.2369
#!     m2-K/W                 =>   ft2-F-hr/Btu        5.678263
#!     W/m2                   =>   Btu/h-ft2           0.316957210776545
#!     A/K                    =>   A/F                 0.555555555555556
#!     g/kg                   =>   grains/lb           7.00000
#!     g/m-s                  =>   lb/ft-s             0.000671968949659
#!     g/m-s-K                =>   lb/ft-s-F           0.000373574867724868
#!     J/K                    =>   Btu/F               0.000526917584820558
#!     J/kg-K2                =>   Btu/lb-F2           0.000132889924714692
#!     J/m3                   =>   Btu/ft3             2.68096514745308E-05
#!     kg/kg-K                =>   lb/lb-F             0.555555555555556
#!     kPa                    =>   psi                 0.145038
#!     kPa                    =>   inHg                0.29523
#!     m2/s                   =>   ft2/s               10.764961
#!     m3/kg                  =>   ft3/lb              16.018
#!     m3/m3                  =>   ft3/ft3             1
    #J/m2-K                 =>   Btu/ft2-F           4.89224766847393E-05
#!     cycles/hr              =>   cycles/hr           1
#!     kg/kg                  =>   lb/lb               1
#!     J/J                    =>   Btu/Btu             1
#!     g/GJ                   =>   lb/MWh              0.00793664091373665
#!     L/GJ                   =>   gal/kWh             0.000951022349025202
#!     m3/GJ                  =>   ft3/MWh             127.13292
#!     m3/s-m2                =>   ft3/min-ft2         196.85
#!     m3/s-person            =>   ft3/min-person      2118.6438
#!     W/m2-K2                =>   Btu/h-ft2-F2        0.097826
#!     g/MJ                   =>   lb/MWh              7.93664091373665
#!     L/MJ                   =>   gal/kWh             0.951022349025202
#!     m3/MJ                  =>   ft3/kWh             127.13292
#!     W/W                    =>   Btuh/Btuh           1
#!     $/m2                   =>   $/ft2               0.0928939733269818
#!     $                      =>   $                   1
#!     $/kW                   =>   $/(kBtuh/h)         0.293083235638921
#!     $/m3                   =>   $/ft3               0.0283127014102352
#!     years                  =>   years               1
#!     $/(W/K)                =>   $/(Btu/h-F)         0.52667614683731
#!     $/(m3/s)               =>   $/(ft3/min)         0.000472000059660808
#!     W/m                    =>   Btu/h-ft            1.04072
#!     K/m                    =>   F/ft                0.54861322767449
#!     W/s                    =>   W/s                 1
#!     kmol                   =>   kmol                1
#!     J                      =>   Wh                  0.000277777777777778
#!     GJ                     =>   ton-hrs             78.9889415481832
#!     kg/m2                  =>   lb/ft2              0.204794053596664
#!     kg                     =>   lb                  2.2046
#!     percent/K              =>   percent/F           0.555555555555556
#!     kg/s2                  =>   lb/s2               2.2046
#!     g/mol                  =>   lb/mol              0.0022046
#!     deltaJ/kg              =>   deltaBtu/lb         0.0004299
#!     person/m2              =>   person/ft2          0.0928939733269818
#!     m2/person              =>   ft2/person          10.764961
#!     W/person               =>   Btu/h-person        3.412
#!     m3/person              =>   ft3/person          35.319837041
#!     m3/hr-person           =>   ft3/hr-person       35.319837041
#!     m3/m2                  =>   ft3/ft2             3.281
#!     m3/hr-m2               =>   ft3/hr-ft2          3.281
#!     m3/hr                  =>   ft3/hr              35.319837041
#!     s/m                    =>   s/ft                0.304785126485827
#!     m2/m                   =>   ft2/ft              3.281
#!     L/day                  =>   pint/day            2.11337629827348
#!     L/kWh                  =>   pint/kWh            2.11337629827348
#!     kg/Pa-s-m2             =>   lb/psi-s-ft2        1412.00523459398
#!
#! Other conversions supported (needs the \ip-units code)
#!
#!     m                      =>   in                  39.37
#!     W                      =>   W                   1
#!     m3/s                   =>   gal/min             15852
#!     m3/s                   =>   lbH2O/hr            7936289.998
#!     Pa                     =>   inHg                0.00029613
#!     Pa                     =>   inH2O               0.00401463
#!     Pa                     =>   ftH2O               0.00033455
#!     W/person               =>   W/person            1
#!     W/m2                   =>   W/m2                1
#!     W/m2                   =>   W/ft2               0.0928939733269818
#!
#! Units fields that are not translated
#!     deg
#!     hr
#!     A
#!     dimensionless
#!     V
#!     ohms
#!     A/V
#!     eV
#!     percent
#!     s
#!     W/m2 or deg C
#!     W/m2, W or deg C
#!     minutes
#! **************************************************************************

  
  
conversionvalues = {'m':('ft',3.281),\
                     'W':('Btu/h',3.412),\
                     'm3/s':('ft3/min',2118.6438),\
                     'C':('F',1.8,+32),\
                     'deg':('F',1.8,+32),\
                     'kg/J':('lb/Btu',2325.83774250441),\
                     'Pa':('psi',0.0001450377),\
                     'W/m-K':('Btu-in/h-ft2-F',6.93481276005548),\
                     'W/K':('Btu/h-F',1.8987),\
                     'deltaC':('deltaF',1.8),\
                     'm2':('ft2',10.764961),\
                     'K':('R',1.8),\
                     '1/K':('1/R',0.555555556),\
                     '(kg/s)/W':('(lbm/sec)/(Btu/hr)',0.646078115385742),\
                     'J/kg':('Btu/lb',0.00042986,-7.686),\
                     'kg-H2O/kg-air':('lb-H2O/lb-air',1),\
                     'kJ/kg':('Btu/lb',0.429925),\
                     'lux':('foot-candles',0.092902267),\
                     'kg/m3':('lb/ft3',0.062428),\
                     'kg/s':('lb/s',2.2046),\
                     'kg/s-m':('lb/s-ft',0.67194),\
                     'm3':('ft3',35.319837041),\
                     'm3':('gal',264.172),\
                     'W/m2-K':('Btu/h-ft2-F',0.176110194261872),\
                     '1/m':('1/ft',0.304785126485827),\
                     'J/kg-K':('Btu/lb-F',0.000239005736137667),\
                     'J/m3-K':('Btu/ft3-F',1.49237004739337E-05),\
                     'm/s':('ft/min',196.86),\
                     'm/s':('miles/hr',2.2369),\
                     'm2-K/W':('ft2-F-hr/Btu',5.678263),\
                     'W/m2':('Btu/h-ft2',0.316957210776545),\
                     'A/K':('A/F',0.555555555555556),\
                     'g/kg':('grains/lb',7.00000),\
                     'g/m-s':('lb/ft-s',0.000671968949659),\
                     'g/m-s-K':('lb/ft-s-F',0.000373574867724868),\
                     'J/K':('Btu/F',0.000526917584820558),\
                     'J/kg-K2':('Btu/lb-F2',0.000132889924714692),\
                     'J/m3':('Btu/ft3',2.68096514745308E-05),\
                     'kg/kg-K':('lb/lb-F',0.555555555555556),\
                     'kPa':('psi',0.145038),\
                     'kPa':('inHg',0.29523),\
                     'm2/s':('ft2/s',10.764961),\
                     'm3/kg':('ft3/lb',16.018),\
                     'm3/m3':('ft3/ft3',1),\
                     'J/m2-K':('Btu/ft2-F',4.89224766847393E-05),\
                     'cycles/hr':('cycles/hr',1),\
                     'kg/kg':('lb/lb',1),\
                     'J/J':('Btu/Btu',1),\
                     'g/GJ':('lb/MWh',0.00793664091373665),\
                     'L/GJ':('gal/kWh',0.000951022349025202),\
                     'm3/GJ':('ft3/MWh',127.13292),\
                     'm3/s-m2':('ft3/min-ft2',196.85),\
                     'm3/s-person':('ft3/min-person',2118.6438),\
                     'W/m2-K2':('Btu/h-ft2-F2',0.097826),\
                     'g/MJ':('lb/MWh',7.93664091373665),\
                     'L/MJ':('gal/kWh',0.951022349025202),\
                     'm3/MJ':('ft3/kWh',127.13292),\
                     'W/W':('Btuh/Btuh',1),\
                     '$/m2':('$/ft2',0.0928939733269818),\
                     '$':('$',1),\
                     '$/kW':('$/(kBtuh/h)',0.293083235638921),\
                     '$/m3':('$/ft3',0.0283127014102352),\
                     'years':('years',1),\
                     '$/(W/K)':('$/(Btu/h-F)',0.52667614683731),\
                     '$/(m3/s)':('$/(ft3/min)',0.000472000059660808),\
                     'W/m':('Btu/h-ft',1.04072),\
                     'K/m':('F/ft',0.54861322767449),\
                     'W/s':('W/s',1),\
                     'kmol':('kmol',1),\
                     'J':('Wh',0.000277777777777778),\
                     'GJ':('ton-hrs',78.9889415481832),\
                     'kg/m2':('lb/ft2',0.204794053596664),\
                     'kg':('lb',2.2046),\
                     'percent/K':('percent/F',0.555555555555556),\
                     'kg/s2':('lb/s2',2.2046),\
                     'g/mol':('lb/mol',0.0022046),\
                     'deltaJ/kg':('deltaBtu/lb',0.0004299),\
                     'person/m2':('person/ft2',0.0928939733269818),\
                     'm2/person':('ft2/person',10.764961),\
                     'W/person':('Btu/h-person',3.412),\
                     'm3/person':('ft3/person',35.319837041),\
                     'm3/hr-person':('ft3/hr-person',35.319837041),\
                     'm3/m2':('ft3/ft2',3.281),\
                     'm3/hr-m2':('ft3/hr-ft2',3.281),\
                     'm3/hr':('ft3/hr',35.319837041),\
                     's/m':('s/ft',0.304785126485827),\
                     'm2/m':('ft2/ft',3.281),\
                     'L/day':('pint/day',2.11337629827348),\
                     'L/kWh':('pint/kWh',2.11337629827348),\
                     'kg/Pa-s-m2':('lb/psi-s-ft2',1412.00523459398)}
#!
#! Other conversions supported (needs the \ip-units code)
#!
#!     m                      =>   in                  39.37
#!     W                      =>   W                   1
#!     m3/s                   =>   gal/min             15852
#!     m3/s                   =>   lbH2O/hr            7936289.998
#!     Pa                     =>   inHg                0.00029613
#!     Pa                     =>   inH2O               0.00401463
#!     Pa                     =>   ftH2O               0.00033455
#!     W/person               =>   W/person            1
#!     W/m2                   =>   W/m2                1
#!     W/m2                   =>   W/ft2               0.0928939733269818
#!

def convertTo(unit,value):
    #returns unit,value list.
    #unit must be SI unit, value SI
    #unit returned is the IP name and converted value
    if unit == '':
        return unit,value
    if unit in conversionvalues:
        if len(conversionvalues[unit]) == 3:
            val = value / conversionvalues[unit][1] + conversionvalues[unit][2]
            return conversionvalues[unit][0],val
            
        else:
            return conversionvalues[unit][0],value / conversionvalues[unit][1]
            
    else:
        print 'convertTo: invalid unit input',unit
        return 'error',0

def convertFrom(unit,value):
    #returns unit,value list
    #unit must be SI, value in IP
    #unit returned is SI and SI converted value
    if unit in conversionvalues:
        if len(conversionvalues[unit]) == 3:
            val = (value - conversionvalues[unit][2]) * conversionvalues[unit][1] 
            return unit,val
            
        else:
            return unit,value * conversionvalues[unit][1]
            
    else:
        print 'convertFrom: invalid unit input',unit
        return 'error',0

def convertable(value):
    #verify type, whether int, real or a numerical value
    print 'convertable',type(value)
    return (type(value) == 'int') or (type(value) == 'real')
    

if __name__ == "__main__":
    print convertTo('deg',30)
    print convertFrom('deg',30)
#deg 30.                                                                                                           
#deltaC 0.4                                                                                                        
#deg 33.90                                                                                                         
#deg -118.50                                                                                                       
#hr -8.00                                                                                                          
#m 30.00                                                                                                           
#C 7.40                                                                                                            
#deltaC 0.00                                                                                                       
#Pa 100941.                                                                                                        
#m/s 2.80                                                                                                          
#deg 70.00                                                                                                         
#C 27.00                                                                                                           
#deltaC 6.10                                                                                                       
#Pa 100941.                                                                                                        
#m/s 4.40                                                                                                          
#deg 250.00                                                                                                        
#C 20.03                                                                                                           
#m 0.667                                                                                                           
#W/m-K 0.115                                                                                                       
#kg/m3 513                                                                                                         
#J/kg-K 1381                                                                                                       
#m 1.2700000E-02                                                                                                   
#W/m-K 1.442000                                                                                                    
#kg/m3 881.0000                                                                                                    
#J/kg-K 1674.000                                                                                                   
#m 9.4999997E-03                                                                                                   
#W/m-K 0.1620000                                                                                                   
#kg/m3 1121.000                                                                                                    
#J/kg-K 1464.000                                                                                                   
#m 7.6200001E-02                                                                                                   
#W/m-K 2.3000000E-02                                                                                               
#kg/m3 24.00000                                                                                                    
#J/kg-K 1590.000                                                                                                   
#m 1.9099999E-02                                                                                                   
#W/m-K 0.1150000                                                                                                   
#kg/m3 513.0000                                                                                                    
#J/kg-K 1381.000                                                                                                   
#m 1.2700000E-02                                                                                                   
#W/m-K 0.1150000                                                                                                   
#kg/m3 545.0000                                                                                                    
#J/kg-K 1213.000                                                                                                   
#m 9.0099998E-02                                                                                                   
#W/m-K 4.3000001E-02                                                                                               
#kg/m3 10.00000                                                                                                    
#J/kg-K 837.0000                                                                                                   
#m 1.2700000E-02                                                                                                   
#W/m-K 0.1600000                                                                                                   
#kg/m3 801.0000                                                                                                    
#J/kg-K 837.0000                                                                                                   
#m 1.5900001E-02                                                                                                   
#W/m-K 0.1600000                                                                                                   
#kg/m3 801.0000                                                                                                    
#J/kg-K 837.0000                                                                                                   
#m 0.1016000                                                                                                       
#W/m-K 1.310000                                                                                                    
#kg/m3 2243.000                                                                                                    
#J/kg-K 837.0000                                                                                                   
#m2-K/W 0.3670000                                                                                                  
#m2-K/W 0.117406666                                                                                                
#m2-K/W 0.652259290                                                                                                
#m2-K/W 3.522199631                                                                                                
#m2-K/W 0.1570000                                                                                                  
#m2-K/W 0.1530000                                                                                                  
#m 0.0063                                                                                                          
#m 0.0127                                                                                                          
#m 0.0127                                                                                                          
#m 0.003                                                                                                           
#W/m-K 0.9                                                                                                         
#m 0.003                                                                                                           
#W/m-K 0.9                                                                                                         
#m 0.006                                                                                                           
#W/m-K 0.9                                                                                                         
#m 0.006                                                                                                           
#W/m-K 0.9                                                                                                         
#deg 0                                                                                                             
#m 0.609600067                                                                                                     
#m3 283.2                                                                                                          
#m 3.0                                                                                                             
#m 0.0                                                                                                             
#m 0.0                                                                                                             
#m 2.4                                                                                                             
#m 30.5                                                                                                            
#m 0.0                                                                                                             
#m 2.4                                                                                                             
#m 30.5                                                                                                            
#m 0.0                                                                                                             
#m 3.0                                                                                                             
#m 30.5                                                                                                            
#m 0.0                                                                                                             
#m 3.0                                                                                                             
#m 30.5                                                                                                            
#m 0.0                                                                                                             
#m 2.4                                                                                                             
#m 30.5                                                                                                            
#m 15.2                                                                                                            
#m 2.4                                                                                                             
#m 30.5                                                                                                            
#m 15.2                                                                                                            
#m 3.0                                                                                                             
#m 30.5                                                                                                            
#m 15.2                                                                                                            
#m 3.0                                                                                                             
#m 30.5                                                                                                            
#m 15.2                                                                                                            
#m 2.4                                                                                                             
#m 0.0                                                                                                             
#m 15.2                                                                                                            
#m 2.4                                                                                                             
#m 0.0                                                                                                             
#m 15.2                                                                                                            
#m 3.0                                                                                                             
#m 0.0                                                                                                             
#m 15.2                                                                                                            
#m 3.0                                                                                                             
#m 0.0                                                                                                             
#m 15.2                                                                                                            
#m 2.4                                                                                                             
#m 0.0                                                                                                             
#m 0.0                                                                                                             
#m 2.4                                                                                                             
#m 0.0                                                                                                             
#m 0.0                                                                                                             
#m 3.0                                                                                                             
#m 0.0                                                                                                             
#m 15.2                                                                                                            
#m 3.0                                                                                                             
#m 0.0                                                                                                             
#m 0.0                                                                                                             
#m 3.0                                                                                                             
#m 30.5                                                                                                            
#m 0.0                                                                                                             
#m 3.0                                                                                                             
#m 30.5                                                                                                            
#m 15.2                                                                                                            
#m 3.0                                                                                                             
#m 26.8                                                                                                            
#m 3.7                                                                                                             
#m 2.4                                                                                                             
#m 30.5                                                                                                            
#m 0.0                                                                                                             
#m 2.4                                                                                                             
#m 0.0                                                                                                             
#m 0.0                                                                                                             
#m 2.4                                                                                                             
#m 3.7                                                                                                             
#m 3.7                                                                                                             
#m 2.4                                                                                                             
#m 26.8                                                                                                            
#m 11.6                                                                                                            
#m 2.4                                                                                                             
#m 30.5                                                                                                            
#m 15.2                                                                                                            
#m 2.4                                                                                                             
#m 30.5                                                                                                            
#m 0.0                                                                                                             
#m 2.4                                                                                                             
#m 26.8                                                                                                            
#m 3.7                                                                                                             
#m 2.4                                                                                                             
#m 26.8                                                                                                            
#m 11.6                                                                                                            
#m 2.4                                                                                                             
#m 3.7                                                                                                             
#m 11.6                                                                                                            
#m 2.4                                                                                                             
#m 0.0                                                                                                             
#m 15.2                                                                                                            
#m 2.4                                                                                                             
#m 30.5                                                                                                            
#m 15.2                                                                                                            
#m 2.4                                                                                                             
#m 3.7                                                                                                             
#m 3.7                                                                                                             
#m 2.4                                                                                                             
#m 0.0                                                                                                             
#m 0.0                                                                                                             
#m 2.4                                                                                                             
#m 0.0                                                                                                             
#m 15.2                                                                                                            
#m 2.4                                                                                                             
#m 3.7                                                                                                             
#m 11.6                                                                                                            
#m 2.4                                                                                                             
#m 26.8                                                                                                            
#m 11.6                                                                                                            
#m 2.4                                                                                                             
#m 26.8                                                                                                            
#m 3.7                                                                                                             
#m 2.4                                                                                                             
#m 3.7                                                                                                             
#m 3.7                                                                                                             
#m 2.4                                                                                                             
#m 3.7                                                                                                             
#m 11.6                                                                                                            
#m 2.4                                                                                                             
#deg 0                                                                                                             
#m 0                                                                                                               
#m 0                                                                                                               
#m 0                                                                                                               
#m 2.438400269                                                                                                     
#m3 239.247360229                                                                                                  
#m3/s 0.0167                                                                                                       
#W 1584                                                                                                            
#1/K None                                                                                                          
#W 1056                                                                                                            
#m 0.0                                                                                                             
#m 0.0                                                                                                             
#m 2.4                                                                                                             
#m 0.0                                                                                                             
#m 0.0                                                                                                             
#m 0.0                                                                                                             
#m 30.5                                                                                                            
#m 0.0                                                                                                             
#m 0.0                                                                                                             
#m 30.5                                                                                                            
#m 0.0                                                                                                             
#m 2.4                                                                                                             
#m 3.0                                                                                                             
#m 0.0                                                                                                             
#m 2.1                                                                                                             
#m 3.0                                                                                                             
#m 0.0                                                                                                             
#m 0.9                                                                                                             
#m 16.8                                                                                                            
#m 0.0                                                                                                             
#m 0.9                                                                                                             
#m 16.8                                                                                                            
#m 0.0                                                                                                             
#m 2.1                                                                                                             
#m 21.3                                                                                                            
#m 0.0                                                                                                             
#m 2.1                                                                                                             
#m 21.3                                                                                                            
#m 0.0                                                                                                             
#m 0.0                                                                                                             
#m 23.8                                                                                                            
#m 0.0                                                                                                             
#m 0.0                                                                                                             
#m 23.8                                                                                                            
#m 0.0                                                                                                             
#m 2.1                                                                                                             
#m 0.0                                                                                                             
#m -1.3                                                                                                            
#m 2.2                                                                                                             
#m 0.0                                                                                                             
#m 0.0                                                                                                             
#m 2.2                                                                                                             
#m 19.8                                                                                                            
#m 0.0                                                                                                             
#m 2.2                                                                                                             
#m 19.8                                                                                                            
#m -1.3                                                                                                            
#m 2.2                                                                                                             
#m 21.0                                                                                                            
#m -2.0                                                                                                            
#m 2.6                                                                                                             
#m 21.0                                                                                                            
#m 0.0                                                                                                             
#m 2.6                                                                                                             
#m 24.1                                                                                                            
#m 0.0                                                                                                             
#m 2.6                                                                                                             
#m 24.1                                                                                                            
#m -2.0                                                                                                            
#m 2.6                                                                                                             
#m 3.7                                                                                                             
#m 3.7                                                                                                             
#m 2.4                                                                                                             
#m 0.0                                                                                                             
#m 0.0                                                                                                             
#m 2.4                                                                                                             
#m 30.5                                                                                                            
#m 0.0                                                                                                             
#m 2.4                                                                                                             
#m 26.8                                                                                                            
#m 3.7                                                                                                             
#m 2.4                                                                                                             
#m 26.8                                                                                                            
#m 3.7                                                                                                             
#m 0.0                                                                                                             
#m 30.5                                                                                                            
#m 0.0                                                                                                             
#m 0.0                                                                                                             
#m 0.0                                                                                                             
#m 0.0                                                                                                             
#m 0.0                                                                                                             
#m 3.7                                                                                                             
#m 3.7                                                                                                             
#m 0.0                                                                                                             
#m 30.5                                                                                                            
#m 0.0                                                                                                             
#m 2.4                                                                                                             
#m 30.5                                                                                                            
#m 0.0                                                                                                             
#m 0.0                                                                                                             
#m 26.8                                                                                                            
#m 3.7                                                                                                             
#m 0.0                                                                                                             
#m 26.8                                                                                                            
#m 3.7                                                                                                             
#m 2.4                                                                                                             
#m 3.7                                                                                                             
#m 3.7                                                                                                             
#m 2.4                                                                                                             
#m 3.7                                                                                                             
#m 3.7                                                                                                             
#m 0.0                                                                                                             
#m 0.0                                                                                                             
#m 0.0                                                                                                             
#m 0.0                                                                                                             
#m 0.0                                                                                                             
#m 0.0                                                                                                             
#m 2.4                                                                                                             
#m 26.8                                                                                                            
#m 3.7                                                                                                             
#m 2.4                                                                                                             
#m 26.8                                                                                                            
#m 3.7                                                                                                             
#m 0.0                                                                                                             
#m 3.7                                                                                                             
#m 3.7                                                                                                             
#m 0.0                                                                                                             
#m 3.7                                                                                                             
#m 3.7                                                                                                             
#m 2.4                                                                                                             
#deg 0                                                                                                             
#m 0                                                                                                               
#m 0                                                                                                               
#m 0                                                                                                               
#m 2.438400269                                                                                                     
#m3 103.311355591                                                                                                  
#m3/s 0.00717                                                                                                      
#W 684                                                                                                             
#W 456                                                                                                             
#m 30.5                                                                                                            
#m 0.0                                                                                                             
#m 2.4                                                                                                             
#m 30.5                                                                                                            
#m 0.0                                                                                                             
#m 0.0                                                                                                             
#m 30.5                                                                                                            
#m 15.2                                                                                                            
#m 0.0                                                                                                             
#m 30.5                                                                                                            
#m 15.2                                                                                                            
#m 2.4                                                                                                             
#m 30.5                                                                                                            
#m 3.8                                                                                                             
#m 2.1                                                                                                             
#m 30.5                                                                                                            
#m 3.8                                                                                                             
#m 0.9                                                                                                             
#m 30.5                                                                                                            
#m 11.4                                                                                                            
#m 0.9                                                                                                             
#m 30.5                                                                                                            
#m 11.4                                                                                                            
#m 2.1                                                                                                             
#m 26.8                                                                                                            
#m 3.7                                                                                                             
#m 2.4                                                                                                             
#m 30.5                                                                                                            
#m 0.0                                                                                                             
#m 2.4                                                                                                             
#m 30.5                                                                                                            
#m 15.2                                                                                                            
#m 2.4                                                                                                             
#m 26.8                                                                                                            
#m 11.6                                                                                                            
#m 2.4                                                                                                             
#m 26.8                                                                                                            
#m 11.6                                                                                                            
#m 0.0                                                                                                             
#m 30.5                                                                                                            
#m 15.2                                                                                                            
#m 0.0                                                                                                             
#m 30.5                                                                                                            
#m 0.0                                                                                                             
#m 0.0                                                                                                             
#m 26.8                                                                                                            
#m 3.7                                                                                                             
#m 0.0                                                                                                             
#m 26.8                                                                                                            
#m 3.7                                                                                                             
#m 2.4                                                                                                             
#m 26.8                                                                                                            
#m 3.7                                                                                                             
#m 0.0                                                                                                             
#m 30.5                                                                                                            
#m 0.0                                                                                                             
#m 0.0                                                                                                             
#m 30.5                                                                                                            
#m 0.0                                                                                                             
#m 2.4                                                                                                             
#m 30.5                                                                                                            
#m 15.2                                                                                                            
#m 2.4                                                                                                             
#m 30.5                                                                                                            
#m 15.2                                                                                                            
#m 0.0                                                                                                             
#m 26.8                                                                                                            
#m 11.6                                                                                                            
#m 0.0                                                                                                             
#m 26.8                                                                                                            
#m 11.6                                                                                                            
#m 2.4                                                                                                             
#m 26.8                                                                                                            
#m 11.6                                                                                                            
#m 2.4                                                                                                             
#m 26.8                                                                                                            
#m 11.6                                                                                                            
#m 0.0                                                                                                             
#m 26.8                                                                                                            
#m 3.7                                                                                                             
#m 0.0                                                                                                             
#m 26.8                                                                                                            
#m 3.7                                                                                                             
#m 2.4                                                                                                             
#deg 0                                                                                                             
#m 0                                                                                                               
#m 0                                                                                                               
#m 0                                                                                                               
#m 2.438400269                                                                                                     
#m3 239.247360229                                                                                                  
#m3/s 0.0167                                                                                                       
#W 1584                                                                                                            
#W 1056                                                                                                            
#m 30.5                                                                                                            
#m 15.2                                                                                                            
#m 2.4                                                                                                             
#m 30.5                                                                                                            
#m 15.2                                                                                                            
#m 0.0                                                                                                             
#m 0.0                                                                                                             
#m 15.2                                                                                                            
#m 0.0                                                                                                             
#m 0.0                                                                                                             
#m 15.2                                                                                                            
#m 2.4                                                                                                             
#m 27.4                                                                                                            
#m 15.2                                                                                                            
#m 2.1                                                                                                             
#m 27.4                                                                                                            
#m 15.2                                                                                                            
#m 0.9                                                                                                             
#m 13.7                                                                                                            
#m 15.2                                                                                                            
#m 0.9                                                                                                             
#m 13.7                                                                                                            
#m 15.2                                                                                                            
#m 2.1                                                                                                             
#m 9.1                                                                                                             
#m 15.2                                                                                                            
#m 2.1                                                                                                             
#m 9.1                                                                                                             
#m 15.2                                                                                                            
#m 0.0                                                                                                             
#m 7.0                                                                                                             
#m 15.2                                                                                                            
#m 0.0                                                                                                             
#m 7.0                                                                                                             
#m 15.2                                                                                                            
#m 2.1                                                                                                             
#m 30.5                                                                                                            
#m 15.2                                                                                                            
#m 2.4                                                                                                             
#m 0.0                                                                                                             
#m 15.2                                                                                                            
#m 2.4                                                                                                             
#m 3.7                                                                                                             
#m 11.6                                                                                                            
#m 2.4                                                                                                             
#m 26.8                                                                                                            
#m 11.6                                                                                                            
#m 2.4                                                                                                             
#m 26.8                                                                                                            
#m 11.6                                                                                                            
#m 0.0                                                                                                             
#m 3.7                                                                                                             
#m 11.6                                                                                                            
#m 0.0                                                                                                             
#m 0.0                                                                                                             
#m 15.2                                                                                                            
#m 0.0                                                                                                             
#m 30.5                                                                                                            
#m 15.2                                                                                                            
#m 0.0                                                                                                             
#m 26.8                                                                                                            
#m 11.6                                                                                                            
#m 2.4                                                                                                             
#m 26.8                                                                                                            
#m 11.6                                                                                                            
#m 0.0                                                                                                             
#m 30.5                                                                                                            
#m 15.2                                                                                                            
#m 0.0                                                                                                             
#m 30.5                                                                                                            
#m 15.2                                                                                                            
#m 2.4                                                                                                             
#m 0.0                                                                                                             
#m 15.2                                                                                                            
#m 2.4                                                                                                             
#m 0.0                                                                                                             
#m 15.2                                                                                                            
#m 0.0                                                                                                             
#m 3.7                                                                                                             
#m 11.6                                                                                                            
#m 0.0                                                                                                             
#m 3.7                                                                                                             
#m 11.6                                                                                                            
#m 2.4                                                                                                             
#m 3.7                                                                                                             
#m 11.6                                                                                                            
#m 2.4                                                                                                             
#m 3.7                                                                                                             
#m 11.6                                                                                                            
#m 0.0                                                                                                             
#m 26.8                                                                                                            
#m 11.6                                                                                                            
#m 0.0                                                                                                             
#m 26.8                                                                                                            
#m 11.6                                                                                                            
#m 2.4                                                                                                             
#deg 0                                                                                                             
#m 0                                                                                                               
#m 0                                                                                                               
#m 0                                                                                                               
#m 2.438400269                                                                                                     
#m3 103.311355591                                                                                                  
#m3/s 0.00717                                                                                                      
#m3/s-m2                                                                                                           
#m3/s-m2                                                                                                           
#person/m2                                                                                                         
#m2/person                                                                                                         
#W 684                                                                                                             
#W/m2                                                                                                              
#W/person                                                                                                          
#1/K None                                                                                                          
#W 456                                                                                                             
#W/m2                                                                                                              
#W/person                                                                                                          
#m 0.0                                                                                                             
#m 15.2                                                                                                            
#m 2.4                                                                                                             
#m 0.0                                                                                                             
#m 15.2                                                                                                            
#m 0.0                                                                                                             
#m 0.0                                                                                                             
#m 0.0                                                                                                             
#m 0.0                                                                                                             
#m 0.0                                                                                                             
#m 0.0                                                                                                             
#m 2.4                                                                                                             
#m 0.0                                                                                                             
#m 11.4                                                                                                            
#m 2.1                                                                                                             
#m 0.0                                                                                                             
#m 11.4                                                                                                            
#m 0.9                                                                                                             
#m 0.0                                                                                                             
#m 3.8                                                                                                             
#m 0.9                                                                                                             
#m 0.0                                                                                                             
#m 3.8                                                                                                             
#m 2.1                                                                                                             
#m 3.7                                                                                                             
#m 11.6                                                                                                            
#m 2.4                                                                                                             
#m 0.0                                                                                                             
#m 15.2                                                                                                            
#m 2.4                                                                                                             
#m 0.0                                                                                                             
#m 0.0                                                                                                             
#m 2.4                                                                                                             
#m 3.7                                                                                                             
#m 3.7                                                                                                             
#m 2.4                                                                                                             
#m 3.7                                                                                                             
#m 3.7                                                                                                             
#m 0.0                                                                                                             
#m 0.0                                                                                                             
#m 0.0                                                                                                             
#m 0.0                                                                                                             
#m 0.0                                                                                                             
#m 15.2                                                                                                            
#m 0.0                                                                                                             
#m 3.7                                                                                                             
#m 11.6                                                                                                            
#m 0.0                                                                                                             
#m 0.0                                                                                                             
#m 0.0                                                                                                             
#m 2.4                                                                                                             
#m 0.0                                                                                                             
#m 0.0                                                                                                             
#m 0.0                                                                                                             
#m 3.7                                                                                                             
#m 3.7                                                                                                             
#m 0.0                                                                                                             
#m 3.7                                                                                                             
#m 3.7                                                                                                             
#m 2.4                                                                                                             
#m 3.7                                                                                                             
#m 11.6                                                                                                            
#m 2.4                                                                                                             
#m 3.7                                                                                                             
#m 11.6                                                                                                            
#m 0.0                                                                                                             
#m 0.0                                                                                                             
#m 15.2                                                                                                            
#m 0.0                                                                                                             
#m 0.0                                                                                                             
#m 15.2                                                                                                            
#m 2.4                                                                                                             
#m 3.7                                                                                                             
#m 3.7                                                                                                             
#m 2.4                                                                                                             
#m 3.7                                                                                                             
#m 3.7                                                                                                             
#m 0.0                                                                                                             
#m 3.7                                                                                                             
#m 11.6                                                                                                            
#m 0.0                                                                                                             
#m 3.7                                                                                                             
#m 11.6                                                                                                            
#m 2.4                                                                                                             
#deg 0                                                                                                             
#m 0                                                                                                               
#m 0                                                                                                               
#m 0                                                                                                               
#m 2.438400269                                                                                                     
#m3 447.682556152                                                                                                  
#m3/s 0.031089                                                                                                     
#m3/s-m2                                                                                                           
#m3/s-m2                                                                                                           
#person/m2                                                                                                         
#m2/person                                                                                                         
#W 2964                                                                                                            
#W/m2                                                                                                              
#W/person                                                                                                          
#1/K None                                                                                                          
#W 1976                                                                                                            
#W/m2                                                                                                              
#W/person                                                                                                          
#m 3.7                                                                                                             
#m 11.6                                                                                                            
#m 2.4                                                                                                             
#m 3.7                                                                                                             
#m 3.7                                                                                                             
#m 2.4                                                                                                             
#m 26.8                                                                                                            
#m 3.7                                                                                                             
#m 2.4                                                                                                             
#m 26.8                                                                                                            
#m 11.6                                                                                                            
#m 2.4                                                                                                             
#m 26.8                                                                                                            
#m 11.6                                                                                                            
#m 0.0                                                                                                             
#m 26.8                                                                                                            
#m 3.7                                                                                                             
#m 0.0                                                                                                             
#m 3.7                                                                                                             
#m 3.7                                                                                                             
#m 0.0                                                                                                             
#m 3.7                                                                                                             
#m 11.6                                                                                                            
#m 0.0                                                                                                             
#m 3.7                                                                                                             
#m 3.7                                                                                                             
#m 2.4                                                                                                             
#m 3.7                                                                                                             
#m 3.7                                                                                                             
#m 0.0                                                                                                             
#m 26.8                                                                                                            
#m 3.7                                                                                                             
#m 0.0                                                                                                             
#m 26.8                                                                                                            
#m 3.7                                                                                                             
#m 2.4                                                                                                             
#m 26.8                                                                                                            
#m 3.7                                                                                                             
#m 2.4                                                                                                             
#m 26.8                                                                                                            
#m 3.7                                                                                                             
#m 0.0                                                                                                             
#m 26.8                                                                                                            
#m 11.6                                                                                                            
#m 0.0                                                                                                             
#m 26.8                                                                                                            
#m 11.6                                                                                                            
#m 2.4                                                                                                             
#m 26.8                                                                                                            
#m 11.6                                                                                                            
#m 2.4                                                                                                             
#m 26.8                                                                                                            
#m 11.6                                                                                                            
#m 0.0                                                                                                             
#m 3.7                                                                                                             
#m 11.6                                                                                                            
#m 0.0                                                                                                             
#m 3.7                                                                                                             
#m 11.6                                                                                                            
#m 2.4                                                                                                             
#m 3.7                                                                                                             
#m 11.6                                                                                                            
#m 2.4                                                                                                             
#m 3.7                                                                                                             
#m 11.6                                                                                                            
#m 0.0                                                                                                             
#m 3.7                                                                                                             
#m 3.7                                                                                                             
#m 0.0                                                                                                             
#m 3.7                                                                                                             
#m 3.7                                                                                                             
#m 2.4                                                                                                             
#C 14.                                                                                                             
#C 50.                                                                                                             
#kg-H2O/kg-air 0.009                                                                                               
#kg-H2O/kg-air 0.004                                                                                               
#m3/s 0.00944                                                                                                      
#m3/s-m2 0.0                                                                                                       
#m3/s 0.0                                                                                                          
#m3/s 0                                                                                                            
#m3/s-m2                                                                                                           
#m3/s                                                                                                              
#m3/s 0                                                                                                            
#m3/s-m2                                                                                                           
#m3/s                                                                                                              
#C 14.                                                                                                             
#C 50.                                                                                                             
#kg-H2O/kg-air 0.009                                                                                               
#kg-H2O/kg-air 0.004                                                                                               
#m3/s 0.00944                                                                                                      
#m3/s-m2 0.0                                                                                                       
#m3/s 0.0                                                                                                          
#m3/s 0                                                                                                            
#m3/s-m2                                                                                                           
#m3/s                                                                                                              
#m3/s 0                                                                                                            
#m3/s-m2                                                                                                           
#m3/s                                                                                                              
#C 14.                                                                                                             
#C 50.                                                                                                             
#kg-H2O/kg-air 0.009                                                                                               
#kg-H2O/kg-air 0.004                                                                                               
#m3/s 0.00944                                                                                                      
#m3/s-m2 0.0                                                                                                       
#m3/s 0.0                                                                                                          
#m3/s 0                                                                                                            
#m3/s-m2                                                                                                           
#m3/s                                                                                                              
#m3/s 0                                                                                                            
#m3/s-m2                                                                                                           
#m3/s                                                                                                              
#C 14.                                                                                                             
#C 50.                                                                                                             
#kg-H2O/kg-air 0.009                                                                                               
#kg-H2O/kg-air 0.004                                                                                               
#m3/s 0.00944                                                                                                      
#m3/s-m2 0.0                                                                                                       
#m3/s 0.0                                                                                                          
#m3/s 0                                                                                                            
#m3/s-m2                                                                                                           
#m3/s                                                                                                              
#m3/s 0                                                                                                            
#m3/s-m2                                                                                                           
#m3/s                                                                                                              
#C 14.                                                                                                             
#C 50.                                                                                                             
#kg-H2O/kg-air 0.009                                                                                               
#kg-H2O/kg-air 0.004                                                                                               
#m3/s 0.00944                                                                                                      
#m3/s-m2 0.0                                                                                                       
#m3/s 0.0                                                                                                          
#m3/s 0                                                                                                            
#m3/s-m2                                                                                                           
#m3/s                                                                                                              
#m3/s 0                                                                                                            
#m3/s-m2                                                                                                           
#m3/s                                                                                                              
#m3/s autosize                                                                                                     
#C 7.0                                                                                                             
#kg-H2O/kg-Air 0.008                                                                                               
#C 11.0                                                                                                            
#kg-H2O/kg-Air 0.008                                                                                               
#C 12.8                                                                                                            
#C 16.7                                                                                                            
#kg-H2O/kg-Air 0.008                                                                                               
#kg-H2O/kg-Air 0.008                                                                                               
#m3/s 0                                                                                                            
#m3/s 0                                                                                                            
#C 82.                                                                                                             
#deltaC 11                                                                                                         
#C 7.22                                                                                                            
#deltaC 6.67                                                                                                       
#C 82.2                                                                                                            
#C 16.6                                                                                                            
#C 71.1                                                                                                            
#C 32.2                                                                                                            
#C 82.2                                                                                                            
#C 16.6                                                                                                            
#C 71.1                                                                                                            
#C 32.2                                                                                                            
#Pa 600.0                                                                                                          
#deltaC 0.002                                                                                                      
#C 19.                                                                                                             
#C -25                                                                                                             
#deltaC 0.002                                                                                                      
#m3/s 0.0                                                                                                          
#C 100                                                                                                             
#C 10                                                                                                              
#W 1000000                                                                                                         
#C 81.                                                                                                             
#C 100.                                                                                                            
#Pa 179352                                                                                                         
#C 98                                                                                                              
#C 1                                                                                                               
#W 900000                                                                                                          
#C 35.0                                                                                                            
#C 6.67                                                                                                            
#C 5
#m -1.0
#Pa 179352
#m3/s 0
#kg/kg 80.7272
#kg/kg 6.2727
#kg/kg 0.2727
#J/J 0.01
#g/MJ 50.23439
#g/MJ 3.51641E-02
#g/MJ 1.08841E-07
#g/MJ 2.09310E-07
#J/J 0.293
#g/MJ 168.33317
#g/MJ 4.20616E-02
#g/MJ 3.36414E-06
#L/MJ 2.10074
