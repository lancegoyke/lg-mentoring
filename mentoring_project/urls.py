from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

from debug_toolbar.toolbar import debug_toolbar_urls


urlpatterns = [
    # Django admin
    path("backside/", admin.site.urls),
    # User management
    path("accounts/", include("allauth.urls")),
    path("accounts/", include("users.urls")),
    # Local apps
    path("", include("pages.urls")),
    path("questions/", include("questions.urls")),
    path("q/", include("questions.urls")),
    path("__reload__/", include("django_browser_reload.urls")),
]

if not settings.TESTING:
    urlpatterns += debug_toolbar_urls()

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
