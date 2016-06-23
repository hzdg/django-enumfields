#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.contrib import admin

from enumfields.admin import EnumFieldListFilter

from .models import MyModel


class MyModelAdmin(admin.ModelAdmin):
    model = MyModel
    list_filter = [
        ('color', EnumFieldListFilter),
        ('taste', EnumFieldListFilter),
        ('int_enum', EnumFieldListFilter),
    ]


admin.site.register(MyModel, MyModelAdmin)
