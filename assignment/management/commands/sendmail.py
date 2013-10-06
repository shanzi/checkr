from django.core.management.base import BaseCommand, CommandError
from optparse import make_option
from mailer.process_mail import _mail_sender
from mailer.mail_settings import DEFAULT_SENDER
from submission.models import Email
from django.template import Context, loader

class Command(BaseCommand):
    option_list = BaseCommand.option_list + (
            make_option(
                '-a','--all',
                action='store_true',
                dest='all',
                default=False,
                help='send mails to all'),
            make_option(
                '--to',
                action='append',
                dest='to',
                default=[DEFAULT_SENDER],
                help='send mail to specified email address'),
            make_option(
                '-t','--template',
                action='store',
                type='string',
                dest='template',
                help='template of email'),
            make_option(
                '-s','--subject',
                action='store',
                type='string',
                dest='subject',
                default='Data Structure Homework',
                help='subject of email'))

    def handle(self, *args, **options):
        subject = options['subject']
        to = set(options['to'])
        all_ = options['all']
        template = options['template']
        if all_:
            to |= {email['fromaddr'] for email in Email.objects.all().values()}
        t = loader.get_template('mails/{}.html'.format(template))
        context = Context(locals())
        message = t.render(context)
        sender = _mail_sender()
        print "sending mails to %d address:" % len(to)
        print '-'*40 
        for i, toaddr in enumerate(to):
            print "%d.  %s" % (i, toaddr)
        print '-'*40 
        sender.send_mail(subject, message, DEFAULT_SENDER, set(to))

