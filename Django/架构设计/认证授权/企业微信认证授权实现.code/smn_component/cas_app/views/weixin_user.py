#! -*- coding: utf-8 -*-


# author: forcemain@163.com


import urllib
import urlparse
import requests


from django.conf import settings
from django.views.generic import View
from django.core.urlresolvers import reverse_lazy
from django.contrib.auth import authenticate, login
from itsdangerous import URLSafeTimedSerializer, BadData
from django.http import HttpResponseRedirect, HttpResponseForbidden


class WeixinUserLoginView(View):
    def get_local_scheme(self):
        return 'https' if self.request.is_secure() else 'http'

    def get_local_netloc(self):
        return self.request.get_host()

    @staticmethod
    def get_local_url():
        return reverse_lazy('cas_app:user-weixin-authenticate')

    @staticmethod
    def get_local_params():
        return ''

    def get_local_query(self):
        return urllib.urlencode({'next': self.get_next()})

    @staticmethod
    def get_local_fragment():
        return ''

    def get_local_redirect_uri(self):
        return urlparse.urlunparse((
            self.get_local_scheme(),
            self.get_local_netloc(),
            # lazy reverse
            str(self.get_local_url()),
            self.get_local_params(),
            self.get_local_query(),
            self.get_local_fragment(),
        ))

    def get_next(self):
        return self.request.GET.get('next', '/')

    def get_state(self):
        serializer = URLSafeTimedSerializer(settings.SECRET_KEY)

        return serializer.dumps(self.get_local_netloc())

    def get_weixin_code_url(self):
        url_params = urllib.urlencode({'state': self.get_state(),
                                       'appid': settings.WEIXIN_CORPID,
                                       'agentid': settings.WEIXIN_AGENTID,
                                       'redirect_uri': self.get_local_redirect_uri()})

        return '{0}?{1}'.format(settings.WEIXIN_CODE_URL, url_params)

    def get(self, request):
        if self.request.user.is_authenticated:
            return HttpResponseRedirect(self.get_next())

        return HttpResponseRedirect(self.get_weixin_code_url())


class WeixinUserAuthenticateView(View):
    def get_next(self):
        return self.request.GET.get('next', '/')

    def get_local_netloc(self):
        return self.request.get_host()

    def get_weixin_code(self):
        return self.request.GET.get('code', '')

    def get_weixin_state(self):
        return self.request.GET.get('state', '')

    def verify_weixin_state(self):
        state = self.get_weixin_state()
        try:
            serializer = URLSafeTimedSerializer(settings.SECRET_KEY)
            return serializer.loads(state) == self.get_local_netloc()
        except BadData:
            return False

    @staticmethod
    def get_weixin_access_token():
        url_params = urllib.urlencode({'corpid': settings.WEIXIN_CORPID,
                                       'corpsecret': settings.WEIXIN_SECRET})
        url = '{0}?{1}'.format(settings.WEIXIN_ACCESS_TOKEN_URL, url_params)
        response = requests.get(url)
        response.raise_for_status()

        return response.json()['access_token']

    @staticmethod
    def get_weixin_userinfo(code, access_token):
        url_params = urllib.urlencode({'code': code, 'access_token': access_token})
        url = '{0}?{1}'.format(settings.WEIXIN_USERINFO_URL, url_params)
        response = requests.get(url)
        response.raise_for_status()

        return response.json()['UserId']

    def build_local_user(self, remote_user):
        return authenticate(request=self.request, remote_user=remote_user)

    def build_weixin_user(self, code, access_token):
        remote_user = self.get_weixin_userinfo(code, access_token)

        return self.build_local_user(remote_user)

    @staticmethod
    def exp_weixin_user_not_authorize():
        return HttpResponseForbidden('Weixin user not authorize')

    @staticmethod
    def exp_invalid_state_from_weixin():
        return HttpResponseForbidden('Invalid state from weixin')

    def get(self, request):
        code = self.get_weixin_code()
        if not code:
            return self.exp_weixin_user_not_authorize()
        if not self.verify_weixin_state():
            return self.exp_invalid_state_from_weixin()
        access_token = self.get_weixin_access_token()
        user = self.build_weixin_user(code, access_token)
        login(request, user)

        return HttpResponseRedirect(self.get_next())
