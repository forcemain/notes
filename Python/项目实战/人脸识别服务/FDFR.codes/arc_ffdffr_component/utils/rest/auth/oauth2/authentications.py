#! -*- coding: utf-8 -*-


# author: forcemain@163.com


import requests


from requests.exceptions import HTTPError
from django.utils.encoding import smart_text
from django.contrib.auth import get_user_model
from rest_framework.settings import perform_import
from django.utils.translation import ugettext_lazy as _
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.authentication import get_authorization_header, BaseAuthentication


from .settings import oauth2_client_settings


class Oauth2BearerTokenAuthentication(BaseAuthentication):
    www_authenticate_realm = 'api'

    @staticmethod
    def get_user_model():
        return get_user_model()

    @staticmethod
    def get_token_model():
        return perform_import(oauth2_client_settings.OAUTH2_CLIENT_TOKEN_MODEL,
                              oauth2_client_settings.OAUTH2_CLIENT_TOKEN_MODEL_NAME)

    def authenticate(self, request):
        bearer_token = self.get_bearer_token(request)
        if not bearer_token:
            return
        try:
            ruser = self.get_remote_user(bearer_token)
        except HTTPError:
            raise AuthenticationFailed(_('Invalid Authorization header. Unable to verify bearer token'))
        luser = self.get_local_user(ruser, bearer_token)

        return luser, ruser

    def get_bearer_token(self, request):
        auth = get_authorization_header(request).split()
        bearer_header_prefix = oauth2_client_settings.OAUTH2_SERVER_BEARER_HEADER_PREFIX.lower()
        if not auth or smart_text(auth[0].lower()) != bearer_header_prefix:
            return
        if len(auth) == 1:
            raise AuthenticationFailed(_('Invalid Authorization header. No credentials provided'))
        if len(auth) > 2:
            raise AuthenticationFailed(_('Invalid Authorization header. Credentials string should not contain spaces.'))

        return auth[1]

    def get_local_user(self, ruser, bearer_token):
        UserModel, TokenModel = self.get_user_model(), self.get_token_model()
        try:
            user, created = UserModel.objects.get_or_create(username=ruser['username'])
            user.set_unusable_password()
        except KeyError:
            raise AuthenticationFailed(_('Invalid remote user, username field required'))
        TokenModel.objects.update_or_create(defaults={'token': bearer_token,
                                                      'endpoint': oauth2_client_settings.OAUTH2_SERVER_USER_ENDPOINT},
                                            user=user)
        return user

    @staticmethod
    def get_remote_user(bearer_token):
        bearer_token = bearer_token.decode('ascii')
        response = requests.get(oauth2_client_settings.OAUTH2_SERVER_USER_ENDPOINT, params={'token': bearer_token},
                                headers={'Authorization': 'Bearer {0}'.format(bearer_token)})
        response.raise_for_status()

        return response.json()
