#! -*- coding: utf-8 -*-


# author: forcemain@163.com


from rest_framework import serializers


from cas_app import models


class IdentifySerializer(serializers.ModelSerializer):
    access_key_id = serializers.CharField(read_only=True)
    secret_access_key = serializers.CharField(read_only=True)
    user_pk = serializers.PrimaryKeyRelatedField(source='user.pk', read_only=True)

    class Meta:
        model = models.Identity
        fields = ('pk', 'access_key_id', 'secret_access_key', 'enable', 'create_time', 'user_pk')
