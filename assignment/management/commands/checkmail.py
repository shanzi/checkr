from django.core.management.base import BaseCommand, CommandError

from mailer.process_mail import process_mail


class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        process_mail()
