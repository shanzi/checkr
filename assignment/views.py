# Create your views here.
from django.shortcuts import render_to_response, get_object_or_404
from django.contrib.auth.decorators import login_required

from assignment.models import Assignment 
from student.models import Student
from submission.models import Submission

collections = [0, 1]

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
                title=assignment.title,
                collections=cs,
                ))

