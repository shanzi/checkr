#!/usr/bin/env python
# encoding: utf-8

from mailer.imbox import Imbox
from mailer.mailsender import MailSender
from mailer import mail_settings as settings

def _mail_reciever():
    receiver = settings.RECEIVER
    server = receiver['server']
    ssl = receiver['ssl']
    account = settings.ACCOUNT

    return Imbox(server,
            username=account['username'],
            password=account['password']
            ssl=ssl)

def _mail_sender():
    sender = settings.sender
    server = sender['sender']
    ssl = sender['ssl']
    account = settings.ACCOUNT
    return MailSender(server,
            username=account['username']
            password=account['password']
            ssl=ssl)

def _process_mail():
    pass
    
