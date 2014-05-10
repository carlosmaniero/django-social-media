from __future__ import unicode_literals
from django.conf.urls import patterns, url
from django.views.decorators.csrf import csrf_exempt
from views import FacebookTokenView, CreatePublicationJson

urlpatterns = patterns('',
    url(r'^facebook_token/', csrf_exempt(FacebookTokenView.as_view()), name='social_media_facebook'),
    url(r'^publication.json', csrf_exempt(CreatePublicationJson.as_view()), name='social_media_publication_json')
)