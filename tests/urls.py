# -*- coding: utf-8 -*-
from django.conf import settings
from django.conf.urls import include, url
from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

admin.autodiscover()

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
]

if settings.DEBUG:
    urlpatterns = staticfiles_urlpatterns() + urlpatterns
