from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls.i18n import i18n_patterns
from main.views import custom_404
from django.urls import re_path
from django.views.static import serve



urlpatterns = [
    path("teachhub/", admin.site.urls),
    path('', include('main.urls')),
    path('api/v1/', include('api.urls')),
    path('api/v1/auth/', include('djoser.urls')),
    path('api/v1/auth/', include("djoser.urls.jwt")),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
else:
    urlpatterns += [
        re_path(r'^media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT}),
        re_path(r'^static/(?P<path>.*)$', serve, {'document_root': settings.STATIC_ROOT}),
    ]




urlpatterns += i18n_patterns(
    path('set_language/', include('django.conf.urls.i18n')),

)
handler404 = custom_404
