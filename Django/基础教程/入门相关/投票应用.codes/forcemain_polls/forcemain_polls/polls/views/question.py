#! -*- coding: utf-8 -*-


# author: forcemain@163.com


from django.http import Http404
from django.conf import settings
from django.utils import timezone
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse_lazy
from django.views.generic import ListView, DetailView, View


from .. import models


class PollIndexView(ListView):
    model = models.Question
    context_object_name = 'questions'
    paginate_by = settings.DEFAULT_PAGE_SIZE
    queryset = models.Question.objects.all()

    template_name = 'polls/index.html'

    def get_queryset(self):
        queryset = super(PollIndexView, self).get_queryset()
        return queryset.filter(
            pub_date__lte=timezone.now()
        ).order_by('-pub_date')


class PollDetailView(DetailView):
    model = models.Question
    pk_url_kwarg = 'question_pk'
    context_object_name = 'question'
    queryset = models.Question.objects.all()

    template_name = 'polls/detail.html'

    def get_queryset(self):
        queryset = super(PollDetailView, self).get_queryset()
        return queryset.filter(
            pub_date__lte=timezone.now()
        ).order_by('-pub_date')


class PollResultView(DetailView):
    model = models.Question
    pk_url_kwarg = 'question_pk'
    context_object_name = 'question'
    queryset = models.Question.objects.all()

    template_name = 'polls/result.html'

    def get_queryset(self):
        queryset = super(PollResultView, self).get_queryset()
        return queryset.filter(
            pub_date__lte=timezone.now()
        ).order_by('-pub_date')


class PollVoteView(View):
    def get_queryset(self):
        return models.Question.objects.filter(
            pub_date__lte=timezone.now()
        ).order_by('-pub_date')

    def post(self, request, question_pk):
        queryset = self.get_queryset()
        try:
            question = queryset.get(pk=question_pk)
        except models.Question.DoesNotExist as e:
            raise Http404(e)
        try:
            choice = question.choice_set.get(pk=request.POST['choice_pk'])
        except (KeyError, models.Choice.DoesNotExist):
            return render(request, 'polls/detail.html', {
                'question': question,
                'error_message': 'no choice selected'
            })
        else:
            choice.votes += 1
            choice.save()

            redirect_url = reverse_lazy('polls:tpl-poll-result', args=(question.pk,))
            return HttpResponseRedirect(redirect_url)
