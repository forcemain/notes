#! -*- coding: utf-8 -*-


# author: forcemain@163.com


from django.contrib.auth import get_user_model
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from utils.rest.view.mixins import JsonModelViewSetMixin
from oauth2_provider.contrib.rest_framework import TokenHasReadWriteScope


from .. import serializers


UserModel = get_user_model()


class UserViewSet(JsonModelViewSetMixin, ModelViewSet):
    permission_classes = [IsAuthenticated, TokenHasReadWriteScope]
    queryset = UserModel.objects.all()
    serializer_class = serializers.UserSerializer
