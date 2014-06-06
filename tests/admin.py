#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.contrib import admin
from .models import MyModel
from django.contrib.admin.sites import AdminSite, site

class MyModelAdmin(admin.ModelAdmin):
    model = MyModel

site.register(MyModel, MyModelAdmin)