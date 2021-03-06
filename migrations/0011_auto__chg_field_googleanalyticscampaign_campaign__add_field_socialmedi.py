# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):

        # Changing field 'GoogleAnalyticsCampaign.campaign'
        db.alter_column(u'social_media_googleanalyticscampaign', 'campaign', self.gf('django.db.models.fields.CharField')(default='', max_length=64))
        # Adding field 'SocialMediaPost.campaign'
        db.add_column(u'social_media_socialmediapost', 'campaign',
                      self.gf('django.db.models.fields.related.ForeignKey')(to=orm['social_media.GoogleAnalyticsCampaign'], null=True, blank=True),
                      keep_default=False)


    def backwards(self, orm):

        # Changing field 'GoogleAnalyticsCampaign.campaign'
        db.alter_column(u'social_media_googleanalyticscampaign', 'campaign', self.gf('django.db.models.fields.CharField')(max_length=64, null=True))
        # Deleting field 'SocialMediaPost.campaign'
        db.delete_column(u'social_media_socialmediapost', 'campaign_id')


    models = {
        u'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'social_media.googleanalyticscampaign': {
            'Meta': {'object_name': 'GoogleAnalyticsCampaign'},
            'campaign': ('django.db.models.fields.CharField', [], {'max_length': '64'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '128', 'null': 'True', 'blank': 'True'})
        },
        u'social_media.network': {
            'Meta': {'ordering': "[u'network', u'name']", 'object_name': 'NetWork'},
            'access_token': ('django.db.models.fields.CharField', [], {'max_length': '256', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '32', 'null': 'True', 'blank': 'True'}),
            'network': ('django.db.models.fields.CharField', [], {'max_length': '32', 'null': 'True', 'blank': 'True'}),
            'network_id': ('django.db.models.fields.CharField', [], {'max_length': '32', 'null': 'True', 'blank': 'True'})
        },
        u'social_media.networkposts': {
            'Meta': {'object_name': 'NetworkPosts'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'network': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['social_media.NetWork']"}),
            'network_post_id': ('django.db.models.fields.CharField', [], {'max_length': '256', 'null': 'True', 'blank': 'True'}),
            'post': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['social_media.SocialMediaPost']"})
        },
        u'social_media.socialmediapost': {
            'Meta': {'object_name': 'SocialMediaPost'},
            'campaign': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['social_media.GoogleAnalyticsCampaign']", 'null': 'True', 'blank': 'True'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['contenttypes.ContentType']", 'null': 'True', 'blank': 'True'}),
            'fb_id': ('django.db.models.fields.CharField', [], {'max_length': '32', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'link': ('django.db.models.fields.URLField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'message': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'networks': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['social_media.NetWork']", 'through': u"orm['social_media.NetworkPosts']", 'symmetrical': 'False'}),
            'object_id': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'publish_at': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'})
        },
        u'social_media.socialmediaprofile': {
            'Meta': {'object_name': 'SocialMediaProfile'},
            'fb_access_token': ('django.db.models.fields.CharField', [], {'max_length': '256', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        }
    }

    complete_apps = ['social_media']