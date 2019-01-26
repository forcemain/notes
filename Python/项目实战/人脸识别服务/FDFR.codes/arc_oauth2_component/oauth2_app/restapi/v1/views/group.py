#! -*- coding: utf-8 -*-


# author: forcemain@163.com


from django.contrib.auth.models import Group
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from utils.rest.view.mixins import JsonModelViewSetMixin
from oauth2_provider.contrib.rest_framework import TokenHasScope


from .. import serializers


class GroupViewSet(JsonModelViewSetMixin, ModelViewSet):
    permission_classes = [IsAuthenticated, TokenHasScope]
    required_scopes = ['groups']
    queryset = Group.objects.all()
    serializer_class = serializers.GroupSerializer
