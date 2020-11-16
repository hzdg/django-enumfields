from django.conf import settings
from django.urls import re_path
from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

admin.autodiscover()

urlpatterns = [
    re_path(r'^admin/', admin.site.urls),
]

if settings.DEBUG:
    urlpatterns = staticfiles_urlpatterns() + urlpatterns
