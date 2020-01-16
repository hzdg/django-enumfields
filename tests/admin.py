#!/usr/bin/env python

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
