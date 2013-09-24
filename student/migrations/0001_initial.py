# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Student'
        db.create_table(u'student_student', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=30)),
            ('student_num', self.gf('django.db.models.fields.CharField')(max_length=20)),
        ))
        db.send_create_signal(u'student', ['Student'])


    def backwards(self, orm):
        # Deleting model 'Student'
        db.delete_table(u'student_student')


    models = {
        u'student.student': {
            'Meta': {'object_name': 'Student'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'student_num': ('django.db.models.fields.CharField', [], {'max_length': '20'})
        }
    }

    complete_apps = ['student']