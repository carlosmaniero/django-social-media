from django.core.urlresolvers import reverse
from django.conf import settings


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
               "redirect_uri=http://{}{}&auth_type=rerequest&scope={}"\
            .format(self.app_id, self.domain, reverse('social_media_facebook'), ','.join(scope))


facebook_api = FacebookApi(settings.FACEBOOK_APP_ID, settings.FACEBOOK_APP_SECRET, settings.FACEBOOK_REDIRECT_DOMAIN)