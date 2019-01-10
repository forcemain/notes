#! -*- coding: utf-8 -*-


# author: forcemain@163.com


from django.conf import settings
from django.utils import timezone
from rest_framework.response import Response
from rest_framework import parsers, renderers
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.serializers import AuthTokenSerializer


class CasTokenAuthView(ObtainAuthToken):
    throttle_classes = ()
    permission_classes = ()
    parser_classes = (parsers.FormParser, parsers.MultiPartParser, parsers.JSONParser,)
    renderer_classes = (renderers.JSONRenderer,) if not settings.DEBUG else (
        renderers.BrowsableAPIRenderer, renderers.JSONRenderer,
    )
    serializer_class = AuthTokenSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        # auto refresh auth-token
        now, _min = timezone.now(), settings.REST_FRAMEWORK_AUTH_TOKEN_EXPIRE_MINUTES
        if not created and _min and (now - token.created) > timezone.timedelta(minutes=_min):
            token.delete()
            token, created = Token.objects.get_or_create(user=user)
        data = {
            'token': token.key,
            'email': user.email,
            'user_pk': user.pk,
            'created': created,
        }
        return Response(data=data)
