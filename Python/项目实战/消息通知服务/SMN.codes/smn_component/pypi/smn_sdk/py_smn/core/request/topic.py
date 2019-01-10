#! -*- coding: utf-8 -*-


# author: forcemain@163.com


from .base import BaseRequest, HttpMethod


class CreateTopicRequest(BaseRequest):
    URI = '/v1/notifications/topics/'

    def __init__(self):
        super(CreateTopicRequest, self).__init__()
        self.set_uri(self.URI)
        self.set_method(HttpMethod.POST)


class ListTopicRequest(BaseRequest):
    URI = '/v1/notifications/topics/'

    def __init__(self):
        super(ListTopicRequest, self).__init__()
        self.set_uri(self.URI)
        self.set_method(HttpMethod.GET)


class RetrieveTopicRequest(BaseRequest):
    URI = '/v1/notifications/topics/'

    def __init__(self):
        super(RetrieveTopicRequest, self).__init__()
        self.set_uri(self.URI)
        self.set_method(HttpMethod.GET)


class DestroyTopicRequest(BaseRequest):
    URI = '/v1/notifications/topics/'

    def __init__(self):
        super(DestroyTopicRequest, self).__init__()
        self.set_uri(self.URI)
        self.set_method(HttpMethod.POST)


class UpdateTopicRequest(BaseRequest):
    URI = '/v1/notifications/topics/'

    def __init__(self):
        super(UpdateTopicRequest, self).__init__()
        self.set_uri(self.URI)
        self.set_method(HttpMethod.POST)
