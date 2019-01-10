#! -*- coding: utf-8 -*-


# author: forcemain@163.com


from django.contrib import admin
from django.utils.translation import ugettext_lazy as _

from .. import models


class IdentityAdmin(admin.ModelAdmin):
    ordering = ('-create_time',)
    list_filter = ('create_time', )
    readonly_fields = ('pk', 'access_key_id', 'secret_access_key')
    list_display = ('pk', 'access_key_id', 'secret_access_key', 'user', 'create_time')
    search_fields = ('access_key_id', 'secret_access_key', 'user__name', 'user__nickname')
    fieldsets = (
        (None, {'fields': ('user', )}),
        (_('identity'), {'fields': ('access_key_id', 'secret_access_key'),
                         'classes': ('collapse', ),
                         'description': _('access key id and secret access key.')}),
    )


admin.site.register(models.Identity, IdentityAdmin)
