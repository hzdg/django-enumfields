#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.contrib import admin

from enumfields.admin import EnumFieldListFilter

from .models import MyModel, RestrictedModel


class MyModelAdmin(admin.ModelAdmin):
    model = MyModel
    list_filter = [
        ('color', EnumFieldListFilter),
        ('taste', EnumFieldListFilter),
        ('int_enum', EnumFieldListFilter),
    ]


class RestrictedModelAdmin(admin.ModelAdmin):
    model = RestrictedModel


admin.site.register(MyModel, MyModelAdmin)
admin.site.register(RestrictedModel, RestrictedModelAdmin)
