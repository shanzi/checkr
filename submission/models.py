#!/usr/bin/env python
# encoding: utf-8

from django.db import models
from student.models import Student
from assignment.models import Assignment


class Submission(models.Model):
    student = models.ForeignKey(Student, related_name="submissions")
    assignment = models.ForeignKey(Assignment, related_name="submissions")
    score = models.DecimalField(max_digits=5, decimal_places=1, default=5)
    updated_at = models.DateTimeField()
    cpplint_result = models.TextField()

    def __unicode__(self):
        return u'[%s] %s (%s)' % (self.assignment.sequence,
                self.student.student_num, self.score)


class Email(models.Model):
    fromaddr = models.CharField(max_length=100)
    toaddr = models.CharField(max_length=100)
    subject = models.CharField(max_length=120)
    content = models.TextField()
    attachment_title = models.CharField(max_length=60)
    sent_at = models.CharField(max_length=80)
    sent_at_parsed = models.DateTimeField(null=True)
    submission = models.ForeignKey(Submission, related_name='mails')

    def __unicode__(self):
        return u'%s (from: <%s>)' % (self.subject, self.fromaddr)


class File(models.Model):
    filename = models.CharField(max_length=200)
    content = models.TextField()
    submission = models.ForeignKey(Submission, related_name='files')

    def __unicode__(self):
        return self.filename
