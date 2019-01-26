#! -*- coding: utf-8 -*-


# author: forcemain@163.com


from django.contrib import admin


from .. import models


class FaceImageAdmin(admin.ModelAdmin):
    list_display = ('pk', 'image', 'user', 'ctime')
    list_filter = ('ctime',)


admin.site.register(models.FaceImage, FaceImageAdmin)
