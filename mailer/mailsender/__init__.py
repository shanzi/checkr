#!/usr/bin/env python
# encoding: utf-8

from django.conf import settings
from django.core.mail import send_mail, send_mass_mail

class MailSender(object):

    def __init__(self, server, username, password, ssl=False):
        settings.EMAIL_HOST = server
        settings.EMAIL_HOST_USER = username
        settings.EMAIL_HOST_PASSWORD = password
        settings.EMAIL_USE_SSL = False

    def send_mail(self, subject, message, fromaddr, toaddr):
        send_mail(subject, message, fromaddr, toaddr)

    def send_mass_mail(self, messages):
        send_mass_mail(messages)
