from __future__ import unicode_literals
import json
from django.core.exceptions import PermissionDenied
from django.http import HttpResponseRedirect, HttpResponse
from django.utils.translation import ugettext as _
from django.views.generic import View
from api import facebook_api, FacebookException
from forms import SocialMediaForm
from models import SocialMediaProfile


class FacebookTokenView(View):

    def get(self, request, *args, **kwargs):
        if request.user and request.user.is_staff:
            item = SocialMediaProfile.objects.get(pk=1)

            item.fb_access_token = facebook_api.get_access_token(request.GET['code'])
            facebook_api.get_pages()
            item.save()

            return HttpResponseRedirect('/admin/social_media/socialmediaprofile/1/')

        return PermissionDenied()


class CreatePublicationJson(View):

    def post(self, request, *args, **kwargs):
        if request.user and request.user.is_staff:
            form = SocialMediaForm(request.POST)

            if form.is_valid():
                obj = form.save(commit=True)

                try:
                    form.save_m2m()
                except FacebookException as e:
                    return HttpResponse(json.dumps({'error': _('Unable to post on') + ' ' + e.network.name}),
                                        status=500, content_type="application/json")
                except Exception as e:
                    return HttpResponse(json.dumps({'error': _('Unable to perform all publications')}),
                                        status=500, content_type="application/json")

                return HttpResponse(json.dumps({'post': obj.pk}), content_type="application/json")

            return HttpResponse(json.dumps({'error': form.errors}), content_type="application/json")

        else:
            return HttpResponse(json.dumps({'error': 'Access Denied'}), status=403, content_type="application/json")