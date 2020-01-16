from django.conf import settings
from django.conf.urls import include, url
import django
from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

admin.autodiscover()

if django.VERSION[0] < 2:
    urlpatterns = [
        url(r'^admin/', include(admin.site.urls)),
    ]
else:
    urlpatterns = [
        url(r'^admin/', admin.site.urls),
    ]

if settings.DEBUG:
    urlpatterns = staticfiles_urlpatterns() + urlpatterns
