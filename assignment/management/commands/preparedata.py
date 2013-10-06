#!/usr/bin/env python
# encoding: utf-8

from django.core.management.base import BaseCommand, CommandError
from namelist import NAME_LIST
from student.models import Student
from assignment.models import Assignment, seq_descriptions

class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        for i, lst in enumerate(NAME_LIST):
            for k, v in lst.iteritems():
                stu, created = Student.objects.get_or_create(student_num=k,
                        name=unicode(v,'utf-8'), collection=i)
                print 'created %s (%s) - %s' % (stu.name, stu.student_num, stu.collection)

