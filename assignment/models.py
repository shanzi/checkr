#!/usr/bin/env python
# encoding: utf-8

from django.db import models

# Create your models here.

seq_descriptions = [
'一',
'二',
'三',
'四',
'五',
'六',
'七',
'八',
'九',
'十',
'十一',
'十二',
'十三',
'十四',
'十五',
'十六',
'十七',
'十八',
'十九',
'二十']

seq_choices = [(i, seq_descriptions[i-1]) for i in range(1,21)]

class Assignment(models.Model):
    title = models.CharField(max_length=50)
    sequence = models.IntegerField(choices=seq_choices)
    description = models.TextField()
    deadline = models.DateTimeField()
    score_weight = models.DecimalField(max_digits=5, decimal_places=1)
    created_at = models.DateTimeField(auto_now_add=True)
