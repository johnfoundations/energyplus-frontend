# -*- coding: iso-8859-1 -*-
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


import smtplib, os, time, atexit
from email.MIMEMultipart import MIMEMultipart
from email.MIMEBase import MIMEBase
from email.MIMEText import MIMEText
from email.Utils import formatdate
from email import Encoders

class ConnectionError(smtplib.SMTPException): pass
class LoginError(smtplib.SMTPException): pass
class DisconnectionError(smtplib.SMTPException): pass
class EmailSendError(smtplib.SMTPException): pass

class Smtp:

    def __init__(self, host, user, password, port=25):
        self._host        = host
        self._port        = port
        self._user        = user
        self._password    = password

        self._message     = None
        self._subject     = None
        self._from_addr   = None
        self._rcpt_to     = None
        self._server      = None
        self._attachments = []

        atexit.register(self.close) #our close() method will be automatically executed upon normal interpreter termination

        self.connect()

    def connect(self):

        if all([self._host, self._port, self._user, self._password]):

            try:
                print 'starting server'
                self._server = smtplib.SMTP(self._host, self._port)

            except smtplib.SMTPException, e:
                raise ConnectionError("Connection failed!")

            self._server.ehlo()
            self._server.starttls()
            self._server.ehlo()

            try:
                print 'logging in'
                self._server.login(self._user, self._password)

            except smtplib.SMTPException, e:
                raise LoginError("Login Failed!")



    def close(self):

        if self._server:
            try:
                self._server.quit()

            except smtplib.SMTPException, e:
                raise DisconnectionError("Disconnection failed!")



    def message(self, message):
        self._message = message


    def subject(self, subject):
        self._subject = subject


    def from_addr(self, email):
        self._from_addr = email


    def rcpt_to(self, email):
        self._rcpt_to = email


    def attach(self, file):
        if os.path.exists(file):
            self._attachments.append(file)
        else:
            print 'attach failed. File does not exist', file



    def load_attachments(self, m_message):
        for mfile in self._attachments:
            print 'load_attachments',mfile
            part = MIMEBase('application', "octet-stream")
            part.set_payload(open(mfile,"rb").read())
            Encoders.encode_base64(part)
            part.add_header('Content-Disposition', 'attachment; filename="%s"' % os.path.basename(mfile))
            m_message.attach(part)

        return m_message


    def send(self, content_type='plain', charset='UTF-8'):

        if all([self._message, self._subject, self._from_addr, self._rcpt_to]):

            m_message             = MIMEMultipart()
            m_message['From']     = self._from_addr
            m_message['To']       = self._rcpt_to
            m_message['Date']     = formatdate(localtime=True)
            m_message['Subject']  = self._subject
            m_message['X-Mailer'] = "Python X-Mailer"
            m_message.attach(MIMEText(self._message, content_type, charset))
            m_message = self.load_attachments(m_message)
            try:
                print 'attempting send'
                self._server.sendmail(self._from_addr, self._rcpt_to.split(','), m_message.as_string())

            except smtplib.SMTPException, e:
		print e
                raise EmailSendError("Email has not been sent")
