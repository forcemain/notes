#! -*- coding: utf-8 -*-


# author: forcemain@163.com


from rest_framework.authtoken.admin import TokenAdmin


TokenAdmin.raw_id_fields = ('user', )
TokenAdmin.list_filter = ('created', )
TokenAdmin.list_display = ('key', 'user', 'created')
TokenAdmin.search_fields = ('user__username', 'user__nickname',)
