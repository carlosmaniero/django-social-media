import urllib
import urllib2
import urlparse
from django.core.urlresolvers import reverse
from django.conf import settings
import models


class FacebookApi(object):

    app_id = ''
    secret_id = ''
    domain = ''

    def __init__(self, app_id, secret_id, domain):
        self.app_id = app_id
        self.secret_id = secret_id
        self.domain = domain

    def login_url(self, scope=()):
        return "https://www.facebook.com/dialog/oauth?client_id={}&" \
               "redirect_uri=http://{}{}&auth_type=rerequest&scope={}" \
            .format(self.app_id, self.domain, reverse('social_media_facebook'), ','.join(scope))

    def get_access_token(self, code):
        url = 'https://graph.facebook.com/oauth/access_token?' \
              'client_id=' + self.app_id + \
              '&client_secret=' + self.secret_id + \
              '&code=' + code + \
              '&redirect_uri=http://' + self.domain + reverse('social_media_facebook')

        f = urllib.urlopen(url)
        parsed = urlparse.parse_qs(f.read())
        return parsed['access_token'][0]

    def publish(self, message):
        data = {}
        if message.message:
            data['message'] = message.message
        if message.link:
            data['link'] = message.link

        item = models.SocialMediaProfile.objects.get(pk=1)

        url = 'https://graph.facebook.com/me/feed?access_token=' + item.fb_access_token

        data = urllib.urlencode(data)
        req = urllib2.Request(url, data)
        response = urllib2.urlopen(req)
        text = response.read()

facebook_api = FacebookApi(settings.FACEBOOK_APP_ID, settings.FACEBOOK_APP_SECRET, settings.FACEBOOK_REDIRECT_DOMAIN)