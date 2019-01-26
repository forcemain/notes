#! -*- coding: utf-8 -*-


# author: forcemain@163.com


import os

from ffdffr_app import models
from rest_framework.viewsets import GenericViewSet
from rest_framework.mixins import CreateModelMixin
from rest_framework.permissions import IsAuthenticated
from utils.rest.view.mixins import JsonCreateModelMixin


from .. import serializers


class FaceFeatureViewSet(JsonCreateModelMixin,
                         CreateModelMixin,
                         GenericViewSet):
    permission_classes = (IsAuthenticated,)
    serializer_class = serializers.FaceFeatureSerializer

    def create(self, request, *args, **kwargs):
        response = super(FaceFeatureViewSet, self).create(request, *args, **kwargs)
        print list(self.get_face_feature(response))

        return response

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    @staticmethod
    def destory_faceimg(face_image):
        image_path = face_image.path
        if os.path.exists(image_path):
            os.remove(image_path)
        face_image.delete()

    def get_face_feature(self, response):
        from utils.core.arcsoft.core.manager import FaceDetectionManager, FaceRecognitionManager
        try:
            face_image = models.FaceImage.objects.get(pk=response.data['data']['pk'])
        except (KeyError, models.FaceImage.DoesNotExist):
            return
        with FaceDetectionManager() as fdmanager, FaceRecognitionManager() as frmanager:
            _, faces = fdmanager.do_still_image_detection(face_image.image.path)
            _, face_feature = frmanager.do_extract_frfeature(faces[0])
        self.destory_faceimg(face_image)

        return face_feature
