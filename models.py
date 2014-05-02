from __future__ import unicode_literals
from django.contrib import messages

from django.db.models import Model, CharField, TextField, URLField, DateTimeField, ManyToManyField
from django.utils.translation import ugettext as _
from django.db.models.signals import pre_save

from api import facebook_api


class SocialMediaProfile(Model):
    fb_access_token = CharField(verbose_name=_("Facebook Access Token"), max_length=256, null=True, blank=True)


class NetWorks(Model):
    name = CharField(max_length=32)

    def __str__(self):
        return self.name

    def __unicode__(self):
        return self.__str__()


class SocialMediaPost(Model):
    message = TextField(verbose_name=_("Publication text"), null=True, blank=True)
    link = URLField(verbose_name=_('Post URL'), null=True, blank=True)
    publish_at = DateTimeField(verbose_name=_('Publish at'), null=True, blank=True, help_text=_("Blank to now"))
    networks = ManyToManyField(NetWorks)
    facebook_id = CharField(max_length=32, null=True, blank=True)


def publish_now(sender, **kwargs):
    # the object which is saved can be accessed via kwargs 'instance' key.
    obj = kwargs['instance']
    if not obj.publish_at:

        try:
            facebook_api.publish(obj)
        except Exception as e:
            messages.error(_('Facebok API error:' + ' ' + e.message))

pre_save.connect(publish_now, sender=SocialMediaPost)

