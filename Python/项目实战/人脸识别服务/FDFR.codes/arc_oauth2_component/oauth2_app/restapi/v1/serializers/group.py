#! -*- coding: utf-8 -*-


# author: forcemain@163.com


from django.contrib.auth.models import Group
from rest_framework.serializers import ModelSerializer


class GroupSerializer(ModelSerializer):
    class Meta:
        model = Group
        fields = ('name',)
