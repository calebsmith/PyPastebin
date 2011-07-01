# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding field 'Code.del_date'
        db.add_column('pastey_code', 'del_date', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2011, 7, 7, 12, 48, 25, 777565)), keep_default=False)


    def backwards(self, orm):
        
        # Deleting field 'Code.del_date'
        db.delete_column('pastey_code', 'del_date')


    models = {
        'pastey.code': {
            'Meta': {'object_name': 'Code'},
            'author': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'code_paste': ('django.db.models.fields.TextField', [], {}),
            'del_date': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2011, 7, 7, 12, 48, 25, 777565)'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'language': ('django.db.models.fields.CharField', [], {'default': "'python'", 'max_length': '25', 'null': 'True', 'blank': 'True'}),
            'private': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'pub_date': ('django.db.models.fields.DateTimeField', [], {}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'})
        },
        'pastey.style': {
            'Meta': {'object_name': 'Style'},
            'highlight': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        }
    }

    complete_apps = ['pastey']
