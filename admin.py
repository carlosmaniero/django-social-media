from django.conf import settings
from django.conf.urls import patterns
from django.contrib import admin
from django.contrib.admin import widgets
from django.contrib.contenttypes.generic import GenericStackedInline
from django.contrib.contenttypes.models import ContentType
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
        exclude = ('networks', 'fb_id')


class SocialMediaPostAdmin(admin.ModelAdmin):
    list_display = ['message', 'link']
    list_filter = ['networks__name']
    search_fields = ['message', 'link']
    date_hierarchy = 'publish_at'
    exclude = ('fb_id', 'networks')
    form = SocialMediaPostForm


class SocialMediaInline(GenericStackedInline):
    model = SocialMediaPost
    form = SocialMediaPostForm
    extra = 1


class SocialMediaForm(SocialMediaPostForm):
    def __init__(self, *args, **kwargs):
        super(SocialMediaForm, self).__init__(*args, **kwargs)
        self.fields['publish_at'].widget = widgets.AdminSplitDateTime()
        self.fields['object_id'].widget = HiddenInput()
        self.fields['content_type'].widget = HiddenInput()


class SocialMediaMixin(object):
    change_form_template = 'admin/social_media/change_form.html'

    class Media:
        css = {
            'all': ('css/social_media.css',)
        }

    def change_view(self, request, object_id, form_url='', extra_context=None):
        extra_context = extra_context or {}
        extra_context['share_form'] = SocialMediaForm(initial={
            'content_type': ContentType.objects.get(app_label=self.opts.app_label, model=self.opts.model_name),
            'object_id': object_id,
            'link': 'http://' + settings.FACEBOOK_REDIRECT_DOMAIN + self.model.objects.get(pk=object_id).get_absolute_url()})

        return super(SocialMediaMixin, self).change_view(request, object_id, form_url=form_url, extra_context=extra_context)


admin.site.register(SocialMediaProfile, SocialMediaProfileAdmin)
admin.site.register(SocialMediaPost, SocialMediaPostAdmin)