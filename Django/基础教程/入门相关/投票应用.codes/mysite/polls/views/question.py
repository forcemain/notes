#! -*- coding: utf-8 -*-


# author: forcemain@163.com


from django.conf import settings
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse_lazy
from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView, View


from .. import models


class PollIndexView(ListView):
    model = models.Question
    context_object_name = 'questions'
    paginate_by = settings.DEFAULT_PAGE_SIZE
    queryset = models.Question.objects.all()

    template_name = 'polls/index.html'


class PollDetailView(DetailView):
    model = models.Question
    pk_url_kwarg = 'question_pk'
    context_object_name = 'question'
    queryset = models.Question.objects.all()

    template_name = 'polls/detail.html'


class PollResultView(DetailView):
    model = models.Question
    pk_url_kwarg = 'question_pk'
    context_object_name = 'question'
    queryset = models.Question.objects.all()

    template_name = 'polls/result.html'


class PollVoteView(View):
    def post(self, request, question_pk):
        question = get_object_or_404(models.Question, pk=question_pk)
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
