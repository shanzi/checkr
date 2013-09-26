# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'File'
        db.create_table(u'submission_file', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('filename', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('content', self.gf('django.db.models.fields.TextField')()),
            ('submission', self.gf('django.db.models.fields.related.ForeignKey')(related_name='files', to=orm['submission.Submission'])),
        ))
        db.send_create_signal(u'submission', ['File'])

        # Deleting field 'Email.attachment_content'
        db.delete_column(u'submission_email', 'attachment_content')

        # Adding field 'Email.submission'
        db.add_column(u'submission_email', 'submission',
                      self.gf('django.db.models.fields.related.ForeignKey')(default=0, related_name='mails', to=orm['submission.Submission']),
                      keep_default=False)


        # Changing field 'Email.sent_at'
        db.alter_column(u'submission_email', 'sent_at', self.gf('django.db.models.fields.CharField')(max_length=80))

    def backwards(self, orm):
        # Deleting model 'File'
        db.delete_table(u'submission_file')

        # Adding field 'Email.attachment_content'
        db.add_column(u'submission_email', 'attachment_content',
                      self.gf('django.db.models.fields.TextField')(default=''),
                      keep_default=False)

        # Deleting field 'Email.submission'
        db.delete_column(u'submission_email', 'submission_id')


        # Changing field 'Email.sent_at'
        db.alter_column(u'submission_email', 'sent_at', self.gf('django.db.models.fields.DateTimeField')())

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
            'attachment_title': ('django.db.models.fields.CharField', [], {'max_length': '60'}),
            'content': ('django.db.models.fields.TextField', [], {}),
            'fromaddr': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'sent_at': ('django.db.models.fields.CharField', [], {'max_length': '80'}),
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
            'assignment': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'assignments'", 'to': u"orm['assignment.Assignment']"}),
            'cpplint_result': ('django.db.models.fields.TextField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'score': ('django.db.models.fields.DecimalField', [], {'default': '5', 'max_digits': '5', 'decimal_places': '1'}),
            'student': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'submissions'", 'to': u"orm['student.Student']"})
        }
    }

    complete_apps = ['submission']