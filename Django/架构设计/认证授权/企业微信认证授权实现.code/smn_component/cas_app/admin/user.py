#! -*- coding: utf-8 -*-


# author: forcemain@163.com


from django.contrib import admin
from django.utils.translation import ugettext_lazy as _


from .. import models


class UserAdmin(admin.ModelAdmin):
    readonly_fields = ('date_joined',)
    list_display = ('pk', 'username', 'email', 'is_active', 'is_superuser', 'date_joined')
    list_filter = ('is_active', 'date_joined')
    search_fields = ('username', 'nickname', 'email')
    filter_horizontal = ('groups', 'user_permissions')
    fieldsets = (
        (None, {'fields': ('username',)}),
        (_('profile'), {'fields': ('email',),
                        'classes': ('collapse',),
                        'description': _('user profile')}),
        (_('groups'), {'fields': ('groups',),
                       'classes': ('collapse',),
                       'description': _('user groups')}),
        (_('permissions'), {'fields': ('user_permissions',),
                            'classes': ('collapse',),
                            'description': _('user permissions')}),
        (None, {'fields': ('is_active',)}),
        (None, {'fields': ('is_superuser',)}),
        (None, {'fields': ('date_joined',)}),
    )


admin.site.register(models.User, UserAdmin)
