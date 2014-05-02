from __future__ import unicode_literals
from django.db.models import Model, CharField
from django.utils.translation import ugettext as _


class SocialMediaProfile(Model):
    fb_access_token = CharField(verbose_name=_("Facebook Access Token"), max_length=256, null=True, blank=True)