from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from django import forms
from django.utils import timezone
from assignment.models import Assignment
from student.models import Student
from submission.models import Submission

class AddSubmissionForm(forms.Form):
    student = forms.CharField(label="Student Number", required=True)
    assignment = forms.ModelChoiceField(label="Assignment",queryset=Assignment.objects.all(),
            required = True)
    score = forms.DecimalField(label="Store", max_digits=5, decimal_places=1,
            min_value=0.0, max_value=2.0, initial=2.0)

    def clean_student(self):
        student_num = self.cleaned_data['student']
        if not (student_num.isdigit() and len(student_num)==10):
            raise forms.ValidationError('Invalid student number: %s' % student_num)
        try:
            student = Student.objects.get(student_num=student_num)
        except Exception as e:
            raise forms.ValidationError(
            'Student with student number "%s" not found.' % student_num)
        return student 

@login_required
def add(request):
    tip = None
    if request.POST:
        form = AddSubmissionForm(request.POST)
        if form.is_valid():
            student = form.cleaned_data['student']
            assignment = form.cleaned_data['assignment']
            score = form.cleaned_data['score']
            try:
                submission = Submission.objects.get(
                        student=student,
                        assignment=assignment)
            except Exception as e:
                submission = Submission(student=student, assignment=assignment)
            submission.score = score 
            submission.updated_at = timezone.now()
            submission.save()
            tip = 'submit: %s - %s' % (student.name, assignment.title)
    else:
        form = AddSubmissionForm()
        tip = 'Add a new submission!'
        
    return render_to_response(
            'add_submission.html', 
            {'form':form,'title':'Submission::Add', 'tip':tip},
            context_instance=RequestContext(request))


@login_required
def submission(request, id_):
    submission = get_object_or_404(Submission, id=id_)
    assignment = submission.assignment
    student = submission.student
    title = "%s - %s(%s)" % (assignment.title, student.name, student.student_num)
    return render_to_response('submission.html',
            {
                'submission':submission,
                'assignment':assignment,
                'student':student,
                'title':title,
                })
