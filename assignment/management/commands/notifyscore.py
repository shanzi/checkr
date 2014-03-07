from django.core.management.base import BaseCommand, CommandError
from optparse import make_option
from mailer.process_mail import _mail_sender
from mailer.mail_settings import DEFAULT_SENDER
from student.models import Student
from assignment.models import Assignment
from django.template import Context, loader
import random

class Command(BaseCommand):
    option_list = BaseCommand.option_list + (
            make_option(
                '--preview',
                action='store_true',
                dest='preview',
                default=False,
                help='if preview'),
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
        preview = options['preview']
        preview_flag = 0
        subject = options['subject']
        t = loader.get_template('mails/notifyscore.html')
        sender = _mail_sender()
        assignments = Assignment.objects.order_by('sequence').values()
        assignments_len = len(assignments)
        for student in Student.objects.all():
            submission_count = student.submissions.count()
            if submission_count==0: continue
            submissions = student.submissions.all()
            results = [0] * assignments_len
            email = ''
            for submission in submissions:
                seq = submission.assignment.sequence
                if seq >0 and seq <= assignments_len:
                    results[seq-1] = float(submission.score)
                    if (not email) and submission.mails.count():
                        mail = submission.mails.all()[0]
                        email = mail.fromaddr
            if not email:
                print "email not found for student: %s" % student
                continue
            context = Context({'student':student,'results':results, 'results_sum':sum(results)})
            message = t.render(context)
            if preview:
                if preview_flag == 0:
                    sender.send_mail(subject, None, DEFAULT_SENDER, [DEFAULT_SENDER], html_message=message)
                    preview_flag = random.randint(20, 40)
                    print "sent preview email to %s" % DEFAULT_SENDER
                else:
                    preview_flag -= 1
                    print "sent to %s test passed" % email
            else:
                print "sending mail to %s" % email
                sender.send_mail(subject, None, DEFAULT_SENDER, [email], html_message=message)

