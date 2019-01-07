#! -*- coding: utf-8 -*-


# author: forcemain@163.com


from django.conf.urls import url


from . import views


app_name = 'polls'


urlpatterns = [
    url('^$', views.question.index, name='tpl-poll-index'),
    url('(?P<question_pk>[0-9]+)/$', views.question.detail, name='tpl-poll-detail'),
    url('(?P<question_pk>[0-9]+)/vote/$', views.question.vote, name='rdr-poll-vote'),
    url('(?P<question_pk>[0-9]+)/result/$', views.question.result, name='tpl-poll-result')
]
