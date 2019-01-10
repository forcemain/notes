#! -*- coding: utf-8 -*-


# author: forcemain@163.com


from django.conf import settings
from django.utils import timezone
from rest_framework import exceptions
from rest_framework.authtoken.models import Token
from django.utils.translation import ugettext_lazy as _
from rest_framework.authentication import TokenAuthentication, get_authorization_header


class AuthTokenAuthentication(TokenAuthentication):
    keyword = 'Token'
    model = Token

    def authenticate(self, request):
        auth = get_authorization_header(request).split()

        if not auth or auth[0].lower() != self.keyword.lower().encode():
            return None

        if len(auth) == 1:
            msg = _('Invalid token header. No credentials provided.')
            raise exceptions.AuthenticationFailed(msg)
        elif len(auth) > 2:
            msg = _('Invalid token header. Token string should not contain spaces.')
            raise exceptions.AuthenticationFailed(msg)

        try:
            token = auth[1].decode()
        except UnicodeError:
            msg = _('Invalid token header. Token string should not contain invalid characters.')
            raise exceptions.AuthenticationFailed(msg)

        return self.authenticate_credentials(token)

    def authenticate_credentials(self, key):
        model = self.get_model()
        try:
            token = model.objects.select_related('user').get(key=key)
        except model.DoesNotExist:
            raise exceptions.AuthenticationFailed(_('Invalid token.'))

        # check expired token
        now, _min = timezone.now(), settings.REST_FRAMEWORK_AUTH_TOKEN_EXPIRE_MINUTES
        if _min and (now - token.created) > timezone.timedelta(minutes=_min):
            raise exceptions.AuthenticationFailed(_('Expired token.'))

        if not token.user.is_active:
            raise exceptions.AuthenticationFailed(_('User inactive or deleted.'))

        return token.user, token
