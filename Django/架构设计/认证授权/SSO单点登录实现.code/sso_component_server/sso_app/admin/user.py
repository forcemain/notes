#! -*- coding: utf-8 -*-


# author: forcemain@163.com


from django.contrib import admin


from .. import models


class UserAdmin(admin.ModelAdmin):
    list_display = ('pk', 'username', 'nickname', 'email', 'date_joined')
    search_fields = ('username', 'nickname')
    list_filter = ('date_joined',)


admin.site.register(models.User, UserAdmin)
