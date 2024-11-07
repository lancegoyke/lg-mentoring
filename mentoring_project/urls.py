from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static


def trigger_error(request):
    division_by_zero = 1 / 0


urlpatterns = [
    # Django admin
    path("backside/", admin.site.urls),
    # Sentry error testing
    path("sentry-debug/", trigger_error),
    # User management
    path("accounts/", include("allauth.urls")),
    path("accounts/", include("users.urls")),
    # Local apps
    path("", include("pages.urls")),
    path("questions/", include("questions.urls")),
    path("q/", include("questions.urls")),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
