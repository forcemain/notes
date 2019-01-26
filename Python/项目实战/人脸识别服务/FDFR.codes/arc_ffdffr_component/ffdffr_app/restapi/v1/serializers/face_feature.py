#! -*- coding: utf-8 -*-


# author: forcemain@163.com


from rest_framework.serializers import ModelSerializer


from ffdffr_app import models


class FaceFeatureSerializer(ModelSerializer):
    class Meta:
        model = models.FaceImage
        fields = ('pk',)
