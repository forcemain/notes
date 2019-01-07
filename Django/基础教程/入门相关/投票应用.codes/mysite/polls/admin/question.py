#! -*- coding: utf-8 -*-


# author: forcemain@163.com


from django.contrib import admin


from .. import models


class ChoiceInline(admin.TabularInline):
    model = models.Choice
    classes = ['collapse']
    extra = 3


class QuestionAdmin(admin.ModelAdmin):
    list_per_page = 15
    list_filter = ['pub_date']
    search_fields = ['question_text']
    list_display = ['pk', 'question_text', 'pub_date', 'was_published_recently']
    fieldsets = [
        (None, {'fields': ['question_text']}),
        ('Date infomation', {'fields': ['pub_date'], 'classes': ['collapse'],
                             'description': u'additional descriptive information'})
    ]
    inlines = [ChoiceInline]


admin.site.register(models.Question, QuestionAdmin)
