#! -*- coding: utf-8 -*-


# author: forcemain@163.com


from django.contrib import admin


from .. import models


class ChoiceAdmin(admin.ModelAdmin):
    list_per_page = 15
    search_fields = ['choice_text']
    list_display = ['pk', 'choice_text', 'votes', 'question']


admin.site.register(models.Choice, ChoiceAdmin)
