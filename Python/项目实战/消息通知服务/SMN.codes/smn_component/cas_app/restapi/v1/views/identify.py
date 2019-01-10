#! -*- coding: utf-8 -*-


# author: forcemain@163.com


from cas_app import models
from django.conf import settings
from utils.rest.view.base import *
from rest_framework import parsers, renderers
from django.utils.translation import ugettext_lazy as _
from utils.rest.exps_handler.exceptions import ExceedMaxIdentityNumberLimit


from .. import serializers


class IdentifyModelViewSet(JsonModelViewSet):
    queryset = models.Identity.objects.all()
    throttle_classes = ()
    permission_classes = ()
    parser_classes = (parsers.FormParser, parsers.MultiPartParser, parsers.JSONParser,)
    renderer_classes = (renderers.JSONRenderer,) if not settings.DEBUG else (
        renderers.BrowsableAPIRenderer, renderers.JSONRenderer,
    )
    serializer_class = serializers.IdentifySerializer

    @staticmethod
    def is_maximize(identify_nu):
        _max = settings.MAX_AKSK_PAIRS_PER_USER

        return _max and identify_nu >= _max

    def perform_create(self, serializer):
        identify_nu = self.request.user.identities.count()
        if self.is_maximize(identify_nu):
            msg = _('Exceed maximum identify number limit.')
            raise ExceedMaxIdentityNumberLimit(msg)
        serializer.save(user=self.request.user)

    def perform_update(self, serializer):
        serializer.save(user=self.request.user)
