#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# (c) Copyright 2003-2009 Hewlett-Packard Development Company, L.P.
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307 USA
#
# Author: Don Welch
#

import sys
import sane
import paperlist
import crop
import traceback

def timeStamp():
    import time
    tuple_time = time.localtime()
    secs = tuple_time[5]
    hours = tuple_time[3]
    if int(hours) in range(10):
        hours = "0%s" %hours
    minutes = tuple_time[4]
    if int(minutes) in range(10):
        minutes = "0%s" %minutes
    day = tuple_time[2]
    month = tuple_time[1]
    year = tuple_time[0]
    scan = 'scan'
    time_ = "%s-%s-%s-%s-%s:%s:%s" %(scan, year, month, day, hours, minutes,secs)
    return time_










def runScan(device,source,paper,dest):
    #print 'runScan',device,source,paper,dest
    sane.init()
    #print sane.get_devices()
    #print 'try to open scanner',device
    scandev = sane.open(device)
#   except:
#       'open scanner failed'
#       return -1

    #print 'set source', source
    if source == 'ADF':
        #print 'setting batch_scan'
        scandev.source = source
        scandev.batch_scan = 1
        scancount = 50
    else:
        scandev.source = source
        scandev.batch_scan = 0
        scancount = 1

    #set dpi to 200
    scandev.resolution = 200

    #calculate size and set x,y
    sizes = paperlist.paperlist[paper]
    #print 'setPaper',paper,sizes
#        print self.scandev.opt
    scandev.tl_x = 0
    scandev.tl_y = 0
    scandev.br_x = sizes[0]
    scandev.br_y = sizes[1]
    #print 'about to start scan'
#    s = raw_input()
    while scancount > 0:
        #print 'run',scancount
        try:
                scandev.start()
                scancount -= 1
        except:
                #traceback.print_exc()
                scancount = 0
                break

        #print 'scanning'
        img = scandev.snap()
        img = crop.autoCrop(img)
        filename = str(dest)+'/'+str(timeStamp())+'.png'
        img.save(filename,"PNG")
        #print 'closing scanner device'
        print filename
        #flush()

    scandev.close()
    return 0


if __name__ == '__main__':
    import getopt
    #args = '-p -s -n -d'.split()
    optlist, args = getopt.getopt(sys.argv[1:],'npsd', ['source=','paper=','scanner=','dest='])
    #print optlist
    for o,a in optlist:
        if o == '--source':
            source = a
        elif o == '--paper':
            paper = a
        elif o == '--scanner':
            scanner = a
        elif o == '--dest':
            dest = a

    runScan(scanner,source,paper,dest)

