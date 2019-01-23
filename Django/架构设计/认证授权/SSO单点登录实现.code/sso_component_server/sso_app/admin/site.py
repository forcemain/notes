#! -*- coding: utf-8 -*-


# author: forcemain@163.com


from django.contrib import admin


from .. import models


class SiteAdmin(admin.ModelAdmin):
    list_display = ('pk', 'url', 'ctime')
    search_fields = ('url',)
    list_filter = ('ctime',)


admin.site.register(models.Site, SiteAdmin)
