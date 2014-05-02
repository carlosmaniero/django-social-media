from __future__ import unicode_literals
from django.http import HttpResponse, HttpResponseRedirect
from django.views.generic import View
from models import SocialMediaProfile


class FacebookTokenView(View):

    def get(self, request, *args, **kwargs):
        if request.user.is_staff:
            item = SocialMediaProfile.objects.get(pk=1)
            item.fb_access_token = request.GET['code']
            item.save()
            return HttpResponseRedirect('/admin/social_media/socialmediaprofile/1/')