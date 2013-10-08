# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):

        # Changing field 'Submission.updated_at'
        db.alter_column(u'submission_submission', 'updated_at', self.gf('django.db.models.fields.DateTimeField')())
        # Adding field 'Email.message_id'
        db.add_column(u'submission_email', 'message_id',
                      self.gf('django.db.models.fields.CharField')(default='', max_length=80),
                      keep_default=False)


    def backwards(self, orm):

        # Changing field 'Submission.updated_at'
        db.alter_column(u'submission_submission', 'updated_at', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, auto_now_add=True))
        # Deleting field 'Email.message_id'
        db.delete_column(u'submission_email', 'message_id')


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
            'collection': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'student_num': ('django.db.models.fields.CharField', [], {'max_length': '20'})
        },
        u'submission.email': {
            'Meta': {'object_name': 'Email'},
            'attachment_title': ('django.db.models.fields.CharField', [], {'max_length': '60'}),
            'content': ('django.db.models.fields.TextField', [], {}),
            'fromaddr': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'message_id': ('django.db.models.fields.CharField', [], {'max_length': '80'}),
            'sent_at': ('django.db.models.fields.CharField', [], {'max_length': '80'}),
            'sent_at_parsed': ('django.db.models.fields.DateTimeField', [], {'null': 'True'}),
            'subject': ('django.db.models.fields.CharField', [], {'max_length': '120'}),
            'submission': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'mails'", 'to': u"orm['submission.Submission']"}),
            'toaddr': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'submission.file': {
            'Meta': {'object_name': 'File'},
            'content': ('django.db.models.fields.TextField', [], {}),
            'filename': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'submission': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'files'", 'to': u"orm['submission.Submission']"})
        },
        u'submission.submission': {
            'Meta': {'object_name': 'Submission'},
            'assignment': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'submissions'", 'to': u"orm['assignment.Assignment']"}),
            'cpplint_result': ('django.db.models.fields.TextField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'score': ('django.db.models.fields.DecimalField', [], {'default': '5', 'max_digits': '5', 'decimal_places': '1'}),
            'student': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'submissions'", 'to': u"orm['student.Student']"}),
            'updated_at': ('django.db.models.fields.DateTimeField', [], {})
        }
    }

    complete_apps = ['submission']