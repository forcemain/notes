#! -*- coding: utf-8 -*-


# author: forcemain@163.com


from django.conf import settings
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse_lazy
from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage


from .. import models


def index(request):
    page = request.GET.get('page', 1)

    queryset = models.Question.objects.order_by('-pub_date')
    paginator = Paginator(queryset, per_page=settings.DEFAULT_PAGE_SIZE)
    try:
        questions = paginator.page(page)
    except PageNotAnInteger:
        questions = paginator.page(1)
    except EmptyPage:
        questions = paginator.page(paginator.num_pages)

    return render(request, 'polls/index.html', {'questions': questions})


def detail(request, question_pk):
    question = get_object_or_404(models.Question, pk=question_pk)

    return render(request, 'polls/detail.html', {'question': question})


def result(request, question_pk):
    question = get_object_or_404(models.Question, pk=question_pk)

    return render(request, 'polls/result.html', {'question': question})


def vote(request, question_pk):
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
