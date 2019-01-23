#! -*- coding: utf-8 -*-


# author: forcemain@163.com


from django.contrib import admin


from .. import models


class SessionAdmin(admin.ModelAdmin):
    list_display = ('pk', 'session_key', 'user', 'ctime', 'mtime')
    search_fields = ('session_key',)
    list_filter = ('ctime', 'mtime')


admin.site.register(models.Session, SessionAdmin)
