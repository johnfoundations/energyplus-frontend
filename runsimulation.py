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


import sys
import os
import fnmatch
from PyQt4 import QtCore, QtGui
import pdb
import re


# to find filenames with line:col pairs in LilyPond output
_ly_message_re = re.compile(r"^((.*?):(\d+)(?::(\d+))?)(?=:)", re.M)


class simulation(QtCore.QObject):
    """
    init is passed the idf file with path. It finds the energyplus executable, or prompts for it.
    It gets either the default weather file or prompts for it.
    
    It then opens a log window, runs the simulation and shows the error file if it failed.
    """
    def __init__(self, idffile,log):
        self.log = log
        self.idffile = idffile
        self.args = QtCore.QStringList()
        self.basename = os.path.split(str(idffile))[1]
        self.directory = os.path.split(str(idffile))[0]
        print self.basename, self.directory

        self.p = QtCore.QProcess()
        self.p.setProcessChannelMode(QtCore.QProcess.MergedChannels)
        self.p.setWorkingDirectory(self.directory)
        cmd = self.getEPExecutable()
        self.args.append(self.basename)
        self.args.append(self.getWeatherFile())
        self.connect(self.p, QtCore.SIGNAL("finished(int, QProcess::ExitStatus)"),
                        self.finished)
        self.connect(self.p, QtCore.SIGNAL("error(QProcess::ProcessError)"), self.error)
        self.connect(self.p, QtCore.SIGNAL("readyRead()"), self.readOutput)
        
        self.log.clear()
        self.log.writeLine('%s running %s with %s...' % (cmd,self.args[0],self.args[1]))
#        self.startTime = time.time()
        self.p.start(cmd,self.args)
        

    def getEPExecutable(self):
        
        epdir = ''
        settings = QtCore.QSettings("EPlus", "IDF Editor")    
        if settings.value("epfolder",'') == '':
            #find energyplus folder
            import fnmatch
            import os
            foundep = False
            print os.name
            if os.name == 'posix':
                epdir = '/usr/local/'
                print 'check usr local'
                for f in os.listdir(epdir):
                    print f
                    if fnmatch.fnmatch(f, 'Energy*'):
                        epdir += f
                        print epdir
                        foundep = True
                        
            else:
                print 'Operating System Not Supported'
                return
                
            if not foundep:
                epdir = QtGui.QFileDialog.getExistingDirectory(None, 'Find Energy Plus Installation Folder',
                                                 "/",QtGui.QFileDialog.ShowDirsOnly)
                                                 
            settings.setValue('epfolder',epdir)
            
            
        else:
            epdir = settings.value('epfolder','')
            print 'epdir',epdir.toString()
        #append executable
        return epdir.toString() + '/bin/runenergyplus'
            
        
        
    def getWeatherFile(self):
        settings = QtCore.QSettings("EPlus", "IDF Editor")
        weatherfile = ''
        if settings.value('weather','') == '':
            w = QtGui.QFileDialog.getOpenFileName(None,"Select Weather File", settings.value('epfolder','').toString(), "*.epw *.EPW")
            weatherfile = os.path.split(str(w))[1]
            settings. setValue('weather',weatherfile)
        else:
            weatherfile = settings.value('weather','').toString()
            
        return weatherfile

        
        
    def finished(self, exitCode, exitStatus):
        if exitCode:
            self.log.writeMsg("EnergyPlus %s exited with return code %s." %(self.args[0], exitCode))
        elif exitStatus:
            self.log.writeMsg("EnergyPlus %s exited with exit status %s." %(self.args[0], exitStatus))
        else:
            # We finished successfully, show elapsed time...
            seconds = time.time() - self.startTime
            if seconds < 60:
                elapsed = '%.1f"' % seconds
            else:
                elapsed = "%i'%i\"" % divmod(seconds, 60)
            self.log.writeMsg(i18n("LilyPond [%1] finished (%2).",
                self.lyfile_arg, elapsed), "msgok")
        self.bye(not (exitCode or exitStatus))
    
    def error(self, errCode):
        """ Called when QProcess encounters an error """
        if errCode == QtCore.QProcess.FailedToStart:
            self.log.writeMsg("Could not start EnergyPlus. Please check path and permissions.",
                "msgerr")
        elif errCode == QtCore.QProcess.ReadError:
            self.log.writeMsg("Could not read from the EnergyPlus process.","msgerr")
        elif self.p.state() == QtCore.QProcess.NotRunning:
            self.log.writeMsg("An unknown error occured.", "msgerr")
        if self.p.state() == QtCore.QProcess.NotRunning:
            self.bye(False)
        
    def bye(self, success):
        # otherwise we delete ourselves during our event handler, causing crash
        QtCore.QTimer.singleShot(0, lambda: self.done(success, self))

    def abort(self):
        """ Abort the LilyPond job """
        self.p.terminate()

    def kill(self):
        """
        Immediately kill the job, and disconnect it's output signals, etc.
        Emits the done(False) signal.
        """
        self.disconnect(self.p,QtCore.SIGNAL("finished(int, QProcess::ExitStatus)"), self.finished)
        self.disconnect(self.p,QtCore.SIGNAL("error(QProcess::ProcessError)"), self.error)
        self.disconnect(self.p, QtCore.SIGNAL("readyRead()"), self.readOutput)
        self.p.kill()
        self.p.waitForFinished(2000)
        self.done(False, self)
        
    def readOutput(self):
        encoding = sys.getfilesystemencoding() or 'utf-8'
        text = str(self.p.readAllStandardOutput()).decode(encoding, 'replace')
        parts = _ly_message_re.split(text)
        # parts has an odd length(1, 6, 11 etc)
        # message, <url, path, line, col, message> etc.
        self.log.write(parts.pop(0))
        while len(parts[:5]) == 5:
            url, path, line, col, msg = parts[:5]
            path = os.path.join(self.directory, path)
            line = int(line or "1") or 1
            col = int(col or "0")
            self.log.writeFileRef(url, path, line, col)
            self.log.write(msg)
            del parts[:5]
    
    def updatedFiles(self):
        """
        Returns a function that can list updated files based on extension.
        """
        return frescobaldi_app.mainapp.updatedFiles(self.lyfile,
            math.floor(self.startTime))
        




class LogWidget(QtGui.QFrame):
    def __init__(self, parent=None):
        QtGui.QFrame.__init__(self, parent)
        self.preview = False # this is used by Ly2PDF and the ActionManager
        layout = QtGui.QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        self.textBrowser = QtGui.QTextBrowser(self)
        self.textBrowser.setFocusPolicy(QtCore.Qt.NoFocus)
        self.textBrowser.setOpenLinks(False)
        self.textBrowser.setOpenExternalLinks(False)
        self.textCursor = QtGui.QTextCursor(self.textBrowser.document())
        self.formats = textFormats()
        layout.addWidget(self.textBrowser)
        self.actionBar = QtGui.QToolBar(self)
        self.actionBar.setFloatable(False)
        self.actionBar.setMovable(False)
        self.actionBar.setToolButtonStyle(QtCore.Qt.ToolButtonTextBesideIcon)
        self.actionBar.setIconSize(QtCore.QSize(16, 16))
        self.actionBar.layout().setContentsMargins(0, 0, 0, 0)
        layout.addWidget(self.actionBar)
        self.actionBar.hide()
        # frame style:
        self.setFrameStyle(self.textBrowser.frameStyle())
        self.textBrowser.setFrameStyle(QtGui.QFrame.NoFrame)
    
    def clear(self):
        self.textBrowser.clear()
        self.actionBar.clear()
        self.actionBar.hide()
    
    def checkScroll(self, func):
        """
        Checks if we were scrolled to the bottom, calls func and then
        again makes sure to scroll to the bottom, if we were.
        """
        sb = self.textBrowser.verticalScrollBar()
        # were we scrolled to the bottom?
        bottom = sb.value() == sb.maximum()
        func()
        # if yes, keep it that way.
        if bottom:
            sb.setValue(sb.maximum())
        
    def write(self, text, format='log'):
        self.checkScroll(lambda:
            self.textCursor.insertText(text, self.formats[format]))

    def writeMsg(self, text, format='msg'):
        # start on a new line if necessary
        if self.textCursor.columnNumber() > 0:
            self.write('\n', format)
        self.write(text, format)

    def writeLine(self, text, format='msg'):
        self.writeMsg(text + '\n', format)
        
    def writeFileRef(self, text, path, line, column, tooltip=None, format='log'):
        self.write(text, format)


class Log(LogWidget):
    """
    A more advanced version of the logwidget, designed for embedding
    in a tool.
    """
    def __init__(self, tool, doc):
        self.tool = tool
        self.doc = doc
        self.anchors = {}
        self.anchorgen = anchorgen().next
        LogWidget.__init__(self, tool.widget)
        QObject.connect(self.textBrowser, SIGNAL("anchorClicked(QUrl)"),
            self.anchorClicked)
        # context menu:
        self.textBrowser.setContextMenuPolicy(Qt.CustomContextMenu)
        QtCore.QObject.connect(self.textBrowser,
            SIGNAL("customContextMenuRequested(QPoint)"),
            self.showContextMenu)
    
    def clear(self):
        self.anchors.clear()
        self.anchorgen = anchorgen().next
        super(Log, self).clear()
        
    def show(self):
        """ Really show our log, e.g. when there are errors """
        self.tool.showLog(self.doc)
        self.tool.show()

    def writeFileRef(self, text, path, line, column, tooltip=None, format='url'):
        anchor = self.anchorgen()
        self.anchors[anchor] = FileRef(self.doc.app, path, line, column)
        f = self.formats[format]
        f.setAnchorHref(anchor)
        f.setToolTip(tooltip or i18n("Click to edit this file"))
        self.write(text, format)
        self.show() # because this refers to a warning or error
    
    def anchorClicked(self, url):
        ref = self.anchors.get(str(url.path()))
        if ref:
            ref.activate()
    
    def showContextMenu(self, pos):
        m = KMenu(self.textBrowser)
        m.addTitle(i18n("LilyPond Log"))
        self.addContextMenuActions(m)
        m.exec_(self.textBrowser.mapToGlobal(pos))
        
    def addContextMenuActions(self, menu):
        a = menu.addAction(KIcon("edit-copy"), i18n("&Copy"))
        QObject.connect(a, SIGNAL("triggered()"), self.copyLog)
        g = KStandardGuiItem.saveAs()
        a = menu.addAction(g.icon(), g.text())
        QObject.connect(a, SIGNAL("triggered()"), self.saveLogAs)

    def copyLog(self):
        text = (self.textBrowser.textCursor().selection().toPlainText()
                or self.textBrowser.toPlainText())
        if text:
            KApplication.clipboard().setText(text)
        
    def saveLogAs(self):
        startDir, fileName = os.path.split(self.doc.localPath())
        fileName = (os.path.splitext(fileName)[0] or "lilypond") + ".log"
        dlg = KEncodingFileDialog(startDir, 'utf-8', '',
            i18n("Save LilyPond Log as"),
            KEncodingFileDialog.Saving, self.textBrowser)
        dlg.setSelection(fileName)
        dlg.setConfirmOverwrite(True)
        result = dlg.exec_()
        if not result:
            return # Cancelled
        encoding = str(dlg.selectedEncoding())
        fileName = unicode(dlg.selectedFile())
        text = unicode(self.textBrowser.textCursor().selection().toPlainText()
                or self.textBrowser.toPlainText())
        try:
            f = open(fileName, 'w')
            f.write(text.encode(encoding, 'replace'))
            f.close()
        except (OSError, IOError), e:
            KMessageBox.error(self.textBrowser,
                i18n("Could not save LilyPond log:\n\n%1", unicode(e)))


def textFormats():
    """ Return a dict with text formats for the log view """
    log = QtGui.QTextCharFormat()
    log.setFontFamily("monospace")
    
    url = QtGui.QTextCharFormat(log)
    url.setForeground(QtGui.QBrush(QtGui.QColor("blue")))
    url.setFontUnderline(True)
    url.setAnchor(True)
    
    msg = QtGui.QTextCharFormat()
    msg.setFontFamily("sans-serif")
    msg.setFontWeight(QtGui.QFont.Bold)
    
    msgok = QtGui.QTextCharFormat(msg)
    msgok.setForeground(QtGui.QBrush(QtGui.QColor("green")))
    
    msgerr = QtGui.QTextCharFormat(msg)
    msgerr.setForeground(QtGui.QBrush(QtGui.QColor("red")))
    
    return locals()


if __name__ == "__main__":
    print 'runsimulation'
    
    
    
    app = QtGui.QApplication(sys.argv)
    log = LogWidget()
    sim = simulation('/home/derek/energyplus-frontend/energyplus-frontend/wildlifegenetics/wlgidealair1.idf',log)
    log.show()

    sys.exit(app.exec_())