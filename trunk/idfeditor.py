# -*- coding: utf-8 -*-
# File : idfeditor.py
import sys
from PyQt4 import QtGui, QtCore
from gwidget import GWidget

# We start a new class here
# derived from QMainWindow
# A calendar is displayed and clicking on a date makes this date be displayed on the label on the bottom

class idfeditor(QtGui.QMainWindow):
    def __init__(self):
        QtGui.QMainWindow.__init__(self)
       	myWidget = GWidget()
        self.setCentralWidget(myWidget)
        self.setWindowTitle('IDF Creator')
        self.resize(800, 600)
        self.statusBar().showMessage('Click on Scene to start')
  


if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    window = idfeditor()
    window.show()
    sys.exit(app.exec_())
