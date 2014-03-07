#!/usr/bin/env python
# encoding: utf-8

from django.core.management.base import BaseCommand, CommandError
from namelist import NAME_LIST
from student.models import Student
from assignment.models import Assignment, seq_descriptions
from datetime import datetime, timedelta
from django.utils import timezone
from optparse import make_option
import re

class Command(BaseCommand):
    option_list = BaseCommand.option_list + (
            make_option(
                '--date',
                action='store',
                dest='start_date',
                type='string',
                default=False,
                help='start date of deadline in format YYYY-mm-dd'),
            )

    def handle(self, start_date, *args, **kwargs):
        for i, lst in enumerate(NAME_LIST):
            for k, v in lst.iteritems():
                stu, created = Student.objects.get_or_create(student_num=k,
                        name=unicode(v,'utf-8'), collection=i)
                print 'created %s (%s) - %s' % (stu.name, stu.student_num, stu.collection)
        if start_date:
            start_date = datetime.strptime(start_date, '%Y-%m-%d')
            deadline = datetime(start_date.year, start_date.month, start_date.day, tzinfo=timezone.utc)
            aweek = timedelta(7)
            for n, w in enumerate(seq_descriptions, 1):
                Assignment.objects.create(
                        sequence = n,
                        title = '第%s作业' % w,
                        description = '数据结构第%s作业' % w,
                        deadline = deadline, 
                        )
                print 'Added assignment at deadline %s' % deadline.strftime('%Y-%m-%d %H:%M')
                deadline += aweek


