#! -*- coding: utf-8 -*-


# author: forcemain@163.com


import os
import json


class HttpMethod(object):
    GET = 'get'
    PUT = 'put'
    POST = 'post'
    DELETE = 'delete'


class BaseRequest(object):
    def __init__(self):
        self._uri = None
        self._data = {}
        self._files = {}
        self._params = {}
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

    def get_files(self):
        return self._files

    def set_files(self, files):
        self._files = files

    def add_file(self, k, v):
        self._files[k] = v

    def get_params(self):
        return self._params

    def set_params(self, params):
        self._params = params

    def add_params(self, k, v):
        self._params[k] = v

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

    def to_req_kwargs(self):
        data = {
            'data': self.get_data(),
            'files': self.get_files(),
            'params': self.get_params(),
            'headers': self.get_headers(),
        }

        return data

    def __str__(self):
        kwargs = self.to_req_kwargs()
        kwargs['files'] = kwargs['files'].keys()
        to_str = json.dumps(kwargs, indent=4)
        return '{0}: method={1} uri={2}{3}{4}'.format(self.__class__, self._method, self._uri, os.linesep, to_str)
