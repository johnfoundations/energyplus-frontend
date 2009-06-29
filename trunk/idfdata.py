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

from PyQt4 import QtGui, QtCore
import idfread

class idfData(QObject):
    def __init__(parent = 0):
        self.idfreadlist = []   #list of idfread classes, allowing multiple idf files to be loaded
        self.idflist = []       #list of classes from idf files
        self.current = 0        #pointer to current class, used in iterating through list

    def next(self):
        if current == len(self.idflist):
            return False
        current = current + 1
        return True

    def previous(self):
        if current == 0:
            return False
        current = current - 1    
        return True

    def first(self):
        if len(self.idflist) == 0:
            return False
        current = 0
        return True

    def last(self):
        if len(self.idflist) == 0:
            return False
        current = self.idflist(self.current) - 1
        return True

    def size(self):
        return len(self.idflist)
        #returns count

    def record(self):
        return self.idflist[self.current]

    def openIdf(self,filename):
        idf = idfread.idfRead(filename)
        if len(idflist) > 0:
            idflist = idf.getActiveList()
        else:
            idflist = idflist + idf.getActiveList()

        self.idfreadlist.append(idf)
        

    def writeIdf(self,filename):
        pass
