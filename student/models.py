from django.db import models

class Student(models.Model):
    name = models.CharField(max_length=30)
    student_num = models.CharField(max_length=20)
    collection = models.IntegerField(default=0)

    def __unicode__(self):
        return u"%s (%s) (%s)" % (self.name, self.student_num, self.collection)
