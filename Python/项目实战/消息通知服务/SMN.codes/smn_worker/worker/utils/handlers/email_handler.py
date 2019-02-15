#! -*- coding: utf-8 -*-


# author: forcemain@163.com


import smtplib


from worker import settings
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


class EmailHandler(object):
    def __init__(self, **kwargs):
        self._debug = kwargs.get('debug', False)
        self.smtp_host = kwargs.get('smtp_host', settings.SMN_EMAIL_SMTP_HOST)
        self.smtp_port = kwargs.get('smtp_port', settings.SMN_EMAIL_SMTP_PORT)
        self.smtp_user = kwargs.get('smtp_user', settings.SMN_EMAIL_SMTP_USER)
        self.smtp_pass = kwargs.get('smtp_pass', settings.SMN_EMAIL_SMTP_PASS)

    @property
    def server(self):
        server = smtplib.SMTP_SSL(self.smtp_host, self.smtp_port)
        server.set_debuglevel(self._debug)
        server.ehlo(self.smtp_host)
        server.login(self.smtp_user, self.smtp_pass)

        return server

    def send(self, name='', _to=(), _cc=(), subject='', content='', payloads=()):
        _from = '{0}<{1}>'.format(name, self.smtp_user) if name else self.smtp_user

        msg = MIMEMultipart('related')
        msg_html = MIMEText(content, _subtype='html', _charset='utf-8')
        msg.attach(msg_html)
        map(lambda payload: msg.attach(payload), payloads)

        msg['Subject'] = subject
        msg['From'] = _from
        msg['To'] = ';'.join(_to)
        msg['Cc'] = ';'.join(_cc)

        self.server.sendmail(_from, _to+_cc, msg.as_string())
        self.server.close()
