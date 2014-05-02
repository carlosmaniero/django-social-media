import urllib
import urllib2
import urlparse
import json
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
        # Return a login URL
        return "https://www.facebook.com/dialog/oauth?client_id={}&" \
               "redirect_uri=http://{}{}&auth_type=rerequest&scope={}" \
            .format(self.app_id, self.domain, reverse('social_media_facebook'), ','.join(scope))

    def get_access_token(self, code):
        # Get a Access Token
        url = 'https://graph.facebook.com/oauth/access_token?' \
              'client_id=' + self.app_id + \
              '&client_secret=' + self.secret_id + \
              '&code=' + code + \
              '&redirect_uri=http://' + self.domain + reverse('social_media_facebook')

        f = urllib.urlopen(url)
        parsed = urlparse.parse_qs(f.read())
        return parsed['access_token'][0]

    def publish(self, message):
        """
        Publish in Facebook Feed
        :rtype : basestring (Facebook id)
        :param message: SocialMediaPost
        """
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
        ret = json.loads(response.read())

        message.fb_id = ret['id']

        return ret['id']

    def get_post(self, message):
        """
        Get Facebook Post info
        :rtype : dict
        :param message: SocialMediaPost
        """

        if message.fb_id:
            item = models.SocialMediaProfile.objects.get(pk=1)
            url = 'https://graph.facebook.com/' + message.fb_id + '?summary=true&access_token=' + item.fb_access_token
            f = urllib.urlopen(url)
            ret = json.loads(f.read())

            ret['link'] = ret.get('actions', [{}])[0].get('link')

            return ret

        return {}

    def get_post_info(self, message, info):
        if message.fb_id:
            item = models.SocialMediaProfile.objects.get(pk=1)
            url = 'https://graph.facebook.com/' + message.fb_id + '/' + info + \
                  '?summary=true&access_token=' + item.fb_access_token
            f = urllib.urlopen(url)
            ret = json.loads(f.read())

            ret['total'] = ret.get('summary', {}).get('total_count', 0)

            return ret

        return {}

    def get_likes(self, message):
        return self.get_post_info(message, 'likes')

    def get_comments(self, message):
        return self.get_post_info(message, 'comments')

facebook_api = FacebookApi(settings.FACEBOOK_APP_ID, settings.FACEBOOK_APP_SECRET, settings.FACEBOOK_REDIRECT_DOMAIN)