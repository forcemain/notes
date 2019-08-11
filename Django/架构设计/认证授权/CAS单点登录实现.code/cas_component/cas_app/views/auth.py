#! -*- coding: utf-8 -*-


# author: forcemain@163.com


import urllib
import urlparse


from django.conf import settings
from django.utils import timezone
from django.views.generic import View
from webservices.models import Provider
from itsdangerous import TimedSerializer
from django.utils.translation import ugettext_lazy as _
from utils.core.overrite.webservices.sync import provider_for_django
from django.http import HttpResponseBadRequest, HttpResponseForbidden, HttpResponseRedirect, QueryDict


from .. import models


class CasBaseProvider(Provider):
    max_age = settings.CAS_SIGNATURE_MAX_AGE

    def provide(self, data):
        raise NotImplementedError

    def get_private_key(self, public_key):
        try:
            self.cas_consumer, created = models.CasConsumer.objects.update_or_create(access_key=public_key)
        except models.CasConsumer.DoesNotExist:
            return
        return self.cas_consumer.secret_key


class CasUserTokenMixin(object):
    token_timeout = timezone.timedelta(seconds=settings.CAS_TOKEN_TIMEOUT)

    @staticmethod
    def _access_denied():
        return HttpResponseForbidden(_('Access denied'))

    @staticmethod
    def _missing_request_token_argument():
        return HttpResponseBadRequest(_('Request token missing'))

    @staticmethod
    def _request_token_not_found():
        return HttpResponseForbidden(_('Request token not found'))

    @staticmethod
    def _request_token_expired():
        return HttpResponseForbidden(_('Request token expired'))

    def has_permission(self):
        return True

    def was_cas_token_expired(self):
        delta = timezone.now() - self.cas_token.timestamp
        if self.token_timeout and delta > self.token_timeout:
            # delete expired cas token
            self.cas_token.delete()
            return True
        return False

    def get_user_data(self, user):
        data = {
            'email': user.email,
            'username': user.username,
            'nickname': user.nickname,
        }
        return data


class CasRequestTokenProvider(CasBaseProvider):
    def provide(self, data):
        # redirect_to needed
        redirect_to = data['redirect_to']
        token, created = models.CasToken.objects.get_or_create(cas_consumer=self.cas_consumer, redirect_to=redirect_to)

        return {'request_token': token.request_token}


class CasUserAuthenticationView(CasUserTokenMixin, View):
    def access_allowed(self):
        self.cas_token.user = self.request.user
        self.cas_token.save()
        serializer = TimedSerializer(self.cas_token.cas_consumer.secret_key)
        url_parser = urlparse.urlparse(self.cas_token.redirect_to)
        query_dict = QueryDict(url_parser.query, mutable=True)
        query_dict['access_token'] = serializer.dumps(self.cas_token.access_token)
        redirect_url = urlparse.urlunparse((
            url_parser.scheme, url_parser.netloc, url_parser.path, '',
            query_dict.urlencode(), ''
        ))

        return HttpResponseRedirect(redirect_url)

    def handle_authenticated_user(self):
        if self.has_permission():
            return self.access_allowed()
        return self._access_denied()

    def handle_unauthenticated_user(self):
        nxt = '{0}?{1}'.format(self.request.path, urllib.urlencode([('request_token', self.cas_token.request_token)]))
        url = '{0}?{1}'.format(settings.LOGIN_URL, urllib.urlencode([('next', nxt)]))

        return HttpResponseRedirect(url)

    def get(self, request):
        request_token = request.GET.get('request_token', None)
        if not request_token:
            return self._missing_request_token_argument()
        try:
            self.cas_token = models.CasToken.objects.get(request_token=request_token)
        except models.CasToken.DoesNotExist:
            return self._request_token_not_found()
        if self.was_cas_token_expired():
            return self._request_token_expired()
        if request.user.is_authenticated:
            return self.handle_authenticated_user()
        return self.handle_unauthenticated_user()


class CasTokenVerificationProvider(CasUserTokenMixin, CasBaseProvider):
    def provide(self, data):
        # access_token needed
        access_token = data['access_token']
        self.cas_token = models.CasToken.objects.get(access_token=access_token)
        if self.was_cas_token_expired():
            pass
        return self.get_user_data(self.cas_token.user)


cas_request_token_view = provider_for_django(CasRequestTokenProvider())
cas_user_authentication_view = CasUserAuthenticationView.as_view()
cas_token_verification_view = provider_for_django(CasTokenVerificationProvider())
