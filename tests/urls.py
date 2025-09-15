from django.urls import path, include
from rest_framework.routers import SimpleRouter
from tests.apps import TestsConfig
from tests.views import (
    TestDetailAPIView,
    TestAttemptCreateAPIView,
    TestAttemptResultAPIView,
    QuestionDetailAPIView,
    TestViewSet,
)


app_name = TestsConfig.name
router = SimpleRouter()
router.register(r"tests", TestViewSet, basename="tests")

urlpatterns = [
    path("", include(router.urls)),
    path("/<int:pk>/", TestDetailAPIView.as_view(), name="test-detail"),
    path(
        "/<int:test_id>/attempts/",
        TestAttemptCreateAPIView.as_view(),
        name="test-attempt-create",
    ),
    path(
        "attempts/<int:pk>/",
        TestAttemptResultAPIView.as_view(),
        name="test-attempt-result",
    ),
    path("questions/<int:pk>/", QuestionDetailAPIView.as_view(), name="quest-detail"),
]
