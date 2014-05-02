from django.conf import settings
from django.conf.urls import patterns
from django.contrib import admin
from django.forms import ModelForm, HiddenInput
from django.http import HttpResponseRedirect
from django.utils.translation import ugettext as _
from api import facebook_api
from fields import LinkWidget
from models import SocialMediaProfile, SocialMediaPost


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


class SocialMediaPostAdmin(admin.ModelAdmin):
    list_display = ['publish_at', 'message', 'link', 'network']
    list_filter = ['network__name']
    search_fields = ['message', 'link']
    date_hierarchy = 'publish_at'
    exclude = ('fb_id',)

admin.site.register(SocialMediaProfile, SocialMediaProfileAdmin)
admin.site.register(SocialMediaPost, SocialMediaPostAdmin)