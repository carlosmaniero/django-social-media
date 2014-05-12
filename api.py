import urllib
import urllib2
import urlparse
import json
from django.core.urlresolvers import reverse
from django.conf import settings
from exept import FacebookException
import models


class FacebookApi(object):

    app_id = ''
    secret_id = ''
    domain = ''
    access_token = ''
    user_id = ''

    def __init__(self, app_id='', secret_id='', domain='', access_token='', user_id='me'):
        self.app_id = app_id or settings.FACEBOOK_APP_ID
        self.secret_id = secret_id or settings.FACEBOOK_APP_SECRET
        self.domain = domain or settings.FACEBOOK_REDIRECT_DOMAIN
        self.access_token = access_token
        self.user_id = user_id

        if not access_token:
            item, created = models.SocialMediaProfile.objects.get_or_create(pk=1)
            self.access_token = item.fb_access_token

    def login_url(self, scopes=()):

        scopes = scopes or settings.FACEBOOK_SCOPES

        # Return a login URL
        return "https://www.facebook.com/dialog/oauth?client_id={}&" \
               "redirect_uri=http://{}{}&auth_type=rerequest&scope={}" \
            .format(self.app_id, self.domain, reverse('social_media_facebook'), ','.join(scopes))

    def get_access_token(self, code):
        # Get a Access Token
        url = 'https://graph.facebook.com/oauth/access_token?' \
              'client_id=' + self.app_id + \
              '&client_secret=' + self.secret_id + \
              '&code=' + code + \
              '&redirect_uri=http://' + self.domain + reverse('social_media_facebook')

        f = urllib.urlopen(url)
        parsed = urlparse.parse_qs(f.read())
        self.access_token = parsed['access_token'][0]
        return self.access_token

    def publish(self, obj, message):
        """
        Publish in Facebook Feed
        :rtype : basestring (Facebook id)
        :param message: SocialMediaPost
        """
        data = {}
        if message.message:
            data['message'] = message.message
        if message.link:
            data['link'] = "{}?utm_source=facebook&utm_medium={}".format(message.link, self.user_id)

            if message.campaign:
                data['link'] += '&utm_campaign=' + message.campaign.campaign

        url = 'https://graph.facebook.com/' + self.user_id + '/feed?access_token=' + self.access_token

        try:
            data = urllib.urlencode(data)
            req = urllib2.Request(url, data)
            response = urllib2.urlopen(req)
            ret = json.loads(response.read())
        except Exception as e:
            raise FacebookException(e.message, self.user_id)

        obj.network_post_id = ret['id']

        return ret['id']

    def get_post(self, message):
        """
        Get Facebook Post info
        :rtype : dict
        :param message: SocialMediaPost
        """

        if message.network_post_id:
            url = 'https://graph.facebook.com/' + message.network_post_id + '?summary=true&access_token=' + self.access_token
            f = urllib.urlopen(url)
            ret = json.loads(f.read())

            ret['link'] = ret.get('actions', [{}])[0].get('link')

            return ret

        return {}

    def get_post_info(self, message, info):
        if message.network_post_id:
            item = models.SocialMediaProfile.objects.get(pk=1)
            url = 'https://graph.facebook.com/' + message.network_post_id + '/' + info + \
                  '?summary=true&access_token=' + self.access_token
            f = urllib.urlopen(url)
            ret = json.loads(f.read())

            ret['total'] = ret.get('summary', {}).get('total_count', 0)

            return ret

        return {}

    def get_likes(self, message):
        return self.get_post_info(message, 'likes')

    def get_comments(self, message):
        return self.get_post_info(message, 'comments')

    def get_pages(self):
        url = 'https://graph.facebook.com/me/accounts?access_token=' + self.access_token
        f = urllib.urlopen(url)
        ret = json.loads(f.read())

        for page in ret['data']:
            obj, created = models.NetWork.objects.get_or_create(network_id=page['id'], network='Facebook')
            obj.network_id = page['id']
            obj.name = page['name']
            obj.access_token = page['access_token']
            obj.network = 'Facebook'

            obj.save()

        return ret

facebook_api = FacebookApi(settings.FACEBOOK_APP_ID, settings.FACEBOOK_APP_SECRET, settings.FACEBOOK_REDIRECT_DOMAIN)