from __future__ import unicode_literals
from django.contrib.contenttypes.generic import GenericForeignKey
from django.contrib.contenttypes.models import ContentType

from django.db.models import Model, CharField, TextField, URLField, DateTimeField, ManyToManyField, ForeignKey, \
    PositiveIntegerField
from django.utils.translation import ugettext as _
from django.db.models.signals import pre_save
from exept import FacebookException


class SocialMediaProfile(Model):
    fb_access_token = CharField(verbose_name=_("Facebook Access Token"), max_length=256, null=True, blank=True)


class NetWork(Model):
    """Networks Model

    Networks are the chanel of you will post
    """
    FACEBOOK = 'Facebook'
    network = CharField(max_length=32, null=True, blank=True)
    network_id = CharField(max_length=32, null=True, blank=True)
    name = CharField(max_length=32, null=True, blank=True)
    access_token = CharField(max_length=256, null=True, blank=True)

    class Meta:
        ordering = ['network', 'name']

    def __str__(self):
        return "{}: {}".format(self.network, self.name)

    def __unicode__(self):
        return self.__str__()


class NetworkPosts(Model):
    network = ForeignKey(NetWork)
    post = ForeignKey('SocialMediaPost')
    network_post_id = CharField(max_length=256, null=True, blank=True)
    _fb_data = None
    _fb_likes = None
    _fb_comments = None
    _fb_shares = None

    @property
    def fb_data(self):
        from api import facebook_api
        if not self._fb_data:
            self._fb_data = facebook_api.get_post(self)
        return self._fb_data

    @property
    def fb_likes(self):
        from api import facebook_api
        if not self._fb_likes:
            self._fb_likes = facebook_api.get_likes(self)
        return self._fb_likes

    @property
    def fb_comments(self):
        from api import facebook_api
        if not self._fb_comments:
            return facebook_api.get_comments(self)
        return self._fb_comments

    @property
    def fb_shares(self):
        from api import facebook_api
        if not self._fb_shares:
            return facebook_api.get_shares(self)
        return self._fb_shares


class GoogleAnalyticsCampaign(Model):
    title = CharField(verbose_name=_('Title of the campaign'), max_length=128, null=True, blank=True)
    campaign = CharField(verbose_name=_('Name of campaign'), max_length=64,
                         help_text=_('Use only character, numbers and underscore.'))

    def __unicode__(self):
        return '[{}] - {}'.format(self.campaign, self.title)


class SocialMediaPost(Model):
    message = TextField(verbose_name=_("Publication text"), null=True, blank=True)
    link = URLField(verbose_name=_('Post URL'), null=True, blank=True)
    publish_at = DateTimeField(verbose_name=_('Publish at'), null=True, blank=True, help_text=_("Blank to now"))
    networks = ManyToManyField(NetWork, through=NetworkPosts)
    fb_id = CharField(max_length=32, null=True, blank=True)
    content_type = ForeignKey(ContentType, null=True, blank=True)
    object_id = PositiveIntegerField(null=True, blank=True)
    content_object = GenericForeignKey('content_type', 'object_id')
    campaign = ForeignKey(GoogleAnalyticsCampaign, null=True, blank=True)

    def get_networks(self):
        return NetworkPosts.objects.filter(post=self)


def publish_now(sender, **kwargs):
    # the object which is saved can be accessed via kwargs 'instance' key.
    obj = kwargs['instance']

    if not obj.post.publish_at:
        try:
            from api import FacebookApi

            if obj.network.network == 'Facebook':

                access_token = ''
                if obj.network.network_id != 'me':
                    access_token = obj.network.access_token

                facebook_api = FacebookApi(access_token=access_token, user_id=obj.network.network_id)
                facebook_api.publish(obj, obj.post)

        except FacebookException as e:
            raise e
        except Exception as e:
            raise e

pre_save.connect(publish_now, sender=NetworkPosts)

