#! -*- coding: utf-8 -*-


# author: forcemain@163.com


from rest_framework.mixins import *


from ..response import JsonResponse


class JsonCreateModelMixin(CreateModelMixin):
    def create(self, request, *args, **kwargs):
        response = super(JsonCreateModelMixin, self).create(request, *args, **kwargs)

        return JsonResponse(data=response.data)


class JsonListModelMixin(ListModelMixin):
    def list(self, request, *args, **kwargs):
        response = super(JsonListModelMixin, self).list(request, *args, **kwargs)

        return JsonResponse(data=response.data)


class JsonRetrieveModelMixin(RetrieveModelMixin):
    def retrieve(self, request, *args, **kwargs):
        response = super(JsonRetrieveModelMixin, self).retrieve(request, *args, **kwargs)

        return JsonResponse(data=response.data)


class JsonUpdateModelMixin(UpdateModelMixin):
    def update(self, request, *args, **kwargs):
        response = super(JsonUpdateModelMixin, self).update(request, *args, **kwargs)

        return JsonResponse(data=response.data)


class JsonDestroyModelMixin(DestroyModelMixin):
    def destroy(self, request, *args, **kwargs):
        response = super(JsonDestroyModelMixin, self).destroy(request, *args, **kwargs)

        return JsonResponse(data=response.data)
