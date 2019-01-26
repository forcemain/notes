#! -*- coding: utf-8 -*-


# author: forcemain@163.com


from rest_framework.viewsets import ReadOnlyModelViewSet, ModelViewSet
from rest_framework.generics import (
    CreateAPIView, ListAPIView, RetrieveAPIView, DestroyAPIView, UpdateAPIView, ListCreateAPIView,
    RetrieveUpdateAPIView, RetrieveDestroyAPIView, RetrieveUpdateDestroyAPIView,
)


from .mixins import *


class JsonCreateAPIView(JsonCreateModelMixin, CreateAPIView):
    pass


class JsonListAPIView(JsonListModelMixin, ListAPIView):
    pass


class JsonRetrieveAPIView(JsonRetrieveModelMixin, RetrieveAPIView):
    pass


class JsonDestroyAPIView(JsonDestroyModelMixin, DestroyAPIView):
    pass


class JsonUpdateAPIView(JsonUpdateModelMixin, UpdateAPIView):
    pass


class JsonListCreateAPIView(JsonListModelMixin, JsonCreateModelMixin, ListCreateAPIView):
    pass


class JsonRetrieveUpdateAPIView(JsonRetrieveModelMixin, JsonUpdateModelMixin, RetrieveUpdateAPIView):
    pass


class JsonRetrieveDestroyAPIView(JsonRetrieveModelMixin, JsonDestroyModelMixin, RetrieveDestroyAPIView):
    pass


class JsonRetrieveUpdateDestroyAPIView(JsonRetrieveModelMixin, JsonUpdateModelMixin, JsonDestroyModelMixin,
                                       RetrieveUpdateDestroyAPIView):
    pass


class JsonReadOnlyModelViewSet(JsonRetrieveModelMixin, JsonListModelMixin, ReadOnlyModelViewSet):
    pass


class JsonModelViewSet(JsonCreateModelMixin, JsonRetrieveModelMixin, JsonUpdateModelMixin, JsonDestroyModelMixin,
                       JsonListModelMixin, ModelViewSet):
    pass

