#encoding=utf-8

from django.contrib import admin

from wx.models import Owner, Customer


class OwnerAdmin(admin.ModelAdmin):
    list_display = ['name', 'account']
    search_fields = ['name']

admin.site.register(Owner, OwnerAdmin)


class CustomerAdmin(admin.ModelAdmin):
    list_display = ['account', 'owner', 'create_time']
    search_fields = ['account']
    raw_id_fields = ('owner', )

admin.site.register(Customer, CustomerAdmin)


