#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.contrib import admin
from .models import MyModel
from django.contrib.admin.sites import AdminSite, site

myadminsite = AdminSite()


class MyModelAdmin(admin.ModelAdmin):
    model = MyModel

myadminsite.register(MyModel, MyModelAdmin)