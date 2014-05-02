# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'NetWorks.network'
        db.add_column(u'social_media_networks', 'network',
                      self.gf('django.db.models.fields.CharField')(max_length=32, null=True, blank=True),
                      keep_default=False)

        # Adding field 'NetWorks.network_id'
        db.add_column(u'social_media_networks', 'network_id',
                      self.gf('django.db.models.fields.CharField')(max_length=32, null=True, blank=True),
                      keep_default=False)

        # Adding field 'NetWorks.access_token'
        db.add_column(u'social_media_networks', 'access_token',
                      self.gf('django.db.models.fields.CharField')(max_length=256, null=True, blank=True),
                      keep_default=False)


        # Changing field 'NetWorks.name'
        db.alter_column(u'social_media_networks', 'name', self.gf('django.db.models.fields.CharField')(max_length=32, null=True))

    def backwards(self, orm):
        # Deleting field 'NetWorks.network'
        db.delete_column(u'social_media_networks', 'network')

        # Deleting field 'NetWorks.network_id'
        db.delete_column(u'social_media_networks', 'network_id')

        # Deleting field 'NetWorks.access_token'
        db.delete_column(u'social_media_networks', 'access_token')


        # Changing field 'NetWorks.name'
        db.alter_column(u'social_media_networks', 'name', self.gf('django.db.models.fields.CharField')(default='', max_length=32))

    models = {
        u'social_media.networks': {
            'Meta': {'object_name': 'NetWorks'},
            'access_token': ('django.db.models.fields.CharField', [], {'max_length': '256', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '32', 'null': 'True', 'blank': 'True'}),
            'network': ('django.db.models.fields.CharField', [], {'max_length': '32', 'null': 'True', 'blank': 'True'}),
            'network_id': ('django.db.models.fields.CharField', [], {'max_length': '32', 'null': 'True', 'blank': 'True'})
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