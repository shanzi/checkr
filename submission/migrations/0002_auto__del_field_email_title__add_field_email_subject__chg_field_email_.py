# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting field 'Email.title'
        db.delete_column(u'submission_email', 'title')

        # Adding field 'Email.subject'
        db.add_column(u'submission_email', 'subject',
                      self.gf('django.db.models.fields.CharField')(default='', max_length=120),
                      keep_default=False)


        # Changing field 'Email.fromaddr'
        db.alter_column(u'submission_email', 'fromaddr', self.gf('django.db.models.fields.CharField')(max_length=100))

        # Changing field 'Email.toaddr'
        db.alter_column(u'submission_email', 'toaddr', self.gf('django.db.models.fields.CharField')(max_length=100))

    def backwards(self, orm):
        # Adding field 'Email.title'
        db.add_column(u'submission_email', 'title',
                      self.gf('django.db.models.fields.CharField')(default='', max_length=120),
                      keep_default=False)

        # Deleting field 'Email.subject'
        db.delete_column(u'submission_email', 'subject')


        # Changing field 'Email.fromaddr'
        db.alter_column(u'submission_email', 'fromaddr', self.gf('django.db.models.fields.EmailField')(max_length=75))

        # Changing field 'Email.toaddr'
        db.alter_column(u'submission_email', 'toaddr', self.gf('django.db.models.fields.EmailField')(max_length=75))

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
            'fromaddr': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'sent_at': ('django.db.models.fields.DateTimeField', [], {}),
            'subject': ('django.db.models.fields.CharField', [], {'max_length': '120'}),
            'toaddr': ('django.db.models.fields.CharField', [], {'max_length': '100'})
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