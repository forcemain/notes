#! -*- coding: utf-8 -*-


# author: forcemain@163.com


from django.conf.urls import url


from . import views


app_name = 'polls'


urlpatterns = [
    url('^$', views.question.PollIndexView.as_view(), name='tpl-poll-index'),
    url('(?P<question_pk>[0-9]+)/$', views.question.PollDetailView.as_view(), name='tpl-poll-detail'),
    url('(?P<question_pk>[0-9]+)/vote/$', views.question.PollVoteView.as_view(), name='rdr-poll-vote'),
    url('(?P<question_pk>[0-9]+)/result/$', views.question.PollResultView.as_view(), name='tpl-poll-result')
]
