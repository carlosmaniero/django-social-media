# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'SocialMediaPost'
        db.create_table(u'social_media_socialmediapost', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('message', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('link', self.gf('django.db.models.fields.URLField')(max_length=200, null=True, blank=True)),
            ('publish_at', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
        ))
        db.send_create_signal(u'social_media', ['SocialMediaPost'])

        # Adding M2M table for field networks on 'SocialMediaPost'
        m2m_table_name = db.shorten_name(u'social_media_socialmediapost_networks')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('socialmediapost', models.ForeignKey(orm[u'social_media.socialmediapost'], null=False)),
            ('networks', models.ForeignKey(orm[u'social_media.networks'], null=False))
        ))
        db.create_unique(m2m_table_name, ['socialmediapost_id', 'networks_id'])

        # Adding model 'NetWorks'
        db.create_table(u'social_media_networks', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=32)),
        ))
        db.send_create_signal(u'social_media', ['NetWorks'])


    def backwards(self, orm):
        # Deleting model 'SocialMediaPost'
        db.delete_table(u'social_media_socialmediapost')

        # Removing M2M table for field networks on 'SocialMediaPost'
        db.delete_table(db.shorten_name(u'social_media_socialmediapost_networks'))

        # Deleting model 'NetWorks'
        db.delete_table(u'social_media_networks')


    models = {
        u'social_media.networks': {
            'Meta': {'object_name': 'NetWorks'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '32'})
        },
        u'social_media.socialmediapost': {
            'Meta': {'object_name': 'SocialMediaPost'},
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