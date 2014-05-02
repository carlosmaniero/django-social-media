# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting field 'SocialMediaPost.facebook_id'
        db.delete_column(u'social_media_socialmediapost', 'facebook_id')

        # Adding field 'SocialMediaPost.fb_id'
        db.add_column(u'social_media_socialmediapost', 'fb_id',
                      self.gf('django.db.models.fields.CharField')(max_length=32, null=True, blank=True),
                      keep_default=False)


    def backwards(self, orm):
        # Adding field 'SocialMediaPost.facebook_id'
        db.add_column(u'social_media_socialmediapost', 'facebook_id',
                      self.gf('django.db.models.fields.CharField')(max_length=32, null=True, blank=True),
                      keep_default=False)

        # Deleting field 'SocialMediaPost.fb_id'
        db.delete_column(u'social_media_socialmediapost', 'fb_id')


    models = {
        u'social_media.networks': {
            'Meta': {'object_name': 'NetWorks'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '32'})
        },
        u'social_media.socialmediapost': {
            'Meta': {'object_name': 'SocialMediaPost'},
            'fb_id': ('django.db.models.fields.CharField', [], {'max_length': '32', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'link': ('django.db.models.fields.URLField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'message': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'networks': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['social_media.NetWorks']", 'symmetrical': 'False'}),
            'publish_at': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'})
        },
        u'social_media.socialmediaprofile': {
            'Meta': {'object_name': 'SocialMediaProfile'},
            'fb_access_token': ('django.db.models.fields.CharField', [], {'max_length': '256', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        }
    }

    complete_apps = ['social_media']