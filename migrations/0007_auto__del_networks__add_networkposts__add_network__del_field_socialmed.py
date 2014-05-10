# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting model 'NetWorks'
        db.delete_table(u'social_media_networks')

        # Adding model 'NetworkPosts'
        db.create_table(u'social_media_networkposts', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('network', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['social_media.NetWork'])),
            ('post', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['social_media.SocialMediaPost'])),
            ('network_post_id', self.gf('django.db.models.fields.CharField')(max_length=256)),
        ))
        db.send_create_signal(u'social_media', ['NetworkPosts'])

        # Adding model 'NetWork'
        db.create_table(u'social_media_network', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('network', self.gf('django.db.models.fields.CharField')(max_length=32, null=True, blank=True)),
            ('network_id', self.gf('django.db.models.fields.CharField')(max_length=32, null=True, blank=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=32, null=True, blank=True)),
            ('access_token', self.gf('django.db.models.fields.CharField')(max_length=256, null=True, blank=True)),
        ))
        db.send_create_signal(u'social_media', ['NetWork'])

        # Deleting field 'SocialMediaPost.network'
        db.delete_column(u'social_media_socialmediapost', 'network_id')


    def backwards(self, orm):
        # Adding model 'NetWorks'
        db.create_table(u'social_media_networks', (
            ('network', self.gf('django.db.models.fields.CharField')(max_length=32, null=True, blank=True)),
            ('access_token', self.gf('django.db.models.fields.CharField')(max_length=256, null=True, blank=True)),
            ('network_id', self.gf('django.db.models.fields.CharField')(max_length=32, null=True, blank=True)),
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=32, null=True, blank=True)),
        ))
        db.send_create_signal(u'social_media', ['NetWorks'])

        # Deleting model 'NetworkPosts'
        db.delete_table(u'social_media_networkposts')

        # Deleting model 'NetWork'
        db.delete_table(u'social_media_network')

        # Adding field 'SocialMediaPost.network'
        db.add_column(u'social_media_socialmediapost', 'network',
                      self.gf('django.db.models.fields.related.ForeignKey')(default='', to=orm['social_media.NetWorks']),
                      keep_default=False)


    models = {
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
            'network_post_id': ('django.db.models.fields.CharField', [], {'max_length': '256'}),
            'post': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['social_media.SocialMediaPost']"})
        },
        u'social_media.socialmediapost': {
            'Meta': {'object_name': 'SocialMediaPost'},
            'fb_id': ('django.db.models.fields.CharField', [], {'max_length': '32', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'link': ('django.db.models.fields.URLField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'message': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'network': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['social_media.NetWork']", 'through': u"orm['social_media.NetworkPosts']", 'symmetrical': 'False'}),
            'publish_at': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'})
        },
        u'social_media.socialmediaprofile': {
            'Meta': {'object_name': 'SocialMediaProfile'},
            'fb_access_token': ('django.db.models.fields.CharField', [], {'max_length': '256', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        }
    }

    complete_apps = ['social_media']