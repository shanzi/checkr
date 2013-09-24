# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Email'
        db.create_table(u'submission_email', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('fromaddr', self.gf('django.db.models.fields.EmailField')(max_length=75)),
            ('toaddr', self.gf('django.db.models.fields.EmailField')(max_length=75)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=120)),
            ('content', self.gf('django.db.models.fields.TextField')()),
            ('attachment_title', self.gf('django.db.models.fields.CharField')(max_length=60)),
            ('attachment_content', self.gf('django.db.models.fields.TextField')()),
            ('sent_at', self.gf('django.db.models.fields.DateTimeField')()),
        ))
        db.send_create_signal(u'submission', ['Email'])

        # Adding model 'Submission'
        db.create_table(u'submission_submission', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('student', self.gf('django.db.models.fields.related.ForeignKey')(related_name='submissions', to=orm['student.Student'])),
            ('assignment', self.gf('django.db.models.fields.related.ForeignKey')(related_name='assignments', to=orm['assignment.Assignment'])),
            ('score', self.gf('django.db.models.fields.DecimalField')(max_digits=5, decimal_places=1)),
            ('cpplint_result', self.gf('django.db.models.fields.TextField')()),
        ))
        db.send_create_signal(u'submission', ['Submission'])


    def backwards(self, orm):
        # Deleting model 'Email'
        db.delete_table(u'submission_email')

        # Deleting model 'Submission'
        db.delete_table(u'submission_submission')


    models = {
        u'assignment.assignment': {
            'Meta': {'object_name': 'Assignment'},
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'deadline': ('django.db.models.fields.DateTimeField', [], {}),
            'description': ('django.db.models.fields.TextField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'score_weight': ('django.db.models.fields.DecimalField', [], {'max_digits': '5', 'decimal_places': '1'}),
            'sequence': ('django.db.models.fields.IntegerField', [], {}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        u'student.student': {
            'Meta': {'object_name': 'Student'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'student_num': ('django.db.models.fields.CharField', [], {'max_length': '20'})
        },
        u'submission.email': {
            'Meta': {'object_name': 'Email'},
            'attachment_content': ('django.db.models.fields.TextField', [], {}),
            'attachment_title': ('django.db.models.fields.CharField', [], {'max_length': '60'}),
            'content': ('django.db.models.fields.TextField', [], {}),
            'fromaddr': ('django.db.models.fields.EmailField', [], {'max_length': '75'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'sent_at': ('django.db.models.fields.DateTimeField', [], {}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '120'}),
            'toaddr': ('django.db.models.fields.EmailField', [], {'max_length': '75'})
        },
        u'submission.submission': {
            'Meta': {'object_name': 'Submission'},
            'assignment': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'assignments'", 'to': u"orm['assignment.Assignment']"}),
            'cpplint_result': ('django.db.models.fields.TextField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'score': ('django.db.models.fields.DecimalField', [], {'max_digits': '5', 'decimal_places': '1'}),
            'student': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'submissions'", 'to': u"orm['student.Student']"})
        }
    }

    complete_apps = ['submission']