# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting field 'Assignment.score_weight'
        db.delete_column(u'assignment_assignment', 'score_weight')


    def backwards(self, orm):
        # Adding field 'Assignment.score_weight'
        db.add_column(u'assignment_assignment', 'score_weight',
                      self.gf('django.db.models.fields.DecimalField')(default=0, max_digits=5, decimal_places=1),
                      keep_default=False)


    models = {
        u'assignment.assignment': {
            'Meta': {'object_name': 'Assignment'},
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'deadline': ('django.db.models.fields.DateTimeField', [], {}),
            'description': ('django.db.models.fields.TextField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'sequence': ('django.db.models.fields.IntegerField', [], {}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        }
    }

    complete_apps = ['assignment']