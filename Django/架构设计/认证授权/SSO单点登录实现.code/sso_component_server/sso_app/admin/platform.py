#! -*- coding: utf-8 -*-


# author: forcemain@163.com


from django.contrib import admin


from .. import models


class PlatformAdmin(admin.ModelAdmin):
    list_display = ('pk', 'ip', 'location', 'endpoint', 'ctime')
    search_fields = ('ip', 'location', 'endpoint',)
    list_filter = ('ctime',)


admin.site.register(models.Platform, PlatformAdmin)
