from django.urls import path
from django.urls import path, re_path
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from config.urls import path
from . import views


schema_view = get_schema_view(
    openapi.Info(
        title="TeachEasy",
        default_version='v1',
        description="Bu API ning Swagger hujjatlari",
    ),
    public=True,
    permission_classes=[permissions.AllowAny],
)


urlpatterns = [
    path('',views.UserSayListAPI.as_view()),
    path('<int:pk>/', views.UserSayDetailAPI.as_view()),

    path('courses/',views.CourseListAPI.as_view()),
    path('course/<int:pk>/',views.CourseDetailAPI.as_view()),
    path('teachers/',views.TeacherListAPI.as_view()),
    path("teacher/<int:pk>/", views.TeacherDetailAPI.as_view()),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]