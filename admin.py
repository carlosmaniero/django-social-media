from django.conf import settings
from django.conf.urls import patterns
from django.contrib import admin
from django.forms import ModelForm, HiddenInput, ModelMultipleChoiceField
from django.http import HttpResponseRedirect
from django.utils.translation import ugettext as _
from api import facebook_api
from fields import LinkWidget
from models import SocialMediaProfile, SocialMediaPost, NetWork, NetworkPosts


class SocialMediaProfileForm(ModelForm):

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


class SocialMediaProfileAdmin(admin.ModelAdmin):
    form = SocialMediaProfileForm

    def list_view(self, request):
        # Force unique page object in admin
        item = SocialMediaProfile.objects.get_or_create(pk=1)
        return HttpResponseRedirect('/admin/social_media/socialmediaprofile/1/')

    def get_urls(self):
        urls = super(SocialMediaProfileAdmin, self).get_urls()
        my_urls = patterns('',
                           (r'^$', admin.site.admin_view(self.list_view)),
                           (r'^add/$', admin.site.admin_view(self.list_view)))

        return my_urls + urls


class SocialMediaPostForm(ModelForm):

    networks = ModelMultipleChoiceField(queryset=NetWork.objects.all())

    def save_m2m(self):
        obj = self.instance
        for network in self.cleaned_data['networks']:
            NetworkPosts.objects.create(network=network, post=obj)

    def save(self, commit=True):
        obj = super(SocialMediaPostForm, self).save(commit=True)
        return obj

    class Meta:
        model = SocialMediaPost
        exclude = ('networks',)


class SocialMediaPostAdmin(admin.ModelAdmin):
    list_display = ['message', 'link']
    list_filter = ['networks__name']
    search_fields = ['message', 'link']
    date_hierarchy = 'publish_at'
    exclude = ('fb_id', 'networks')
    form = SocialMediaPostForm

admin.site.register(SocialMediaProfile, SocialMediaProfileAdmin)
admin.site.register(SocialMediaPost, SocialMediaPostAdmin)