#encoding=utf-8

from django.conf.urls import patterns,  url

urlpatterns = \
    patterns('',
             url(r'^$', 'website.views.index'),
             url(r'^wx/$', 'website.views.wx'),
             )
