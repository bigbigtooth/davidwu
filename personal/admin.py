#encoding=utf-8

from django.contrib import admin

from personal.models import Blog


class BlogAdmin(admin.ModelAdmin):
    list_display = ['title', 'summary']
    search_fields = ['title']

admin.site.register(Blog, BlogAdmin)

