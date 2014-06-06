# -*- coding: utf-8 -*-
from django.conf import settings
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

__author__ = 'mikhailturilin'

from django.conf.urls import *
from django.contrib import admin


admin.autodiscover()

urlpatterns = patterns(
    '',
    url(r'^admin/', include(admin.site.urls)),
)

if settings.DEBUG:
    urlpatterns = staticfiles_urlpatterns() + urlpatterns