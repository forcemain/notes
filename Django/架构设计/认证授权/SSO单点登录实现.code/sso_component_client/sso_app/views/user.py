#! -*- coding: utf-8 -*-


# author: forcemain@163.com


import urllib
import urlparse
import requests


from django.views import View
from django.conf import settings
from importlib import import_module
from django.core.urlresolvers import reverse_lazy
from django.contrib.auth import authenticate, get_user_model, login, logout
from django.http import HttpResponseBadRequest, HttpResponseRedirect, HttpResponseForbidden


from .. import models


UserModel = get_user_model()


class SSOAuthenticateView(View):
    @staticmethod
    def _missing_access_token_argument():
        return HttpResponseBadRequest('Access token missing')

    def get_access_token(self):
        return self.request.GET.get('access_token', None)

    @staticmethod
    def get_user_data(access_token):
        url = '{0}{1}'.format(settings.SSO_SERVER_BSAE_URL, settings.SSO_SERVER_TOKEN_VERIFY_URL)
        response = requests.post(url, {'access_token': access_token})

        return response.json()

    def get_next(self):
        return self.request.GET.get('next', '/')

    def synchronous_user(self, user_data):
        remote_user = user_data[UserModel.USERNAME_FIELD]

        return authenticate(self.request, remote_user=remote_user)

    def build_user_object(self, access_token):
        user_data = self.get_user_data(access_token)

        return self.synchronous_user(user_data)

    def do_create_user_token(self, access_token):
        models.Token.objects.update_or_create(defaults={'access_token': access_token}, user=self.request.user)

    def do_create_user_session(self):
        session_key = self.request.session.session_key
        models.Session.objects.get_or_create(session_key=session_key, user=self.request.user)

    def get(self, request):
        access_token = self.get_access_token()
        if not access_token:
            return self._missing_access_token_argument()
        user = self.build_user_object(access_token)
        login(request, user)
        # create user token
        self.do_create_user_token(access_token)
        # create user session
        self.do_create_user_session()

        return HttpResponseRedirect(self.get_next())


class SSOLoginView(View):
    def get_next(self):
        return self.request.GET.get('next', '/')

    def get_scheme(self):
        return 'https' if self.request.is_secure() else 'http'

    def get_netloc(self):
        return self.request.get_host()

    @staticmethod
    def get_url():
        return reverse_lazy('sso_app:sso-authenticate')

    @staticmethod
    def get_params():
        return ''

    def get_query(self):
        return urllib.urlencode({'next': self.get_next()})

    @staticmethod
    def get_fragment():
        return ''

    def get_redirect_to(self):
        redirect_url = urlparse.urlunparse((
            self.get_scheme(),
            self.get_netloc(),
            # for lazy obj
            str(self.get_url()),
            self.get_params(),
            self.get_query(),
            self.get_fragment(),
        ))

        return redirect_url

    @staticmethod
    def do_remote_login(redirect_to):
        redirect_url = '{0}{1}?{2}'.format(settings.SSO_SERVER_BSAE_URL,
                                           settings.SSO_SERVER_AUTHENTICATE_URL,
                                           urllib.urlencode({'redirect_to': redirect_to}))

        return HttpResponseRedirect(redirect_url)

    def get(self, request):
        if self.request.user.is_authenticated:
            return HttpResponseRedirect(self.get_next())
        redirect_to = self.get_redirect_to()

        return self.do_remote_login(redirect_to)


class SSOLogoutView(View):
    @staticmethod
    def _invalid_access_token():
        return HttpResponseForbidden('Invalid access token')

    @staticmethod
    def _anonymous_user_not_allowed():
        return HttpResponseForbidden('Anonymous user not allowed')

    def get_next(self):
        return self.request.GET.get('next', '/')

    def get_scheme(self):
        return 'https' if self.request.is_secure() else 'http'

    def get_netloc(self):
        return self.request.get_host()

    @staticmethod
    def get_url():
        return ''

    @staticmethod
    def get_params():
        return ''

    def get_query(self):
        return urllib.urlencode({'next': self.get_next()})

    @staticmethod
    def get_fragment():
        return ''

    def get_access_token(self):
        return self.request.GET.get('access_token', None)

    @staticmethod
    def do_clean_user_token(user):
        user.user_tokens.all().delete()

    @staticmethod
    def do_clean_user_session(user):
        engine = import_module(settings.SESSION_ENGINE)
        session = engine.SessionStore()
        for user_session in user.user_sessions.all():
            session.delete(user_session.session_key)
            user_session.delete()

    def do_local_logout(self, access_token):
        try:
            user = models.Token.objects.get(access_token=access_token).user
        except (models.Token.DoesNotExist, AttributeError):
            return self._invalid_access_token()
        # clean user token
        self.do_clean_user_token(user)
        # clean user session
        self.do_clean_user_session(user)

        return HttpResponseRedirect(self.get_next())

    def get_redirect_to(self):
        redirect_url = urlparse.urlunparse((
            self.get_scheme(),
            self.get_netloc(),
            # for lazy obj
            str(self.get_url()),
            self.get_params(),
            self.get_query(),
            self.get_fragment(),
        ))

        return redirect_url

    def do_remote_logout(self, access_token):
        url_params = {'access_token': access_token, 'redirect_to': self.get_redirect_to}
        redirect_url = '{0}{1}?{2}'.format(settings.SSO_SERVER_BSAE_URL,
                                           settings.SSO_SERVER_USER_LOGOUT_URL,
                                           urllib.urlencode(url_params))

        return HttpResponseRedirect(redirect_url)

    def get(self, request):
        access_token = self.get_access_token()
        if access_token:
            return self.do_local_logout(access_token)
        if not request.user.is_authenticated:
            return self._anonymous_user_not_allowed()
        access_token = request.user.user_tokens.first().access_token

        return self.do_remote_logout(access_token)
