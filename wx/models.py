#encoding=utf-8

from django.db import models


class Owner(models.Model):
    name = models.CharField(max_length=2000, blank=True)
    desc = models.CharField(max_length=2000, blank=True)
    account = models.CharField(max_length=2000, blank=True)
    pwd = models.CharField(max_length=2000, blank=True)
    create_time = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return self.name


class Customer(models.Model):
    owner = models.ForeignKey(Owner)
    account = models.CharField(max_length=2000, blank=True)
    info = models.CharField(max_length=2000, blank=True)
    create_time = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return self.account

