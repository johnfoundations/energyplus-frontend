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

  
  
converstionvalues = {'m':('/3.281','ft','*3.281'),\
                     'W':('/3.412','Btu/h','*3.412')\
                     'm3/s':('/2118.6438','ft3/min','*2118.6438')\
                     'C':('*1.8+32','F','-32/1.8')\
                     'kg/J':('/2325.83774250441','lb/Btu','*2325.83774250441')\
                     'Pa':('/0.0001450377','psi','*0.0001450377')\
                     'W/m-K':('/6.93481276005548','Btu-in/h-ft2-F','*6.93481276005548')\
                     'W/K':('/1.8987','Btu/h-F','*1.8987')\
                     'deltaC':('/1.8','deltaF','*1.8')\
                     'm2':('/10.764961','ft2','*10.764961')\
                     'K':('/1.8','R','*1.8')\
                     '1/K':('/0.555555556','1/R','*0.555555556')\
                     '(kg/s)/W':('/0.646078115385742','(lbm/sec)/(Btu/hr)','*0.646078115385742')\
                     'J/kg':('/0.00042986 + 7.686','Btu/lb','*0.00042986 - 7.686')\
                     'kg-H2O/kg-air':('*1','lb-H2O/lb-air','*1')\
                     
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
