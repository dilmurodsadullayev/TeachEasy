from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls.i18n import i18n_patterns



urlpatterns = [
    path("teachhub/", admin.site.urls),
    path('', include('main.urls')),
    path('api/v1/', include('api.urls')),
    path('api/v1/auth/', include('djoser.urls')),
    path('api/v1/auth/', include("djoser.urls.jwt")),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


urlpatterns += i18n_patterns(
    path('set_language/', include('django.conf.urls.i18n')),

)
