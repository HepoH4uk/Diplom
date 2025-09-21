from django.urls import path, include
from rest_framework.routers import SimpleRouter

from learning.apps import LearningConfig
from learning.views import LessonViewSet, SectionViewSet


app_name = LearningConfig.name

router = SimpleRouter()
router.register(r"sections", SectionViewSet, basename="sections")
router.register(r"lessons", LessonViewSet, basename="lessons")

urlpatterns = [
    path("", include(router.urls)),
]
