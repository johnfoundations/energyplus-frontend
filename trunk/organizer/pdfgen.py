# -*- coding: utf-8 -*-
"""***************************************************************************
*   Copyright (C) 2010 by Derek Kite   *
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


from __future__ import division
import os
import reportlab
from reportlab.platypus import *
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.rl_config import defaultPageSize
from reportlab.lib.units import inch

import Image



def createPDF(outputPDFName,imglist):
    PAGE_HEIGHT = defaultPageSize[1]
    PAGE_WIDTH  = defaultPageSize[0]
    styles = getSampleStyleSheet()
    elements = []
    for img in imglist:
        print 'createPDF, adding',img
        pilimg = Image.open(img)
        #figure out size and scale to 8.5x11 minus margins
        #imgwidth,imgheight = pilimg.size()
        print pilimg.size
        pw = pilimg.size[0]
        ph = pilimg.size[1]
        print pw,ph
        aspectratio = ph/pw
        print 'aspectratio',aspectratio
        w = PAGE_WIDTH-inch
        h = w*aspectratio
        print w,h
        elements.append(reportlab.platypus.Image(img,w,h))
        fname = os.path.splitext(img)[0]
        if os.path.exists(fname+'.txt'):
            print 'text file exists',fname
            txtf = open(fname+'.txt')
            t = txtf.read()
            elements.append(Paragraph(t,styles["Normal"]))

        elements.append(PageBreak())

    t = SimpleDocTemplate(outputPDFName)
    t.build(elements)





def savePDF(filename,imglist,dpi):
    output = str(filename)
    width, height = letter
    c = canvas.Canvas(output, pagesize=letter)
    for img in imglist:
        print 'savePDF, adding',img
        pilimg = Image.open(img)
        c.drawInlineImage(pilimg,0,height-(inch*pilimg.size[1]/dpi)-2,inch*pilimg.size[0]/dpi,inch*pilimg.size[1]/dpi)
        #check for text file
        fname = os.path.splitext(img)[0]
        if os.path.exists(fname+'.txt'):
            print 'text file exists',fname
            textobj = c.beginText()
            roomleft = 0
            print 'check if there is room left on page',pilimg.size[1]/dpi,pilimg.size[0]/dpi,dpi,height/inch
            if pilimg.size[1]/dpi > (height/inch) - (.5):
                c.showPage()
                textobj.setTextOrigin(inch,inch*11 - inch)
                roomleft = height-inch

            else:
                textobj.setTextOrigin(inch,height-(inch)-(pilimg.size[1]/dpi*inch))
                roomleft = height-inch-(pilimg.size[1]/dpi*inch)-inch

            print 'read from file and insert lines'
            txtf = open(fname+'.txt')
            for line in txtf:
                textobj.textLine(line.strip())
                if textobj.getY() - (inch/3) < 0:
                    c.drawText(textobj)
                    c.showPage()
                    textobj = c.beginText()
                    textobj.setTextOrigin(inch,inch*11 - inch)
                    roomleft = height - inch

            c.drawText(textobj)
            c.showPage()

        else:
            c.showPage()

    c.save()

if __name__ == '__main__':
    imglist = ['/home/derek/scanandsave/scans/scan-2010-6-11-22:27:1/scan-2010-6-11-22:27:25.png',\
               '/home/derek/scanandsave/scans/scan-2010-6-11-22:27:1/scan-2010-6-11-22:27:42.png']

    createPDF('test.pdf',imglist,100)



