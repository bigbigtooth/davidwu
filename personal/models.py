#encoding=utf-8

from django.db import models


class Blog(models.Model):
    title = models.CharField(max_length=2000)
    tag = models.CharField(max_length=2000, null=True, blank=True)
    summary = models.CharField(max_length=2000, null=True, blank=True)
    text = models.TextField(default='', null=True, blank=True)
    create_time = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return self.title

