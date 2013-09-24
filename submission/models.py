from django.db import models
from student.models import Student
from assignment.models import Assignment

class Email(models.Model):
    fromaddr = models.CharField(max_length=100)
    toaddr = models.CharField(max_length=100)
    subject = models.CharField(max_length=120)
    content = models.TextField()
    attachment_title = models.CharField(max_length=60)
    attachment_content = models.TextField()
    sent_at = models.DateTimeField()

class Submission(models.Model):
    student = models.ForeignKey(Student, related_name="submissions")
    assignment = models.ForeignKey(Assignment, related_name="assignments")
    score = models.DecimalField(max_digits=5, decimal_places=1)
    cpplint_result = models.TextField()
