#! -*- coding: utf-8 -*-


# author: forcemain@163.com


from .base import BaseRequest, HttpMethod


class FaceFeatureExtractRequest(BaseRequest):
    URI = '/staff/feature'

    def __init__(self):
        super(FaceFeatureExtractRequest, self).__init__()
        self.set_uri(self.URI)
        self.set_method(HttpMethod.POST)

    def add_image_data(self, image):
        self.add_file('image', image)


class FaceFeatureStorageRequest(BaseRequest):
    URI = '/face-service-test/staff/upload'

    def __init__(self):
        super(FaceFeatureStorageRequest, self).__init__()
        self.set_uri(self.URI)
        self.set_method(HttpMethod.POST)

    def add_info_data(self, info):
        self.add_data('info', info)

    def add_feature_data(self, feature):
        self.add_data('feature', feature)
