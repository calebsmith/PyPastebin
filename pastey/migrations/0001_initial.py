# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'Code'
        db.create_table('pastey_code', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('code_paste', self.gf('django.db.models.fields.TextField')()),
            ('language', self.gf('django.db.models.fields.CharField')(default='python', max_length=25, null=True, blank=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=50, null=True, blank=True)),
            ('author', self.gf('django.db.models.fields.CharField')(max_length=50, null=True, blank=True)),
            ('email', self.gf('django.db.models.fields.EmailField')(max_length=50, null=True, blank=True)),
            ('private', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('pub_date', self.gf('django.db.models.fields.DateTimeField')()),
            ('del_date', self.gf('django.db.models.fields.DateTimeField')()),
        ))
        db.send_create_signal('pastey', ['Code'])

        # Adding model 'Style'
        db.create_table('pastey_style', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('highlight', self.gf('django.db.models.fields.CharField')(max_length=50, null=True, blank=True)),
        ))
        db.send_create_signal('pastey', ['Style'])


    def backwards(self, orm):
        
        # Deleting model 'Code'
        db.delete_table('pastey_code')

        # Deleting model 'Style'
        db.delete_table('pastey_style')


    models = {
        'pastey.code': {
            'Meta': {'object_name': 'Code'},
            'author': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'code_paste': ('django.db.models.fields.TextField', [], {}),
            'del_date': ('django.db.models.fields.DateTimeField', [], {}),
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
