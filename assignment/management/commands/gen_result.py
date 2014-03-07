from django.core.management.base import BaseCommand, CommandError
from optparse import make_option
from student.models import Student
from assignment.models import Assignment

class Command(BaseCommand):
    option_list = BaseCommand.option_list + (
            make_option(
                '--collection',
                action='store',
                dest='collection',
                default=1,
                help='student collection'),)
    def handle(self, *args, **kwargs):
        collection = int(kwargs['collection'])
        assignments = Assignment.objects.order_by('sequence').values()
        assignments_len = len(assignments)
        students = Student.objects.filter(collection=collection).order_by('student_num').all()
        header = ['number', 'name']+range(1, assignments_len+1) + ['sum']
        print ','.join(map(str, header))
        for student in students:
            submissions = student.submissions.all()
            results = [0] * assignments_len
            sum_=0
            for submission in submissions:
                seq = submission.assignment.sequence
                if seq >0 and seq <= assignments_len:
                    old = results[seq-1]
                    new = float(submission.score)
                    if new > old:
                        results[seq-1] = new
                sum_ = sum(results)
            pres = [student.student_num, student.name.encode('utf8')] + results + [sum_]
            print ','.join(map(str, pres))
         
