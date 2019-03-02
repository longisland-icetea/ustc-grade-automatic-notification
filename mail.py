#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import smtplib
from email.mime.text import MIMEText
from config import *


def send_email(subject):
    msg = MIMEText(subject,'plain','utf-8')
    msg['Subject'] = '新成绩'
    msg['From'] = smtp_username
    msg['To'] = smtp_to
    if smtp_ssl:
        s = smtplib.SMTP_SSL(smtp_server)
    else:
        s = smtplib.SMTP(smtp_server)
    s.login(smtp_username, smtp_password)
    s.sendmail(smtp_username, smtp_to, msg.as_string())
    s.quit()
