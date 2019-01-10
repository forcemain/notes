#! -*- coding: utf-8 -*-


# author: forcemain@163.com


import hmac
import base64


from cas_app.models import Identity
from rest_framework import exceptions
from django.utils.translation import ugettext_lazy as _
from rest_framework.authentication import BaseAuthentication, get_authorization_header


class AuthAkskAuthentication(BaseAuthentication):
    keyword = 'Aksk'
    model = Identity

    def get_model(self):
        if self.model is not None:
            return self.model
        from cas_app.models import Identity
        return Identity

    def authenticate(self, request):
        auth = get_authorization_header(request).split()

        if not auth or auth[0].lower() != self.keyword.lower().encode():
            return None

        if len(auth) == 1:
            msg = _('Invalid aksk header. No credentials provided.')
            raise exceptions.AuthenticationFailed(msg)
        elif len(auth) > 2:
            msg = _('Invalid aksk header. Aksk string should not contain spaces.')
            raise exceptions.AuthenticationFailed(msg)
        if auth[1].count(':') != 1:
            msg = _('Invalid aksk header. Aksk string should contain one colon.')
            raise exceptions.AuthenticationFailed(msg)
        try:
            # access key id and sign
            ak, sign = auth[1].decode().split(':', 1)
        except UnicodeError:
            msg = _('Invalid aksk header. Aksk string should not contain invalid characters.')
            raise exceptions.AuthenticationFailed(msg)

        return self.authenticate_credentials(request, ak, sign)

    def check_sign(self, request, ak, sk, sign):
        code = hmac.new(sk, request.body).digest()
        code_b64 = base64.b64encode(code).replace('/', '_').replace('+', '-')

        return code_b64 == sign

    def authenticate_credentials(self, request, ak, sign):
        model = self.get_model()
        try:
            identity = model.objects.select_related('user').get(access_key_id=ak)
        except model.DoesNotExist:
            raise exceptions.AuthenticationFailed(_('Invalid access key id.'))
        if not identity.enable:
            raise exceptions.AuthenticationFailed(_('Aksk was Frozen.'))
        if not identity.user.is_active:
            raise exceptions.AuthenticationFailed(_('User inactive or deleted.'))
        # check aksk sign
        if not self.check_sign(request, ak, identity.secret_access_key, sign):
            raise exceptions.AuthenticationFailed(_('Invalid aksk sign.'))

        return identity.user, identity
