#! -*- coding: utf-8 -*-


# author: forcemain@163.com


from __future__ import unicode_literals


from django.db import models


from . import question


class Choice(models.Model):
    question = models.ForeignKey(question.Question)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)

    def __unicode__(self):
        return self.choice_text
