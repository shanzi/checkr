#!/usr/bin/env python
# encoding: utf-8

# Create your views here.
from django.shortcuts import render_to_response, get_object_or_404
from django.contrib.auth.decorators import login_required

from assignment.models import Assignment 
from student.models import Student
from submission.models import Submission

from django.utils import timezone
from django.template import RequestContext, Context, loader
from mailer.mail_settings import DEFAULT_SENDER, DEFAULT_RECEIVERS

collections = [0, 1, 2]

def assignments(request):
    assignments = Assignment.objects.all()
    student_count = Student.objects.count()
    return render_to_response('assignments.html',
            dict(
            student_count=student_count,
            title="assignments",
            assignments=assignments))



@login_required
def assignment(request, seq):
    assignment = get_object_or_404(Assignment, sequence=seq)
    cs = []
    for c in collections:
        students = Student.objects.filter(collection=c).order_by('student_num').values()
        s_count = len(students)
        sub_count = 0
        for student in students:
            submissions = Submission.objects.filter(
                    student=student['id'],
                    assignment=assignment).values()
            if submissions:
                student['submission'] = submissions[0]
                sub_count += 1

        cs.append((students, sub_count, s_count))

    return render_to_response('assignment.html', 
            dict(
                assignment=assignment,
                title=assignment.title,
                collections=cs,
                ))

@login_required
def report(request, seq):
    assignment = get_object_or_404(Assignment, sequence=seq)
    cs = []
    all_sum = 0
    sub_sum = 0
    for c in collections:
        students = Student.objects.filter(collection=c).order_by('student_num').values()
        s_count = len(students)
        sub_count = 0
        zeros = []
        for student in students:
            submissions = Submission.objects.filter(
                    student=student['id'],
                    assignment=assignment).values()
            if submissions:
                sub_count += 1
            else:
                zeros.append(student)
        all_sum += s_count
        sub_sum += sub_count
        cs.append((zeros, s_count, sub_count, s_count-sub_count))

    zero_sum = all_sum - sub_sum
    now = timezone.now()
    to = None

    if request.POST and request.POST.has_key('to'):
        from mailer.process_mail import _mail_sender
        import re
        to = request.POST['to']
        to = set(re.split(r'[\s,;]+', to))
        to.add(DEFAULT_SENDER)
        to.discard('')
        t = loader.get_template('mails/report.html')
        receivers = to | set(DEFAULT_RECEIVERS)
        context = Context({
            'title':assignment.title,
            'collections':cs,
            'now':now,
            'all_sum':all_sum,
            'sub_sum':sub_sum,
            'zero_sum':zero_sum,
            'to':to,
            'receivers':receivers,
            })
        message = t.render(context)
        sender = _mail_sender()
        subject = "数据结构 %s 提交情况报告".decode('utf8')% assignment.title
        print "sending mails to %d address:" % len(to)
        print '-'*40 
        for i, toaddr in enumerate(to):
            print "%d.  %s" % (i, toaddr)
        print '-'*40 
        sender.send_mail(subject, None, DEFAULT_SENDER, set(to), html_message=message)

    return render_to_response('report.html',
            {   'title':assignment.title,
                'collections':cs,
                'now':now,
                'all_sum':all_sum,
                'sub_sum':sub_sum,
                'zero_sum':zero_sum,
                'to':to,
                'receivers':DEFAULT_RECEIVERS,
                }, context_instance=RequestContext(request))
