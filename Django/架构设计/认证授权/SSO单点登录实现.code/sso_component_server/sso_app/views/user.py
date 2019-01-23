#! -*- coding: utf-8 -*-


# author: forcemain@163.com


import urlparse
import requests


from django.views import View
from django.conf import settings
from django.utils import timezone
from django.http import JsonResponse
from django.contrib.auth import login, logout
from django.contrib.auth.views import LoginView
from utils.core.view.mixin.csrf import CsrfExemptMixin
from utils.core.view.mixin.login import LoginRequiredMixin
from django.http import (
    HttpResponseBadRequest, QueryDict, HttpResponseRedirect, HttpResponseForbidden, HttpResponseNotFound
)


from .. import models


class SSOAuthenticateView(LoginRequiredMixin, View):
    @staticmethod
    def _missing_access_token_argument():
        return HttpResponseBadRequest('Access token missing')

    @staticmethod
    def _missing_redirect_to_argument():
        return HttpResponseBadRequest('Redirect_to missing')

    def get_redirect_to(self):
        return self.request.GET.get('redirect_to', None)

    @staticmethod
    def was_token_expired(sso_token):
        delta = timezone.now() - sso_token.mtime

        return delta.seconds > settings.SSO_TOKEN_EXPIRED_TIME

    def gen_access_token(self):
        token, created = models.Token.objects.get_or_create(user=self.request.user)
        if not self.was_token_expired(token):
            return token.access_token
        token.refresh()

        return token.access_token

    @staticmethod
    def do_register_site(site):
        models.Site.objects.get_or_create(url=site)

    def do_redirect(self, redirect_to):
        scheme, netloc, url, params, query, fragment = urlparse.urlparse(redirect_to)
        query_dict = QueryDict(query, mutable=True)
        query_dict['access_token'] = self.gen_access_token()
        # register site
        self.do_register_site(urlparse.urlunparse((scheme, netloc, '', '', '', '')))
        redirect_url = urlparse.urlunparse((scheme, netloc, url, params, query_dict.urlencode(), fragment))

        return HttpResponseRedirect(redirect_url)

    def get(self, request):
        redirect_to = self.get_redirect_to()
        if not redirect_to:
            return self._missing_redirect_to_argument()

        return self.do_redirect(redirect_to)


class SSOLoginView(LoginView):
    template_name = 'sso_app/login.html'

    def get_user_agent(self):
        return self.request.META.get('HTTP_USER_AGENT', '')

    def get_client_ip(self):
        x_forwarded_for = self.request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for and x_forwarded_for.split(','):
            client_ip = x_forwarded_for.split(',')[0]
        else:
            client_ip = self.request.META.get('REMOTE_ADDR')

        return client_ip or ''

    def do_trace_user(self):
        ip, user_agent = self.get_client_ip(), self.get_user_agent()
        platform, created = models.Platform.objects.get_or_create(ip=ip, endpoint=user_agent)
        user = self.request.user or None
        models.Trace.objects.create(type=models.Trace.TYPE_CHOICE_LOGIN, user=user, platform=platform,)

    def form_valid(self, form):
        login(self.request, form.get_user())
        self.do_trace_user()

        return HttpResponseRedirect(self.get_success_url())


class SSOTokenVerifyView(CsrfExemptMixin, View):
    @staticmethod
    def _invalid_access_token():
        return HttpResponseNotFound('Invalid access token')

    @staticmethod
    def _access_token_expired():
        return HttpResponseForbidden('Access token expired')

    @staticmethod
    def _missing_access_token_argument():
        return HttpResponseBadRequest('Access token missing')

    @staticmethod
    def was_token_expired(sso_token):
        delta = timezone.now() - sso_token.mtime

        return delta.seconds > settings.SSO_TOKEN_EXPIRED_TIME

    def get_access_token(self):
        return self.request.POST.get('access_token', None)

    @staticmethod
    def get_user_data(user):
        return JsonResponse({'email': user.email, 'username': user.username})

    def post(self, request):
        access_token = self.get_access_token()
        if not access_token:
            return self._missing_access_token_argument()
        try:
            token = models.Token.objects.get(access_token=access_token)
        except models.Token.DoesNotExist:
            return self._invalid_access_token()
        if self.was_token_expired(token):
            return self._access_token_expired()

        return self.get_user_data(token.user)


class SSOLogoutView(View):
    def get_next(self):
        return self.request.GET.get('next', '/')

    def get_redirect_to(self):
        return self.request.GET.get('redirect_to', None)

    def get_access_token(self):
        return self.request.GET.get('access_token', None)

    def do_local_logout(self):
        logout(self.request)

    def do_remote_logout(self, access_token):
        redirect_to = self.get_redirect_to()
        for site in models.Site.objects.all():
            url = urlparse.urljoin(site.url, settings.SSO_CLIENT_USER_LOGOUT_URL)
            try:
                requests.get(url, params={'access_token': access_token})
            except requests.exceptions.RequestException:
                pass

        return HttpResponseRedirect(redirect_to)

    def get(self, request):
        access_token = self.get_access_token()
        self.do_local_logout()
        if access_token:
            return self.do_remote_logout(access_token)

        return HttpResponseRedirect(self.get_next())
