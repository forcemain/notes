#! -*- coding: utf-8 -*-


# author: forcemain@163.com


from django.contrib import admin


from .. import models


class TokenAdmin(admin.ModelAdmin):
    list_display = ('pk', 'access_token', 'user', 'ctime', 'mtime')
    search_fields = ('access_token',)
    list_filter = ('ctime', 'mtime',)


admin.site.register(models.Token, TokenAdmin)
