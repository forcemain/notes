#! -*- coding: utf-8 -*-


# author: forcemain@163.com


from django.contrib.auth import get_user_model
from rest_framework.serializers import ModelSerializer


UserModel = get_user_model()


class UserSerializer(ModelSerializer):
    class Meta:
        model = UserModel
        fields = ('username', 'nickname', 'email',)
