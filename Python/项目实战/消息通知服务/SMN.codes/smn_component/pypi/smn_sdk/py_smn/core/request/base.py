#! -*- coding: utf-8 -*-


# author: forcemain@163.com


class HttpMethod(object):
    GET = 'get'
    PUT = 'put'
    POST = 'post'
    DELETE = 'delete'


class BaseRequest(object):
    def __init__(self):
        self._uri = None
        self._data = {}
        self._headers = {}
        self._endpoint = None
        self._method = HttpMethod.GET

    def get_uri(self):
        return self._uri

    def set_uri(self, uri):
        self._uri = uri

    def get_data(self):
        return self._data

    def set_data(self, data):
        self._data = data

    def add_data(self, key, val):
        self._data[key] = val

    def get_headers(self):
        return self._headers

    def set_headers(self, headers):
        self._headers = headers

    def add_header(self, key, val):
        self._headers[key] = val

    def get_endpoint(self):
        return self._endpoint

    def set_endpoint(self, endpoint):
        self._endpoint = endpoint

    def get_method(self):
        return self._method

    def set_method(self, method):
        self._method = method
