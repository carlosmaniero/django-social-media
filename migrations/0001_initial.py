# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'SocialMediaProfile'
        db.create_table(u'social_media_socialmediaprofile', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('fb_access_token', self.gf('django.db.models.fields.CharField')(max_length=256, null=True, blank=True)),
        ))
        db.send_create_signal(u'social_media', ['SocialMediaProfile'])


    def backwards(self, orm):
        # Deleting model 'SocialMediaProfile'
        db.delete_table(u'social_media_socialmediaprofile')


    models = {
        u'social_media.socialmediaprofile': {
            'Meta': {'object_name': 'SocialMediaProfile'},
            'fb_access_token': ('django.db.models.fields.CharField', [], {'max_length': '256', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        }
    }

    complete_apps = ['social_media']