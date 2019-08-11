#! -*- coding: utf-8 -*-


# author: forcemain@163.com


from django.contrib import admin
from django.utils.translation import ugettext_lazy as _


from .. import models


class CasTokenInline(admin.TabularInline):
    model = models.CasToken
    classes = ('collapse',)
    extra = 0


class CasConsumerAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name', 'access_key', 'secret_key')
    search_fields = ('name',)

    inlines = [CasTokenInline]


class CasTokenAdmin(admin.ModelAdmin):
    list_display = ('pk', 'request_token', 'access_token', 'redirect_to', 'timestamp')
    search_fields = ('redirect_to',)
    list_filter = ('timestamp',)


admin.site.register(models.CasToken, CasTokenAdmin)
admin.site.register(models.CasConsumer, CasConsumerAdmin)
