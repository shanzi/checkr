#!/usr/bin/env python
# encoding: utf-8

from django.conf import settings
from django.core.mail import send_mail, send_mass_mail
from django.core.mail import EmailMultiAlternatives
import html2text

class MailSender(object):

    def __init__(self, server, username, password, ssl=False):
        settings.EMAIL_HOST = server
        settings.EMAIL_HOST_USER = username
        settings.EMAIL_HOST_PASSWORD = password
        settings.EMAIL_USE_SSL = False

    def send_mail(self, subject, message, fromaddr, toaddr, html_message=None):
        msg = EmailMultiAlternatives(subject, message, fromaddr, toaddr)
        if html_message and not message:
            message = html2text.html2text(html_message)
            msg.attach_alternative(html_message, 'text/html')
        msg.send()

    def send_mass_mail(self, messages):
        for subject, body, from_, to in messages:
            print "sending: <%s> to %s" % (subject, to) 
            self.send_mail(subject, None, from_, to, html_message=body)
