from django.conf import settings
from django.contrib.admin import widgets
from django.forms import ModelForm, ModelMultipleChoiceField, HiddenInput
from django.utils.translation import ugettext as _
from api import facebook_api
from fields import LinkWidget
from models import NetWork, NetworkPosts, SocialMediaPost, SocialMediaProfile


class SocialMediaProfileForm(ModelForm):
    """For to Get Access token"""
    def __init__(self, *args, **kwargs):
        super(SocialMediaProfileForm, self).__init__(*args, **kwargs)

        if not self.instance.pk:
            self.fields['fb_access_token'].widget = HiddenInput()
        else:
            self.fields['fb_access_token'].widget = LinkWidget(_('Connect with Facebook'),
                                                               facebook_api.login_url(settings.FACEBOOK_SCOPES))

            if self.instance.fb_access_token:
                self.fields['fb_access_token'].help_text = \
                    _('Current:') + ' ' + self.instance.fb_access_token[0:20] + '...'

    class Meta:
        model = SocialMediaProfile


class SocialMediaPostForm(ModelForm):
    """ Form for social media Post Form"""

    networks = ModelMultipleChoiceField(queryset=NetWork.objects.all())

    def save_m2m(self):
        obj = self.instance
        print '*' * 5
        for network in self.cleaned_data['networks']:
            NetworkPosts.objects.create(network=network, post=obj)

    def save(self, commit=True):
        obj = super(SocialMediaPostForm, self).save(commit=True)
        print obj
        print '-' * 30
        return obj

    class Meta:
        model = SocialMediaPost
        exclude = ('networks', 'fb_id')


class SocialMediaForm(SocialMediaPostForm):
    """Form to be used in another model

    pass the content_type and object id in the initial parameter.
    eg.:

    content_type = ContentType.objects.get(app_label=app_label, model=model_name)
    initial={'content_type': content_type,'object_id': object_id}

    """
    def __init__(self, *args, **kwargs):
        super(SocialMediaForm, self).__init__(*args, **kwargs)
        self.fields['publish_at'].widget = widgets.AdminSplitDateTime()
        self.fields['object_id'].widget = HiddenInput()
        self.fields['content_type'].widget = HiddenInput()