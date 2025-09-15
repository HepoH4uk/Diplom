from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter

from drf_yasg import openapi
from rest_framework import permissions
from drf_yasg.views import get_schema_view

from learning.views import SectionViewSet, LessonViewSet

schema_view = get_schema_view(
    openapi.Info(
        title="Snippets API",
        default_version="v1",
        description="Test description",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="contact@snippets.local"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

router = DefaultRouter()
router.register(r"sections", SectionViewSet)
router.register(r"lessons", LessonViewSet)


urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include(router.urls)),
    path("users/", include("users.urls", namespace="users")),
    path("learning/", include("learning.urls", namespace="learning")),
    path("test/", include("tests.urls", namespace="test")),
    path("questions/", include("tests.urls")),
    path(
        "swagger<format>/", schema_view.without_ui(cache_timeout=0), name="schema-json"
    ),
    path(
        "swagger/",
        schema_view.with_ui("swagger", cache_timeout=0),
        name="schema-swagger-ui",
    ),
    path("redoc/", schema_view.with_ui("redoc", cache_timeout=0), name="schema-redoc"),
]
