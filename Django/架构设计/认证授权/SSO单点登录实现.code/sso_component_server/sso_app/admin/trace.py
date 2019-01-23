#! -*- coding: utf-8 -*-


# author: forcemain@163.com


from django.contrib import admin


from .. import models


class TraceAdmin(admin.ModelAdmin):
    list_display = ('pk', 'type', 'ctime',)
    list_filter = ('ctime',)


admin.site.register(models.Trace, TraceAdmin)

