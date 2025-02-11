from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls.i18n import i18n_patterns

# Asosiy URL'lar
urlpatterns = [
    path("teachhub/", admin.site.urls),
    path('', include('main.urls')),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# Tilni almashtirish uchun URL yo'nalishlari (i18n_patterns ichida)
urlpatterns += i18n_patterns(
    # Tilni o'zgartirish uchun URL'ni qo'shadi
    path('set_language/', include('django.conf.urls.i18n')),  # Django tomonidan taqdim etilgan tilni o'zgartirish
    # Agar boshqa URL'lar bo'lsa, ularni shu yerga qo'shish mumkin
)
